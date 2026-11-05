from __future__ import annotations

from pathlib import Path

from docx import Document

import sys

# 共享引擎位于仓库根 shared/（本文件位于 skills/<id>/scripts/）
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import rules  # noqa: E402  模板专属规则
from strict_word_filler.docx_ops import apply_plan  # noqa: E402
from strict_word_filler.loader import build_plan, load_json  # noqa: E402


BASE_DIR = Path(__file__).resolve().parent
SKILL_DIR = BASE_DIR.parent
TEMPLATE_PATH = SKILL_DIR / "documents" / "[01]软件总体技术方案-438C.docx"
CONFIG_PATH = SKILL_DIR / "templates" / "config.json"
PROJECT_PATH = SKILL_DIR / "templates" / "project.json"
OUTPUT_PATH = BASE_DIR / "output" / "[01]软件总体技术方案-438C-filled.docx"


def main() -> int:
    config_data = load_json(CONFIG_PATH)
    project_data = load_json(PROJECT_PATH)
    plan = build_plan(config_data, project_data, rules)

    doc = Document(str(TEMPLATE_PATH))
    apply_plan(doc, plan)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUTPUT_PATH))
    print(f"文档已生成: {OUTPUT_PATH}")
    print("目录字段已标记为需要更新，首次在 Word 中打开时应刷新目录。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
