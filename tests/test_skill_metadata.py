from __future__ import annotations

import re
from collections import Counter

import pytest

from conftest import REPO_ROOT, SKILL_DIRS, SKILL_IDS


def _frontmatter_line(skill_id: str, key: str) -> str:
    text = (SKILL_DIRS[skill_id] / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(rf"^{key}:.*$", text, re.M)
    assert match, f"{skill_id} SKILL.md 缺少 {key} 字段"
    return match.group(0)


def _process_refs(skill_id: str) -> tuple[str, str, str]:
    """返回 process.py 中 (TEMPLATE_PATH 文件名, OUTPUT_PATH 文件名, 模板所在目录键)。"""
    src = (SKILL_DIRS[skill_id] / "scripts" / "process.py").read_text(encoding="utf-8")
    template_line = next(line for line in src.splitlines() if line.startswith("TEMPLATE_PATH ="))
    output_line = next(line for line in src.splitlines() if line.startswith("OUTPUT_PATH ="))
    template_name = re.findall(r'"([^"]+\.docx)"', template_line)[0]
    output_name = re.findall(r'"([^"]+\.docx)"', output_line)[0]
    anchor = "documents" if "SKILL_DIR /" in template_line else "scripts"
    return template_name, output_name, anchor


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_frontmatter_name_matches_directory(skill_id):
    assert _frontmatter_line(skill_id, "name") == f"name: word-fillter-438c-{skill_id}"


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_description_has_no_generic_trigger(skill_id):
    # 通用短语与裸「438C」会让所有 Skill 同时命中，必须由文档名称/缩写触发
    desc = _frontmatter_line(skill_id, "description")
    assert "按照438C模板填写word文档" not in desc
    assert "「438C」" not in desc


def test_description_triggers_are_unique_across_skills():
    counter: Counter[str] = Counter()
    for skill_id in SKILL_IDS:
        desc = _frontmatter_line(skill_id, "description")
        counter.update(set(re.findall(r"「([^」]+)」", desc)))
    dups = sorted(k for k, v in counter.items() if v > 1)
    assert not dups, f"触发关键词在多个 Skill 间重复: {dups}"


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_process_template_exists_in_own_documents(skill_id):
    template_name, _, anchor = _process_refs(skill_id)
    skill_dir = SKILL_DIRS[skill_id]
    if anchor == "documents":
        assert (skill_dir / "documents" / template_name).is_file()
    else:
        assert (skill_dir / "scripts" / template_name).is_file()
    own_docs = [p.name for p in (skill_dir / "documents").glob("*.docx")]
    assert template_name in own_docs, f"process.py 引用的模板 {template_name} 不属于本 Skill"


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_process_output_name_derives_from_template(skill_id):
    template_name, output_name, _ = _process_refs(skill_id)
    assert output_name.startswith(template_name[: -len(".docx")]), (
        f"输出文件名 {output_name} 应以模板名 {template_name} 为前缀，避免不同 Skill 互相覆盖"
    )


def test_process_output_names_are_unique():
    outputs = [_process_refs(s)[1] for s in SKILL_IDS]
    assert len(outputs) == len(set(outputs))


def test_08_requirements_lives_with_scripts():
    assert (REPO_ROOT / "skills/word-fillter-438c-08/scripts/requirements.txt").is_file()
    assert not (REPO_ROOT / "skills/word-fillter-438c-08/documents/requirements.txt").exists()
