from __future__ import annotations

import ast
import fnmatch
import importlib
import inspect
import json
import re
import sys
from collections.abc import Iterable, Mapping
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
    enum_values: tuple[str, ...] = ()
    enum_descriptions: tuple[str, ...] = ()
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
    file_path: Path


def ensure_src_on_path() -> None:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))


def load_package():
    ensure_src_on_path()
    return importlib.import_module(PACKAGE_NAME)


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

            enum_values = tuple(str(value) for value in (prop.get("enum") or ()))
            enum_descriptions = tuple(
                str(value) for value in (prop.get("enumDescriptions") or ())
            )

            props[prop_name] = DiscoveryProp(
                name=prop_name,
                desc=parse_discovery_type(prop),
                description=prop.get("description"),
                format_hint=format_hint,
                enum_values=enum_values,
                enum_descriptions=enum_descriptions,
                deprecated=bool(prop.get("deprecated", False)),
            )
        schemas[name] = DiscoverySchema(
            name=name,
            description=raw.get("description"),
            properties=props,
        )
    return schemas


def _is_deprecated_call(node: ast.expr) -> bool:
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id in {"deprecated", "_te_deprecated"}
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "deprecated":
                return True
    return False


def _contains_deprecated_in_annotation(node: ast.expr) -> bool:
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
                file_path=Path(inspect.getfile(obj)).resolve(),
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


def load_models_and_schemas(
    offline: Path | None,
) -> tuple[dict[str, DiscoverySchema], list[ModelInfo]]:
    payload = load_discovery(offline)
    schemas = parse_discovery_schemas(payload)
    pkg = load_package()
    ast_docs = discover_ast_docs_for_package(pkg)
    models = collect_model_info(pkg, ast_docs)
    return schemas, models


def iter_schema_candidates_for_model(
    model: ModelInfo,
    schemas: Mapping[str, DiscoverySchema],
) -> list[DiscoverySchema]:
    matches: list[DiscoverySchema] = []
    for schema_name, schema in schemas.items():
        for pattern in model.schema_patterns:
            if pattern == schema_name:
                matches.append(schema)
                break
            if is_pattern(pattern) and fnmatch.fnmatch(schema_name, pattern):
                matches.append(schema)
                break
    return sorted(matches, key=lambda item: item.name)


def is_basemodel_subclass(obj: object) -> bool:
    return inspect.isclass(obj) and issubclass(obj, BaseModel)


def iter_model_infos(models: Iterable[ModelInfo]) -> dict[str, ModelInfo]:
    return {model.name: model for model in models}
