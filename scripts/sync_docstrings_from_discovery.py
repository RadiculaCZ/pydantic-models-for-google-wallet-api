#!/usr/bin/env python3
"""
Synchronize model docstrings from the Google Wallet discovery document.
"""

from __future__ import annotations

import argparse
import ast
import inspect
import sys
import textwrap
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import libcst as cst
from _discovery_common import (
    DiscoverySchema,
    ModelInfo,
    iter_schema_candidates_for_model,
    load_models_and_schemas,
    unwrap_annotated,
    unwrap_optional,
)


class UpdateMode(str, Enum):
    FILL_MISSING = "fill-missing"
    OVERWRITE = "overwrite"
    INTERACTIVE = "interactive"


@dataclass(frozen=True)
class Change:
    file_path: Path
    class_name: str
    target_name: str | None
    kind: str
    current: str | None
    desired: str


@dataclass(frozen=True)
class Conflict:
    file_path: Path
    class_name: str
    target_name: str | None
    kind: str
    candidates: tuple[tuple[str, str], ...]


@dataclass
class ClassUpdate:
    class_doc: str | None = None
    member_docs: dict[str, str] = field(default_factory=dict)
    changes: list[Change] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.changes)


def normalize_format_hint(format_hint: str | None) -> str | None:
    if not format_hint:
        return None
    normalized = format_hint.lower().strip()
    if normalized == "byte":
        return None
    return normalized


def wrap_description(text: str) -> str:
    paragraphs = [part.strip() for part in text.strip().split("\n\n")]
    wrapped: list[str] = []
    for paragraph in paragraphs:
        if not paragraph:
            wrapped.append("")
            continue
        lines = [line.strip() for line in paragraph.splitlines()]
        compact = " ".join(line for line in lines if line)
        wrapped.append(
            textwrap.fill(
                compact,
                width=75,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return "\n\n".join(wrapped).strip()


def render_docstring(
    description: str | None,
    format_hint: str | None = None,
) -> str | None:
    parts: list[str] = []
    normalized_format = normalize_format_hint(format_hint)
    if normalized_format:
        parts.append(f"{normalized_format} format")

    if description and description.strip():
        wrapped = wrap_description(description)
        if wrapped:
            if parts:
                parts.append("")
            parts.append(wrapped)

    if not parts:
        return None

    return "\n".join(parts)


def render_enum_member_docs(prop) -> dict[str, str]:
    if prop.desc.kind != "enum":
        return {}

    raw_descriptions = prop.enum_descriptions
    raw_values = prop.enum_values
    if not raw_descriptions:
        return {}

    if len(raw_values) != len(raw_descriptions):
        return {}

    docs: dict[str, str] = {}
    for enum_name, description in zip(raw_values, raw_descriptions, strict=False):
        if description and description.strip():
            docs[enum_name] = wrap_description(description)
    return docs


def normalize_doc(doc: str | None) -> str | None:
    if not doc:
        return None
    cleaned = inspect.cleandoc(doc)
    return cleaned if cleaned else None


def should_change(
    current: str | None,
    desired: str,
    mode: UpdateMode,
) -> bool:
    if current == desired:
        return False
    if mode == UpdateMode.FILL_MISSING:
        return not current
    return True


def resolve_consensus(
    candidates: list[tuple[str, str | None]],
) -> tuple[str | None, tuple[tuple[str, str], ...]]:
    filtered = [(name, value) for name, value in candidates if value]
    if not filtered:
        return None, ()

    unique_values = {value for _, value in filtered}
    if len(unique_values) == 1:
        return filtered[0][1], ()

    return None, tuple(filtered)


def resolve_enum_consensus(
    candidates: list[tuple[str, dict[str, str]]],
) -> tuple[dict[str, str], tuple[tuple[str, str], ...]]:
    filtered = [(name, value) for name, value in candidates if value]
    if not filtered:
        return {}, ()

    rendered = {
        name: "\n".join(f"{key}: {value}" for key, value in sorted(mapping.items()))
        for name, mapping in filtered
    }
    unique_values = set(rendered.values())
    if len(unique_values) == 1:
        return filtered[0][1], ()

    return {}, tuple((name, rendered[name]) for name, _ in filtered)


def extract_enum_class(annotation: object) -> type[str] | None:
    inner = unwrap_annotated(annotation)
    inner, _ = unwrap_optional(inner)
    if not inspect.isclass(inner):
        return None
    if not issubclass(inner, str):
        return None
    if not hasattr(inner, "__members__"):
        return None
    return inner


def build_sync_plan(
    models: list[ModelInfo],
    schemas: Mapping[str, DiscoverySchema],
    mode: UpdateMode,
) -> tuple[dict[Path, dict[str, ClassUpdate]], list[Change], list[Conflict]]:
    updates_by_file: dict[Path, dict[str, ClassUpdate]] = defaultdict(dict)
    conflicts: list[Conflict] = []
    seen_changes: set[tuple[Path, str, str | None, str, str]] = set()
    seen_conflicts: set[
        tuple[Path, str, str | None, str, tuple[tuple[str, str], ...]]
    ] = set()
    enum_current_docs: dict[type, dict[str, str]] = {}

    def record_change(class_update: ClassUpdate, change: Change) -> None:
        key = (
            change.file_path,
            change.class_name,
            change.target_name,
            change.kind,
            change.desired,
        )
        if key in seen_changes:
            return
        seen_changes.add(key)
        class_update.changes.append(change)

    def add_conflict(conflict: Conflict) -> None:
        key = (
            conflict.file_path,
            conflict.class_name,
            conflict.target_name,
            conflict.kind,
            conflict.candidates,
        )
        if key in seen_conflicts:
            return
        seen_conflicts.add(key)
        conflicts.append(conflict)

    for model in models:
        schema_candidates = iter_schema_candidates_for_model(model, schemas)
        if not schema_candidates:
            continue

        per_file_updates = updates_by_file[model.file_path]
        class_update = per_file_updates.setdefault(model.name, ClassUpdate())

        class_doc_candidates = [
            (schema.name, render_docstring(schema.description))
            for schema in schema_candidates
        ]
        desired_class_doc, class_conflict = resolve_consensus(class_doc_candidates)
        if class_conflict:
            add_conflict(
                Conflict(
                    file_path=model.file_path,
                    class_name=model.name,
                    target_name=None,
                    kind="class-doc",
                    candidates=class_conflict,
                )
            )
        elif desired_class_doc and should_change(
            normalize_doc(model.class_doc),
            desired_class_doc,
            mode,
        ):
            class_update.class_doc = desired_class_doc
            record_change(
                class_update,
                Change(
                    file_path=model.file_path,
                    class_name=model.name,
                    target_name=None,
                    kind="class-doc",
                    current=normalize_doc(model.class_doc),
                    desired=desired_class_doc,
                ),
            )

        for field_name in model.fields:
            field_candidates = []
            enum_candidates = []
            enum_cls = extract_enum_class(
                model.cls.model_fields[field_name].annotation,
            )

            for schema in schema_candidates:
                prop = schema.properties.get(field_name)
                if not prop:
                    continue
                field_candidates.append(
                    (
                        schema.name,
                        render_docstring(prop.description, prop.format_hint),
                    )
                )
                if enum_cls is not None:
                    enum_candidates.append((schema.name, render_enum_member_docs(prop)))

            desired_field_doc, field_conflict = resolve_consensus(field_candidates)
            if field_conflict:
                add_conflict(
                    Conflict(
                        file_path=model.file_path,
                        class_name=model.name,
                        target_name=field_name,
                        kind="field-doc",
                        candidates=field_conflict,
                    )
                )
            elif desired_field_doc and should_change(
                normalize_doc(model.field_docs.get(field_name)),
                desired_field_doc,
                mode,
            ):
                class_update.member_docs[field_name] = desired_field_doc
                record_change(
                    class_update,
                    Change(
                        file_path=model.file_path,
                        class_name=model.name,
                        target_name=field_name,
                        kind="field-doc",
                        current=normalize_doc(model.field_docs.get(field_name)),
                        desired=desired_field_doc,
                    ),
                )

            if enum_cls is None:
                continue

            desired_enum_docs, enum_conflict = resolve_enum_consensus(enum_candidates)
            enum_file_path = Path(inspect.getfile(enum_cls)).resolve()
            current_member_docs = enum_current_docs.setdefault(
                enum_cls,
                {},
            )
            if not current_member_docs:
                try:
                    module = ast.parse(
                        enum_file_path.read_text(encoding="utf-8"),
                        filename=str(enum_file_path),
                    )
                except OSError:
                    module = None
                if module is not None:
                    for node in module.body:
                        if (
                            isinstance(node, ast.ClassDef)
                            and node.name == enum_cls.__name__
                        ):
                            for idx, stmt in enumerate(node.body):
                                next_stmt = (
                                    node.body[idx + 1]
                                    if idx + 1 < len(node.body)
                                    else None
                                )
                                if not isinstance(stmt, ast.Assign):
                                    continue
                                if len(stmt.targets) != 1:
                                    continue
                                target = stmt.targets[0]
                                if not isinstance(target, ast.Name):
                                    continue
                                if (
                                    isinstance(next_stmt, ast.Expr)
                                    and isinstance(next_stmt.value, ast.Constant)
                                    and isinstance(next_stmt.value.value, str)
                                ):
                                    current_member_docs[target.id] = (
                                        next_stmt.value.value
                                    )

            if enum_conflict:
                add_conflict(
                    Conflict(
                        file_path=enum_file_path,
                        class_name=enum_cls.__name__,
                        target_name=field_name,
                        kind="enum-member-doc",
                        candidates=enum_conflict,
                    )
                )
                continue

            if not desired_enum_docs:
                continue

            enum_updates = updates_by_file[enum_file_path].setdefault(
                enum_cls.__name__,
                ClassUpdate(),
            )
            for member_name, desired_member_doc in desired_enum_docs.items():
                current_doc = normalize_doc(current_member_docs.get(member_name))
                if not should_change(current_doc, desired_member_doc, mode):
                    continue
                enum_updates.member_docs[member_name] = desired_member_doc
                record_change(
                    enum_updates,
                    Change(
                        file_path=enum_file_path,
                        class_name=enum_cls.__name__,
                        target_name=member_name,
                        kind="enum-member-doc",
                        current=current_doc,
                        desired=desired_member_doc,
                    ),
                )

    all_changes = [
        change
        for file_updates in updates_by_file.values()
        for class_update in file_updates.values()
        for change in class_update.changes
    ]
    return updates_by_file, all_changes, conflicts


def is_docstring_stmt(stmt: cst.BaseStatement) -> bool:
    if not isinstance(stmt, cst.SimpleStatementLine):
        return False
    if len(stmt.body) != 1:
        return False
    expr = stmt.body[0]
    return isinstance(expr, cst.Expr) and isinstance(expr.value, cst.SimpleString)


def extract_stmt_name(stmt: cst.BaseStatement) -> str | None:
    if not isinstance(stmt, cst.SimpleStatementLine):
        return None
    if len(stmt.body) != 1:
        return None

    inner = stmt.body[0]
    if isinstance(inner, cst.AnnAssign) and isinstance(inner.target, cst.Name):
        return inner.target.value

    if isinstance(inner, cst.Assign) and len(inner.targets) == 1:
        target = inner.targets[0].target
        if isinstance(target, cst.Name):
            return target.value

    return None


def stmt_doc_value(stmt: cst.BaseStatement) -> str | None:
    if not is_docstring_stmt(stmt):
        return None
    assert isinstance(stmt, cst.SimpleStatementLine)
    expr = stmt.body[0]
    assert isinstance(expr, cst.Expr)
    assert isinstance(expr.value, cst.SimpleString)
    return ast.literal_eval(expr.value.value)


def build_doc_stmt(content: str, indent: str) -> cst.SimpleStatementLine:
    lines = content.splitlines() or [""]
    escaped_lines = [line.replace("\\", "\\\\") for line in lines]
    rendered = "\n".join(f"{indent}{line}" if line else "" for line in escaped_lines)
    literal = f'"""\n{rendered}\n{indent}"""'
    return cst.SimpleStatementLine(body=[cst.Expr(value=cst.SimpleString(literal))])


class DocstringTransformer(cst.CSTTransformer):
    def __init__(self, updates: dict[str, ClassUpdate], indent: str) -> None:
        self.updates = updates
        self.indent = indent

    def leave_ClassDef(
        self,
        original_node: cst.ClassDef,
        updated_node: cst.ClassDef,
    ) -> cst.ClassDef:
        update = self.updates.get(updated_node.name.value)
        if not update or not isinstance(updated_node.body, cst.IndentedBlock):
            return updated_node

        body = list(updated_node.body.body)
        new_body: list[cst.BaseStatement] = []
        index = 0

        if original_node.name.value == "GroupingInfo":
            print("debug here")

        if update.class_doc is not None:
            existing_class_doc = (
                body[0] if body and is_docstring_stmt(body[0]) else None
            )
            if existing_class_doc is not None:
                new_body.append(build_doc_stmt(update.class_doc, self.indent))
                index = 1
            else:
                new_body.append(build_doc_stmt(update.class_doc, self.indent))

        while index < len(body):
            stmt = body[index]
            name = extract_stmt_name(stmt)
            next_stmt = body[index + 1] if index + 1 < len(body) else None
            existing_doc_stmt = (
                next_stmt
                if next_stmt is not None and is_docstring_stmt(next_stmt)
                else None
            )

            new_body.append(stmt)
            if name is None:
                index += 1
                continue

            desired_doc = update.member_docs.get(name)
            if desired_doc is None:
                if existing_doc_stmt is not None:
                    new_body.append(existing_doc_stmt)
                    index += 2
                    continue
                index += 1
                continue

            new_body.append(build_doc_stmt(desired_doc, self.indent))
            index += 2 if existing_doc_stmt is not None else 1

        return updated_node.with_changes(
            body=updated_node.body.with_changes(body=tuple(new_body))
        )


def format_target(change: Change | Conflict) -> str:
    if change.target_name is None:
        return change.class_name
    return f"{change.class_name}.{change.target_name}"


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync model docstrings against Google Wallet discovery.",
    )
    parser.add_argument("--offline", type=Path, help="Use a local discovery JSON")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply the computed docstring updates in place.",
    )
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in UpdateMode],
        default=UpdateMode.OVERWRITE.value,
        help="How to handle existing differing docstrings.",
    )
    return parser.parse_args(list(argv))


def print_report(changes: list[Change], conflicts: list[Conflict]) -> None:
    print("## Planned changes")
    if not changes:
        print("(none)")
    else:
        for change in sorted(
            changes,
            key=lambda item: (
                str(item.file_path),
                item.class_name,
                item.target_name or "",
                item.kind,
            ),
        ):
            rel_path = change.file_path.relative_to(Path.cwd())
            print(f"- {rel_path}: {change.kind} -> {format_target(change)}")

    print("\n## Conflicts")
    if not conflicts:
        print("(none)")
    else:
        for conflict in sorted(
            conflicts,
            key=lambda item: (
                str(item.file_path),
                item.class_name,
                item.target_name or "",
                item.kind,
            ),
        ):
            rel_path = conflict.file_path.relative_to(Path.cwd())
            print(f"- {rel_path}: {conflict.kind} -> {format_target(conflict)}")
            for source_name, rendered in conflict.candidates:
                print(f"  * {source_name}: {rendered}")


def confirm_file_write(file_path: Path, change_count: int) -> bool:
    prompt = (
        f"Apply {change_count} change(s) to {file_path.relative_to(Path.cwd())}? [y/N] "
    )
    answer = input(prompt).strip().lower()
    return answer in {"y", "yes"}


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    mode = UpdateMode(args.mode)

    if mode == UpdateMode.INTERACTIVE and not args.write:
        print("--mode interactive requires --write", file=sys.stderr)
        return 2

    schemas, models = load_models_and_schemas(args.offline)
    updates_by_file, changes, conflicts = build_sync_plan(models, schemas, mode)

    print_report(changes, conflicts)

    if conflicts:
        print(
            f"\nWarning: {len(conflicts)} conflict(s) detected. "
            "Conflicted targets are skipped; continuing with non-conflicting updates.",
            file=sys.stderr,
        )

    if not changes:
        return 0

    if not args.write:
        return 1

    if mode == UpdateMode.INTERACTIVE and not sys.stdin.isatty():
        print("interactive mode requires a TTY", file=sys.stderr)
        return 2

    changes_by_file: dict[Path, int] = defaultdict(int)
    for change in changes:
        changes_by_file[change.file_path] += 1

    for file_path, class_updates in sorted(updates_by_file.items()):
        if not class_updates:
            continue
        if mode == UpdateMode.INTERACTIVE and not confirm_file_write(
            file_path,
            changes_by_file[file_path],
        ):
            continue

        source = file_path.read_text(encoding="utf-8")
        module = cst.parse_module(source)
        transformed = module.visit(
            DocstringTransformer(class_updates, module.default_indent)
        )
        if transformed.code != source:
            file_path.write_text(transformed.code, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
