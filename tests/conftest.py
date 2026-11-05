from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRS = {
    path.name.removeprefix("word-fillter-438c-"): path
    for path in sorted((REPO_ROOT / "skills").glob("word-fillter-438c-*"))
    if (path / "scripts" / "rules.py").is_file() and (path / "templates").is_dir()
}
SKILL_IDS = tuple(SKILL_DIRS)

SHARED_DIR = REPO_ROOT / "shared"
_ENGINE_MODULES = ("docx_ops", "errors", "loader", "models", "pipeline")


def load_engine(skill_id: str) -> SimpleNamespace:
    """加载仓库根 shared/ 的共享引擎，并导入该 Skill 的 rules.py。

    返回的命名空间包含各引擎模块，以及 ``rules``（该 Skill 的模板专属规则）。
    规则模块以唯一名称加载，避免不同 Skill 的 rules 在同一进程内互相覆盖。
    """
    if str(SHARED_DIR) not in sys.path:
        sys.path.insert(0, str(SHARED_DIR))
    modules = {name: importlib.import_module(f"strict_word_filler.{name}") for name in _ENGINE_MODULES}
    spec = importlib.util.spec_from_file_location(
        f"rules_{skill_id}", SKILL_DIRS[skill_id] / "scripts" / "rules.py"
    )
    rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rules)
    modules["rules"] = rules
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
