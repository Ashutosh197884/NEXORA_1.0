"""Safe local project inspection services."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean
from typing import Any

from nexora.policies.paths import PathPolicyError, resolve_workspace_path

TEXT_SUFFIXES = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".json", ".jsonl", ".md",
    ".txt", ".toml", ".yaml", ".yml", ".html", ".css", ".scss", ".sql", ".sh",
    ".bat", ".ps1", ".env.example", ".ini", ".cfg", ".xml", ".csv", ".gitignore",
}


class ToolInputError(ValueError):
    """Raised for a validly transported but invalid tool argument."""


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError):
        return False


def list_project_files(root: Path, path: str = ".", *, max_entries: int = 500) -> dict[str, Any]:
    target = resolve_workspace_path(root, path)
    if not target.is_dir():
        raise ToolInputError("path must refer to a directory")
    entries: list[dict[str, Any]] = []
    truncated = False
    for child in sorted(target.iterdir(), key=lambda item: item.name.casefold()):
        try:
            resolved = child.resolve(strict=True)
        except OSError:
            continue
        if not _is_within(resolved, root):
            continue
        if len(entries) >= max_entries:
            truncated = True
            break
        entries.append({
            "name": child.name,
            "path": child.relative_to(root.resolve()).as_posix(),
            "type": "directory" if resolved.is_dir() else "file" if resolved.is_file() else "other",
        })
    return {"path": target.relative_to(root.resolve()).as_posix() or ".", "entries": entries,
            "truncated": truncated}


def read_project_file(root: Path, path: str, *, max_bytes: int = 1_048_576) -> dict[str, Any]:
    target = resolve_workspace_path(root, path)
    if not target.is_file():
        raise ToolInputError("path must refer to a file")
    if target.suffix.lower() not in TEXT_SUFFIXES and target.name not in {".gitignore", ".env.example", "Dockerfile"}:
        raise ToolInputError("unsupported text file type")
    size = target.stat().st_size
    if size > max_bytes:
        raise ToolInputError(f"file exceeds the {max_bytes}-byte read limit")
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ToolInputError("file is not valid UTF-8 text") from exc
    return {"path": target.relative_to(root.resolve()).as_posix(), "size_bytes": size, "content": content}


def search_project_code(
    root: Path,
    query: str,
    path: str = ".",
    *,
    max_results: int = 100,
    max_file_bytes: int = 1_048_576,
) -> dict[str, Any]:
    if not isinstance(query, str) or not query.strip():
        raise ToolInputError("query must not be empty")
    if len(query) > 500:
        raise ToolInputError("query must be 500 characters or fewer")
    target = resolve_workspace_path(root, path)
    if not target.is_file() and not target.is_dir():
        raise ToolInputError("path must refer to a file or directory")
    candidates = [target] if target.is_file() else sorted(target.rglob("*"))
    results: list[dict[str, Any]] = []
    scanned = 0
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            relative = resolved.relative_to(root.resolve()).as_posix()
        except (OSError, ValueError):
            continue
        if not _is_within(resolved, root):
            continue
        if resolved.suffix.lower() not in TEXT_SUFFIXES and resolved.name not in {".gitignore", ".env.example", "Dockerfile"}:
            continue
        try:
            if resolved.stat().st_size > max_file_bytes:
                continue
            text = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        scanned += 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            if query.casefold() in line.casefold():
                results.append({"path": relative, "line": line_number, "snippet": line[:500]})
                if len(results) >= max_results:
                    return {"query": query, "matches": results, "scanned_files": scanned, "truncated": True}
    return {"query": query, "matches": results, "scanned_files": scanned, "truncated": False}


def _numeric_summaries(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    if not rows:
        return {}
    summaries: dict[str, dict[str, float | int]] = {}
    for key in rows[0]:
        values: list[float] = []
        for row in rows:
            value = row.get(key)
            if value is None or isinstance(value, bool):
                continue
            try:
                number = float(value)
            except (TypeError, ValueError):
                continue
            if number == number and abs(number) != float("inf"):
                values.append(number)
        if values:
            summaries[key] = {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": fmean(values),
            }
    return summaries


def inspect_data_file(root: Path, path: str, *, max_bytes: int = 10_485_760) -> dict[str, Any]:
    target = resolve_workspace_path(root, path)
    if not target.is_file():
        raise ToolInputError("path must refer to a file")
    suffix = target.suffix.lower()
    if suffix not in {".csv", ".json"}:
        raise ToolInputError("only .csv and .json files are supported")
    size = target.stat().st_size
    if size > max_bytes:
        raise ToolInputError(f"file exceeds the {max_bytes}-byte inspection limit")
    try:
        raw = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ToolInputError("file is not valid UTF-8 text") from exc

    if suffix == ".json":
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ToolInputError("invalid JSON file") from exc
        if isinstance(parsed, list):
            sample = parsed[:1000]
            keys = sorted({key for item in sample if isinstance(item, dict) for key in item})
            rows = [item for item in sample if isinstance(item, dict)]
            return {"path": target.relative_to(root.resolve()).as_posix(), "format": "json",
                    "size_bytes": size, "top_level_type": "array", "record_count": len(parsed),
                    "sampled_records": len(sample), "keys": keys,
                    "numeric_summary": _numeric_summaries(rows)}
        if isinstance(parsed, dict):
            return {"path": target.relative_to(root.resolve()).as_posix(), "format": "json",
                    "size_bytes": size, "top_level_type": "object", "keys": sorted(parsed.keys()),
                    "record_count": len(parsed)}
        return {"path": target.relative_to(root.resolve()).as_posix(), "format": "json",
                "size_bytes": size, "top_level_type": type(parsed).__name__, "record_count": None}

    try:
        with target.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = reader.fieldnames or []
            rows: list[dict[str, Any]] = []
            record_count = 0
            for row in reader:
                record_count += 1
                if len(rows) < 1000:
                    rows.append(dict(row))
    except (csv.Error, OSError) as exc:
        raise ToolInputError("invalid CSV file") from exc
    return {"path": target.relative_to(root.resolve()).as_posix(), "format": "csv",
            "size_bytes": size, "columns": columns, "record_count": record_count,
            "sampled_records": len(rows), "numeric_summary": _numeric_summaries(rows)}
