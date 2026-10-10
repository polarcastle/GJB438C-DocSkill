from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = {
    "08": REPO_ROOT / "skills" / "word-fillter-438c-08",
    "10": REPO_ROOT / "skills" / "word-fillter-438c-10",
}
SKILL_IDS = tuple(SKILL_DIRS)

_ENGINE_MODULES = ("docx_ops", "errors", "loader", "models", "pipeline", "template_rules")


def load_engine(skill_id: str) -> SimpleNamespace:
    """Import one skill's strict_word_filler package in isolation.

    Both skills ship a package named ``strict_word_filler``; purge any
    previously imported copy so the two never mix in one pytest process.
    """
    scripts_dir = SKILL_DIRS[skill_id] / "scripts"
    for name in [n for n in sys.modules if n == "strict_word_filler" or n.startswith("strict_word_filler.")]:
        del sys.modules[name]
    sys.path.insert(0, str(scripts_dir))
    try:
        modules = {name: importlib.import_module(f"strict_word_filler.{name}") for name in _ENGINE_MODULES}
    finally:
        sys.path.remove(str(scripts_dir))
    return SimpleNamespace(**modules)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def template_path(skill_id: str) -> Path:
    return next((SKILL_DIRS[skill_id] / "documents").glob("*.docx"))


def config_data(skill_id: str) -> dict:
    return load_json(SKILL_DIRS[skill_id] / "templates" / "config.json")


def project_data(skill_id: str) -> dict:
    return load_json(SKILL_DIRS[skill_id] / "templates" / "project.json")


def minimal_config() -> dict:
    def entry(value: str) -> dict:
        return {"content": value}

    return {
        "project": {
            "name": entry("测试系统"),
            "short_name": entry("CS"),
            "version": entry("V1.0"),
            "company": entry("测试单位"),
        },
        "document": {
            "id": entry("DOC-001"),
            "title": entry("测试文档"),
            "classification": entry("内部"),
            "phase": entry("方案"),
            "date": entry("2026年10月11日"),
        },
    }
