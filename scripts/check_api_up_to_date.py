#!/usr/bin/env python3
"""
Check whether local Pydantic models are in sync with Google Wallet discovery.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from _discovery_common import (
    PKG_ONLY_MODELS,
    RE_DEFAULT,
    RE_REQUIRED,
    DiscoverySchema,
    ModelInfo,
    choose_model_for_schema,
    collect_model_info,
    compare_type_desc,
    discover_ast_docs_for_package,
    load_discovery,
    load_package,
    normalize_text,
    parse_discovery_schemas,
    split_docstring_format,
)


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

    payload = load_discovery(args.offline)
    schemas = parse_discovery_schemas(payload)

    pkg = load_package()
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
    import sys

    raise SystemExit(main(sys.argv[1:]))
