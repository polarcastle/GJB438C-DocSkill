from __future__ import annotations

import json
import subprocess
import sys

import pytest
from docx import Document
from docx.oxml.ns import qn

from conftest import SKILL_DIRS, SKILL_IDS, config_data, load_engine, project_data, template_path


def _doc_all_text(doc) -> str:
    texts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.append(cell.text)
    for section in doc.sections:
        texts.extend(p.text for p in section.header.paragraphs)
        texts.extend(p.text for p in section.footer.paragraphs)
    return "\n".join(texts)


FORBIDDEN_ANCHORS = {
    "08": (
        "外部型号+产品名称",
        "XXXX年XX月XX日",
        "产品型号-XXXX",
        "标题：Software Requirements Specification",
        "Test-引用文档",
        "Test 3.2",
        "Test table",
        "《GB/T 0018》",
        "《GB/T 0028》",
        "合规性方法",
        "合规性级别",
        "3.1.2维护状态",
        "3.1.3调试状态",
    ),
    "10": ("外部型号+产品名称", "XXXX年XX月XX日", "产品型号-XXXX"),
    "16": ('本章应分为以下几条。适用时应包括用"警告"或"注意"所标志的安全提示，以及保密性考虑。',),
}


def _with_test_company(config: dict) -> dict:
    # shipped config.json 不再携带默认单位名称，测试时注入测试值
    if not config["project"]["company"]["content"].strip():
        config["project"]["company"]["content"] = "测试单位"
    return config


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_end_to_end_fill(skill_id, tmp_path):
    eng = load_engine(skill_id)
    config = _with_test_company(config_data(skill_id))
    project = project_data(skill_id)
    plan = eng.loader.build_plan(config, project, eng.rules)

    doc = Document(str(template_path(skill_id)))
    eng.docx_ops.apply_plan(doc, plan)
    output = tmp_path / f"filled-{skill_id}.docx"
    doc.save(str(output))

    result = Document(str(output))
    text = _doc_all_text(result)
    assert config["project"]["name"]["content"] in text
    assert config["document"]["id"]["content"] in text
    assert config["document"]["title"]["content"] in text
    if skill_id == "08":
        assert config["document"]["title"]["content"] == "软件需求规格说明"
    for anchor in FORBIDDEN_ANCHORS.get(skill_id, ()):
        assert anchor not in text

    update_fields = result.settings.element.find(qn("w:updateFields"))
    assert update_fields is not None
    assert update_fields.get(qn("w:val")) == "true"

    bookmark_ids = [
        element.get(qn("w:id"))
        for element in result.element.body.iter(qn("w:bookmarkStart"))
    ]
    assert len(bookmark_ids) == len(set(bookmark_ids))
    paragraph_ids = [
        element.get(qn("w14:paraId"))
        for element in result.element.body.iter(qn("w:p"))
        if element.get(qn("w14:paraId")) is not None
    ]
    assert len(paragraph_ids) == len(set(paragraph_ids))


def _run_cli(skill_id, config_path, project_path, output_path) -> subprocess.CompletedProcess:
    scripts_dir = SKILL_DIRS[skill_id] / "scripts"
    return subprocess.run(
        [
            sys.executable,
            str(scripts_dir / "main.py"),
            "--template",
            str(template_path(skill_id)),
            "--config",
            str(config_path),
            "--project",
            str(project_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_cli_success(skill_id, tmp_path):
    output = tmp_path / f"cli-{skill_id}.docx"
    config = _with_test_company(config_data(skill_id))
    config_path = tmp_path / f"config-{skill_id}.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
    proc = _run_cli(
        skill_id,
        config_path,
        SKILL_DIRS[skill_id] / "templates" / "project.json",
        output,
    )
    assert proc.returncode == 0, proc.stderr
    assert output.exists()
    assert "文档已生成" in proc.stdout


@pytest.mark.parametrize("skill_id", SKILL_IDS)
def test_cli_data_error_exit_code(skill_id, tmp_path):
    broken_config = config_data(skill_id)
    del broken_config["project"]["name"]
    broken_path = tmp_path / "broken-config.json"
    broken_path.write_text(json.dumps(broken_config, ensure_ascii=False), encoding="utf-8")

    proc = _run_cli(
        skill_id,
        broken_path,
        SKILL_DIRS[skill_id] / "templates" / "project.json",
        tmp_path / "should-not-exist.docx",
    )
    assert proc.returncode == 1
    assert "数据校验失败" in proc.stderr
    assert "Traceback" not in proc.stderr
