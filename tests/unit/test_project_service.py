from __future__ import annotations

import json
from pathlib import Path

import pytest

from nexora.policies.paths import PathPolicyError
from nexora.services.project_service import (
    ToolInputError,
    inspect_data_file,
    list_project_files,
    read_project_file,
    search_project_code,
)


def test_list_project_files(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    result = list_project_files(tmp_path, ".")
    assert [entry["name"] for entry in result["entries"]] == ["README.md", "src"]


def test_read_project_file(tmp_path: Path) -> None:
    (tmp_path / "hello.py").write_text("print('hello')", encoding="utf-8")
    result = read_project_file(tmp_path, "hello.py")
    assert result["content"] == "print('hello')"


def test_read_rejects_oversized_file(tmp_path: Path) -> None:
    (tmp_path / "large.txt").write_text("x" * 20, encoding="utf-8")
    with pytest.raises(ToolInputError, match="exceeds"):
        read_project_file(tmp_path, "large.txt", max_bytes=10)


def test_search_project_code(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("alpha\nNEXORA rocks\n", encoding="utf-8")
    result = search_project_code(tmp_path, "nexora")
    assert result["matches"][0]["line"] == 2
    assert result["matches"][0]["path"] == "main.py"


def test_inspect_csv(tmp_path: Path) -> None:
    (tmp_path / "metrics.csv").write_text("name,value\na,2\nb,4\n", encoding="utf-8")
    result = inspect_data_file(tmp_path, "metrics.csv")
    assert result["record_count"] == 2
    assert result["numeric_summary"]["value"]["mean"] == 3.0


def test_inspect_json(tmp_path: Path) -> None:
    (tmp_path / "data.json").write_text(json.dumps([{"score": 3}, {"score": 5}]), encoding="utf-8")
    result = inspect_data_file(tmp_path, "data.json")
    assert result["record_count"] == 2
    assert result["numeric_summary"]["score"]["max"] == 5.0


def test_rejects_unsupported_data_format(tmp_path: Path) -> None:
    (tmp_path / "data.xml").write_text("<root />", encoding="utf-8")
    with pytest.raises(ToolInputError, match="only .csv and .json"):
        inspect_data_file(tmp_path, "data.xml")


def test_rejects_empty_search(tmp_path: Path) -> None:
    with pytest.raises(ToolInputError, match="must not be empty"):
        search_project_code(tmp_path, "  ")


def test_absolute_path_rejected(tmp_path: Path) -> None:
    with pytest.raises(PathPolicyError, match="absolute paths"):
        read_project_file(tmp_path, str(tmp_path / "secret.txt"))
