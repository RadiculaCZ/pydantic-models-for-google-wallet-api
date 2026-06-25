#!/usr/bin/env python3
"""
Check whether local Pydantic models are in sync with Google Wallet discovery.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import importlib
import inspect
import json
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from types import UnionType
from typing import Any, get_args, get_origin

import requests
from pydantic import BaseModel

DISCOVERY_URL = "https://walletobjects.googleapis.com/$discovery/rest?version=v1"
PACKAGE_NAME = "pydantic_models_for_google_wallet_api"
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

PKG_ONLY_MODELS = {
    "JWT",
    "JwtPayload",
}

RE_REQUIRED = re.compile(r"^\s*required\b", flags=re.IGNORECASE)
RE_DEFAULT = re.compile(r"\bby default\b|\bdefault\b", flags=re.IGNORECASE)
RE_FORMAT_LINE = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s+format\s*$")


@dataclass
class TypeDesc:
    kind: str
    base: str | None = None
    ref: str | None = None
    enum_values: set[str] = field(default_factory=set)
    item: "TypeDesc | None" = None
    optional: bool = False

    def render(self) -> str:
        if self.kind == "ref":
            return self.ref or "unknown"
        if self.kind == "array":
            return f"array[{self.item.render() if self.item else 'unknown'}]"
        if self.kind == "enum":
            return f"{self.base}(enum)"
        return self.base or "unknown"


@dataclass
class DiscoveryProp:
    name: str
    desc: TypeDesc
    description: str | None
    format_hint: str | None
    deprecated: bool = False


@dataclass
class DiscoverySchema:
    name: str
    description: str | None
    properties: dict[str, DiscoveryProp]


@dataclass
class AstClassDocs:
    class_doc: str | None
    field_docs: dict[str, str]
    member_docs: dict[str, str]
    deprecated_fields: set[str] = field(default_factory=set)


@dataclass
class ModelInfo:
    cls: type[BaseModel]
    name: str
    fields: dict[str, TypeDesc]
    required: dict[str, bool]
    deprecated_fields: set[str]
    field_docs: dict[str, str]
    class_doc: str | None
    schema_patterns: tuple[str, ...]


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    text = value.replace("`", "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_docstring_format(value: str | None) -> tuple[str | None, str | None]:
    """
    Split a field docstring into (format_hint, description_without_format_line).

    The format hint is recognized only when the first non-empty line follows the
    convention: "<format> format".
    """
    if value is None:
        return None, None

    lines = value.splitlines()
    first_non_empty_idx: int | None = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_non_empty_idx = idx
            break

    if first_non_empty_idx is None:
        return None, value

    match = RE_FORMAT_LINE.match(lines[first_non_empty_idx].strip())
    if not match:
        return None, value

    format_hint = match.group(1).lower()
    lines_without_format = (
        lines[:first_non_empty_idx] + lines[first_non_empty_idx + 1 :]
    )
    return format_hint, "\n".join(lines_without_format)


def is_pattern(value: str) -> bool:
    return any(ch in value for ch in "*?[")


def download_discovery(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def load_discovery(offline: Path | None) -> dict[str, Any]:
    if offline:
        return json.loads(offline.read_text(encoding="utf-8"))
    return download_discovery(DISCOVERY_URL)


def parse_discovery_type(schema: dict[str, Any]) -> TypeDesc:
    if "$ref" in schema:
        return TypeDesc(kind="ref", ref=schema["$ref"])

    dtype = schema.get("type")
    enum_values = schema.get("enum") or []

    if dtype == "array":
        items = schema.get("items", {})
        return TypeDesc(kind="array", base="array", item=parse_discovery_type(items))

    if dtype == "object":
        return TypeDesc(kind="scalar", base="object")

    if enum_values:
        return TypeDesc(
            kind="enum",
            base=dtype or "string",
            enum_values={str(v) for v in enum_values},
        )

    return TypeDesc(kind="scalar", base=dtype or "unknown")


def parse_discovery_schemas(payload: dict[str, Any]) -> dict[str, DiscoverySchema]:
    schemas: dict[str, DiscoverySchema] = {}
    for name, raw in payload.get("schemas", {}).items():
        props: dict[str, DiscoveryProp] = {}
        for prop_name, prop in raw.get("properties", {}).items():
            format_hint = prop.get("format")
            if format_hint is None and prop.get("type") == "array":
                items = prop.get("items", {})
                format_hint = items.get("format")

            props[prop_name] = DiscoveryProp(
                name=prop_name,
                desc=parse_discovery_type(prop),
                description=prop.get("description"),
                format_hint=format_hint,
                deprecated=bool(prop.get("deprecated", False)),
            )
        schemas[name] = DiscoverySchema(
            name=name,
            description=raw.get("description"),
            properties=props,
        )
    return schemas


def _is_deprecated_call(node: ast.expr) -> bool:
    """Check if a node is a call to deprecated() or imports deprecated() from typing_extensions."""
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id in {"deprecated", "_te_deprecated"}
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "deprecated":
                return True
    return False


def _contains_deprecated_in_annotation(node: ast.expr) -> bool:
    """Check if an Annotated type contains deprecated()."""
    if isinstance(node, ast.Subscript):
        if isinstance(node.value, ast.Name) and node.value.id == "Annotated":
            if isinstance(node.slice, ast.Tuple):
                for elt in node.slice.elts:
                    if _is_deprecated_call(elt):
                        return True
            elif _is_deprecated_call(node.slice):
                return True
        return _contains_deprecated_in_annotation(node.value)
    return False


def parse_class_docs_from_file(file_path: Path) -> dict[str, AstClassDocs]:
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    result: dict[str, AstClassDocs] = {}

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        class_doc = ast.get_docstring(node)
        field_docs: dict[str, str] = {}
        member_docs: dict[str, str] = {}
        deprecated_fields: set[str] = set()
        body = node.body

        for idx, stmt in enumerate(body):
            next_stmt = body[idx + 1] if idx + 1 < len(body) else None
            doc_value = None
            if (
                isinstance(next_stmt, ast.Expr)
                and isinstance(next_stmt.value, ast.Constant)
                and isinstance(next_stmt.value.value, str)
            ):
                doc_value = next_stmt.value.value

            name = None
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                name = stmt.target.id
                if _contains_deprecated_in_annotation(stmt.annotation):
                    deprecated_fields.add(name)
            elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
                target = stmt.targets[0]
                if isinstance(target, ast.Name):
                    name = target.id

            if name and doc_value:
                field_docs[name] = doc_value
                member_docs[name] = doc_value

        result[node.name] = AstClassDocs(
            class_doc=class_doc,
            field_docs=field_docs,
            member_docs=member_docs,
            deprecated_fields=deprecated_fields,
        )

    return result


def discover_ast_docs_for_package(pkg) -> dict[str, AstClassDocs]:
    docs: dict[str, AstClassDocs] = {}
    package_dir = Path(pkg.__file__).resolve().parent

    for py_file in package_dir.glob("*.py"):
        module_docs = parse_class_docs_from_file(py_file)
        docs.update(module_docs)

    return docs


def unwrap_optional(annotation: Any) -> tuple[Any, bool]:
    origin = get_origin(annotation)
    if origin is None:
        return annotation, False

    if origin is UnionType or str(origin).endswith("typing.Union"):
        args = get_args(annotation)
        non_none = [arg for arg in args if arg is not type(None)]
        if len(non_none) == 1 and len(non_none) != len(args):
            return non_none[0], True

    return annotation, False


def unwrap_annotated(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is None:
        return annotation

    if str(origin).endswith("typing.Annotated"):
        args = get_args(annotation)
        if args:
            return unwrap_annotated(args[0])

    return annotation


def parse_model_type(annotation: Any) -> TypeDesc:
    ann = unwrap_annotated(annotation)
    ann, opt = unwrap_optional(ann)

    origin = get_origin(ann)
    args = get_args(ann)

    if origin is list and args:
        item_desc = parse_model_type(args[0])
        return TypeDesc(kind="array", base="array", item=item_desc, optional=opt)

    if origin is not None and str(origin).endswith("typing.Literal"):
        literal_values = set(str(v) for v in args)
        desc = TypeDesc(kind="enum", base="string", enum_values=literal_values)
        desc.optional = opt
        return desc

    if inspect.isclass(ann):
        if issubclass(ann, BaseModel):
            return TypeDesc(kind="ref", ref=ann.__name__, optional=opt)

        if issubclass(ann, str):
            if hasattr(ann, "__members__"):
                enum_values = {str(v.value) for v in ann.__members__.values()}
                return TypeDesc(
                    kind="enum",
                    base="string",
                    enum_values=enum_values,
                    optional=opt,
                )

        if ann is str:
            return TypeDesc(kind="scalar", base="string", optional=opt)

        if ann is int:
            return TypeDesc(kind="scalar", base="integer", optional=opt)

        if ann is float:
            return TypeDesc(kind="scalar", base="number", optional=opt)

        if ann is bool:
            return TypeDesc(kind="scalar", base="boolean", optional=opt)

        if ann is dict:
            return TypeDesc(kind="scalar", base="object", optional=opt)

    return TypeDesc(kind="scalar", base="unknown", optional=opt)


def collect_model_info(pkg, ast_docs: dict[str, AstClassDocs]) -> list[ModelInfo]:
    models: list[ModelInfo] = []

    for symbol in getattr(pkg, "__all__", []):
        obj = getattr(pkg, symbol, None)
        if not inspect.isclass(obj):
            continue

        if not issubclass(obj, BaseModel):
            continue

        docs = ast_docs.get(obj.__name__, AstClassDocs(None, {}, {}))
        fields: dict[str, TypeDesc] = {}
        required: dict[str, bool] = {}

        deprecated_fields: set[str] = set()
        for field_name, field_info in obj.model_fields.items():
            fields[field_name] = parse_model_type(field_info.annotation)
            required[field_name] = field_info.is_required()
        deprecated_fields = docs.deprecated_fields

        schema_patterns = tuple(getattr(obj, "__discovery_schemas__", (obj.__name__,)))

        models.append(
            ModelInfo(
                cls=obj,
                name=obj.__name__,
                fields=fields,
                required=required,
                deprecated_fields=deprecated_fields,
                field_docs=docs.field_docs,
                class_doc=docs.class_doc,
                schema_patterns=schema_patterns,
            )
        )

    unique: dict[str, ModelInfo] = {}
    for model in models:
        unique[model.name] = model

    return list(unique.values())


def choose_model_for_schema(
    schema_name: str,
    models: list[ModelInfo],
) -> ModelInfo | None:
    exact: list[ModelInfo] = []
    pattern: list[tuple[int, ModelInfo]] = []

    for model in models:
        for item in model.schema_patterns:
            if item == schema_name:
                exact.append(model)
                break
            if is_pattern(item) and fnmatch.fnmatch(schema_name, item):
                pattern.append((len(item), model))

    if exact:
        return sorted(exact, key=lambda m: m.name)[0]

    if pattern:
        pattern.sort(key=lambda p: p[0], reverse=True)
        return pattern[0][1]

    return None


def ref_matches(
    api_ref: str,
    model_ref: str,
    model_by_name: dict[str, ModelInfo],
) -> bool:
    if api_ref == model_ref:
        return True

    model = model_by_name.get(model_ref)
    if not model:
        return False

    for pattern in model.schema_patterns:
        if is_pattern(pattern):
            if fnmatch.fnmatch(api_ref, pattern):
                return True
            continue

        if pattern == api_ref:
            return True

    return False


def compare_type_desc(
    api: TypeDesc,
    model: TypeDesc,
    model_by_name: dict[str, ModelInfo],
) -> tuple[bool, str]:
    if api.kind != model.kind:
        if api.kind == "scalar" and api.base == "string" and model.kind == "enum":
            return True, ""
        return False, f"expected {api.render()}, got {model.render()}"

    if api.kind == "ref":
        if not api.ref or not model.ref:
            return False, f"expected {api.render()}, got {model.render()}"
        if not ref_matches(api.ref, model.ref, model_by_name):
            return False, f"expected {api.render()}, got {model.render()}"
        return True, ""

    if api.kind == "array":
        if not api.item or not model.item:
            return False, f"expected {api.render()}, got {model.render()}"
        if model.item.base == "unknown":
            return True, ""
        return compare_type_desc(api.item, model.item, model_by_name)

    if api.kind == "enum":
        if model.kind != "enum" and model.base != api.base:
            return False, f"expected {api.render()}, got {model.render()}"

    if api.base != model.base and api.base != "unknown" and model.base != "unknown":
        return False, f"expected {api.render()}, got {model.render()}"

    return True, ""


def compare(
    schemas: dict[str, DiscoverySchema],
    models: list[ModelInfo],
    check_docstrings: bool,
) -> dict[str, Any]:
    mapped: dict[str, ModelInfo] = {}
    model_by_name = {model.name: model for model in models}

    for schema_name in schemas:
        model = choose_model_for_schema(schema_name, models)
        if model:
            mapped[schema_name] = model

    model_names_mapped = {model.name for model in mapped.values()}
    api_names_mapped = set(mapped)

    type_missing = sorted(set(schemas) - api_names_mapped)
    type_superfluous = sorted(
        model.name
        for model in models
        if model.name not in model_names_mapped and model.name not in PKG_ONLY_MODELS
    )

    field_lines: list[str] = []
    enum_lines: list[str] = []
    deprecation_lines: list[str] = []
    advisory_lines: list[str] = []
    doc_lines: list[str] = []

    for schema_name in sorted(api_names_mapped):
        schema = schemas[schema_name]
        model = mapped[schema_name]

        api_fields = set(schema.properties)
        model_fields = set(model.fields)

        missing_fields = sorted(api_fields - model_fields)
        superfluous_fields = sorted(model_fields - api_fields)

        if missing_fields or superfluous_fields:
            field_lines.append(f"[{schema_name} -> {model.name}]")
            for name in missing_fields:
                field_lines.append(f"+ {name}")
            for name in superfluous_fields:
                field_lines.append(f"- {name}")

        for field_name in sorted(api_fields & model_fields):
            api_prop = schema.properties[field_name]
            model_desc = model.fields[field_name]
            model_field_doc_raw = model.field_docs.get(field_name)
            model_doc_format, model_field_doc_wo_format = split_docstring_format(
                model_field_doc_raw
            )

            if model.name in {
                "ResourceListing",
                "ResourcePaginatedListing",
                "ResourceResponse",
            } and field_name in {"resources", "resource"}:
                ok, reason = True, ""
            else:
                ok, reason = compare_type_desc(
                    api_prop.desc,
                    model_desc,
                    model_by_name,
                )
            if not ok:
                field_lines.append(f"~ {schema_name}.{field_name}: {reason}")

            if api_prop.desc.kind == "enum" and model_desc.kind == "enum":
                missing_enum = sorted(
                    api_prop.desc.enum_values - model_desc.enum_values
                )
                extra_enum = sorted(model_desc.enum_values - api_prop.desc.enum_values)
                if missing_enum or extra_enum:
                    enum_lines.append(f"[{schema_name}.{field_name}]")
                    for value in missing_enum:
                        enum_lines.append(f"+ {value}")
                    for value in extra_enum:
                        enum_lines.append(f"- {value}")

            api_deprecated = api_prop.deprecated
            model_deprecated = field_name in model.deprecated_fields
            if api_deprecated and not model_deprecated:
                deprecation_lines.append(
                    f"+ {schema_name}.{field_name} (deprecated in API, not in model)"
                )
            elif model_deprecated and not api_deprecated:
                deprecation_lines.append(
                    f"- {schema_name}.{field_name} (deprecated in model, not in API)"
                )

            api_format = api_prop.format_hint.lower() if api_prop.format_hint else None
            if api_format == "byte":
                if model_doc_format is not None:
                    advisory_lines.append(
                        f"[format] {schema_name}.{field_name}: "
                        f"superfluous docstring format '{model_doc_format} format' "
                        "(API uses byte format represented as bytes type annotation)"
                    )
            elif api_format:
                if model_doc_format is None:
                    advisory_lines.append(
                        f"[format] {schema_name}.{field_name}: "
                        f"missing docstring format line '{api_format} format'"
                    )
                elif model_doc_format != api_format:
                    advisory_lines.append(
                        f"[format] {schema_name}.{field_name}: "
                        f"docstring format line is '{model_doc_format} format', "
                        f"expected '{api_format} format'"
                    )
            elif model_doc_format is not None:
                advisory_lines.append(
                    f"[format] {schema_name}.{field_name}: "
                    f"superfluous docstring format '{model_doc_format} format' "
                    "(API has no format constraint)"
                )

            api_desc_norm = normalize_text(api_prop.description)
            inferred_required = bool(RE_REQUIRED.match(api_desc_norm))
            has_default_hint = bool(RE_DEFAULT.search(api_desc_norm))
            model_required = model.required.get(field_name, False)

            if inferred_required and not model_required:
                advisory_lines.append(
                    f"[required] {schema_name}.{field_name}: "
                    "API description says required"
                )

            if has_default_hint and model_required:
                advisory_lines.append(
                    f"[default] {schema_name}.{field_name}: "
                    "API mentions default but model field is required"
                )

            if check_docstrings:
                model_field_doc = normalize_text(model_field_doc_wo_format)
                if (
                    api_desc_norm
                    and model_field_doc
                    and api_desc_norm != model_field_doc
                ):
                    doc_lines.append(f"~ {schema_name}.{field_name}: docstring differs")

        if check_docstrings:
            api_doc = normalize_text(schema.description)
            model_doc = normalize_text(model.class_doc)
            if api_doc and model_doc and api_doc != model_doc:
                doc_lines.append(f"~ {schema_name}: class docstring differs")

    return {
        "types": {
            "missing_in_package": type_missing,
            "superfluous_in_package": type_superfluous,
        },
        "fields": field_lines,
        "enums": enum_lines,
        "deprecations": deprecation_lines,
        "advisory": sorted(set(advisory_lines)),
        "docstrings": sorted(set(doc_lines)),
    }


def render_text_report(result: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.append("## Types")
    for name in result["types"]["missing_in_package"]:
        lines.append(f"+ {name} (in API, missing from package)")
    for name in result["types"]["superfluous_in_package"]:
        lines.append(f"- {name} (in package, not in API)")
    if len(lines) == 1:
        lines.append("(none)")

    lines.append("\n## Fields")
    if result["fields"]:
        lines.extend(result["fields"])
    else:
        lines.append("(none)")

    lines.append("\n## Enums")
    if result["enums"]:
        lines.extend(result["enums"])
    else:
        lines.append("(none)")

    lines.append("\n## Deprecations")
    if result["deprecations"]:
        lines.extend(result["deprecations"])
    else:
        lines.append("(none)")

    lines.append("\n## Advisory")
    if result["advisory"]:
        lines.extend(result["advisory"])
    else:
        lines.append("(none)")

    lines.append("\n## Docstrings")
    if result["docstrings"]:
        lines.extend(result["docstrings"])
    else:
        lines.append("(none)")

    return "\n".join(lines) + "\n"


def has_primary_discrepancy(result: dict[str, Any]) -> bool:
    return any(
        [
            result["types"]["missing_in_package"],
            result["types"]["superfluous_in_package"],
            result["fields"],
            result["enums"],
            result["deprecations"],
        ]
    )


def has_secondary_discrepancy(result: dict[str, Any]) -> bool:
    return any([result["advisory"], result["docstrings"]])


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check package models against Google Wallet discovery schemas."
    )
    parser.add_argument("--offline", type=Path, help="Use a local discovery JSON")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit machine-readable JSON output",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on advisory and docstring discrepancies too",
    )
    parser.add_argument(
        "--no-docstrings",
        action="store_true",
        help="Skip docstring comparison",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)

    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    payload = load_discovery(args.offline)
    schemas = parse_discovery_schemas(payload)

    pkg = importlib.import_module(PACKAGE_NAME)
    ast_docs = discover_ast_docs_for_package(pkg)
    models = collect_model_info(pkg, ast_docs)

    result = compare(
        schemas=schemas,
        models=models,
        check_docstrings=not args.no_docstrings,
    )

    if args.json_output:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_text_report(result), end="")

    if has_primary_discrepancy(result):
        return 1

    if args.strict and has_secondary_discrepancy(result):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
