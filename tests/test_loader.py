from __future__ import annotations

import pytest

from conftest import SKILL_IDS, load_engine, minimal_config


def _table_section(**table_overrides) -> dict:
    table = {
        "table_id": "T1",
        "data_start_row": 1,
        "preserve_tail_rows": 0,
        "locator_rows": [["名称", "说明"]],
        "columns": ["c1", "c2"],
        "rows": [{"c1": "a", "c2": "b"}],
    }
    table.update(table_overrides)
    return {"structure": {"3": {"tables": [table]}}}


@pytest.mark.parametrize("skill_id", SKILL_IDS)
class TestBuildPlanCommon:
    def test_minimal_config_builds_plan(self, skill_id):
        eng = load_engine(skill_id)
        plan = eng.loader.build_plan(minimal_config(), {"structure": {}})
        expected = {"08": 13, "10": 13}.get(skill_id)
        if expected is None:
            assert len(plan.exact_replacements) >= 1
        else:
            assert len(plan.exact_replacements) == expected
        assert plan.paragraph_replacements == ()
        assert plan.tables == ()

    def test_missing_required_field(self, skill_id):
        eng = load_engine(skill_id)
        config = minimal_config()
        del config["project"]["name"]
        with pytest.raises(eng.errors.StrictDataError, match=r"project\.name"):
            eng.loader.build_plan(config, {"structure": {}})

    def test_blank_content_rejected(self, skill_id):
        eng = load_engine(skill_id)
        config = minimal_config()
        config["document"]["date"]["content"] = "   "
        with pytest.raises(eng.errors.StrictDataError, match="字段为空"):
            eng.loader.build_plan(config, {"structure": {}})

    def test_missing_structure_rejected(self, skill_id):
        eng = load_engine(skill_id)
        with pytest.raises(eng.errors.StrictDataError, match="structure"):
            eng.loader.build_plan(minimal_config(), {})

    def test_subsections_sorted_numerically(self, skill_id):
        eng = load_engine(skill_id)
        section_id = "99"
        while section_id in eng.template_rules.INSERTION_PARENT_RULES:
            section_id = str(int(section_id) + 1)
        project = {
            "structure": {
                section_id: {
                    "subsections": {
                        f"{section_id}.10": {"replacement_pattern": "锚点十", "content": "十"},
                        f"{section_id}.2": {"replacement_pattern": "锚点二", "content": "二"},
                    }
                }
            }
        }
        plan = eng.loader.build_plan(minimal_config(), project)
        assert [rule.key for rule in plan.paragraph_replacements] == [f"{section_id}.2", f"{section_id}.10"]

    def test_table_duplicate_columns_rejected(self, skill_id):
        eng = load_engine(skill_id)
        with pytest.raises(eng.errors.StrictDataError, match="不能重复"):
            eng.loader.build_plan(minimal_config(), _table_section(columns=["c1", "c1"]))

    def test_table_row_keys_must_match_columns(self, skill_id):
        eng = load_engine(skill_id)
        with pytest.raises(eng.errors.StrictDataError, match="字段必须严格等于"):
            eng.loader.build_plan(minimal_config(), _table_section(rows=[{"c1": "a"}]))

    def test_table_negative_row_params_rejected(self, skill_id):
        eng = load_engine(skill_id)
        with pytest.raises(eng.errors.StrictDataError, match="不能为负数"):
            eng.loader.build_plan(minimal_config(), _table_section(data_start_row=-1))

    def test_table_missing_locator_rows_rejected(self, skill_id):
        eng = load_engine(skill_id)
        section = _table_section()
        del section["structure"]["3"]["tables"][0]["locator_rows"]
        with pytest.raises(eng.errors.StrictDataError, match="locator_rows"):
            eng.loader.build_plan(minimal_config(), section)

    def test_table_rules_parsed(self, skill_id):
        eng = load_engine(skill_id)
        plan = eng.loader.build_plan(minimal_config(), _table_section())
        assert len(plan.tables) == 1
        rule = plan.tables[0]
        assert rule.key == "3.T1"
        assert rule.columns == ("c1", "c2")
        assert rule.rows == (("a", "b"),)


class TestBuildPlan08:
    def test_dynamic_section_rule(self):
        eng = load_engine("08")
        project = {
            "structure": {
                "3": {
                    "placeholders": [
                        {
                            "id": "3.2",
                            "content": "能力总述",
                            "subsections": {
                                "3.2.2": {"name": "能力乙", "content": "乙说明"},
                                "3.2.1": {"name": "能力甲", "content": "甲说明"},
                            },
                        }
                    ]
                }
            }
        }
        plan = eng.loader.build_plan(minimal_config(), project)
        assert len(plan.dynamic_sections) == 1
        rule = plan.dynamic_sections[0]
        assert rule.parent_id == "3.2"
        assert [item.section_id for item in rule.items] == ["3.2.1", "3.2.2"]
        assert any(r.key == "3.2.summary" for r in plan.paragraph_replacements)

    def test_dynamic_section_missing_subsections_rejected(self):
        eng = load_engine("08")
        project = {"structure": {"3": {"placeholders": [{"id": "3.2", "content": "能力总述"}]}}}
        with pytest.raises(eng.errors.StrictDataError, match="缺少 subsections"):
            eng.loader.build_plan(minimal_config(), project)


class TestBuildPlan10:
    def _csci_item(self) -> dict:
        return {
            "title": "核心子系统",
            "overview": "概述",
            "component_title": "核心部件",
            "component_design": "部件设计",
            "execution_plan": "执行方案",
            "interface_overview": "接口概述",
            "interface_identification": "接口标识",
            "interface_detail_title": "接口一",
            "interface_details": "接口详情",
        }

    def test_csci_rule_parsed(self):
        eng = load_engine("10")
        project = {"structure": {"4": {"cscis": [self._csci_item(), self._csci_item()]}}}
        plan = eng.loader.build_plan(minimal_config(), project)
        assert len(plan.csci_sections) == 1
        items = plan.csci_sections[0].items
        assert [item.section_id for item in items] == ["4.1", "4.2"]

    def test_csci_missing_field_rejected(self):
        eng = load_engine("10")
        item = self._csci_item()
        del item["overview"]
        project = {"structure": {"4": {"cscis": [item]}}}
        with pytest.raises(eng.errors.StrictDataError, match="字段为空|缺少必填字段"):
            eng.loader.build_plan(minimal_config(), project)

    def test_csci_empty_list_rejected(self):
        eng = load_engine("10")
        project = {"structure": {"4": {"cscis": []}}}
        with pytest.raises(eng.errors.StrictDataError, match="非空数组"):
            eng.loader.build_plan(minimal_config(), project)
