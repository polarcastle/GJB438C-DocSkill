"""[12] 模板专属规则：封面/标识行替换与特殊规则，由共享引擎 loader.build_plan 读取。"""

from __future__ import annotations


# 图表编号后是否补空格（与原引擎副本行为一致；模板无空格时设为 False）
CAPTION_SPACE_BEFORE_REST = True


COVER = [
    ('cover.project_name', 'ＸＸＸＸＸ', lambda c: c['project_name'], 2),
    ('cover.project_name_inner', 'ＸＸＸＸＸＸ', lambda c: c['project_name'], 1),
    ('cover.document_title', '软件详细设计说明', lambda c: c['document_title'], 3),
    ('cover.company', 'XXXXXXXXXX', lambda c: c['company'], 2),
    ('cover.date', 'XXXX年XX月XX日', lambda c: c['document_date'], 2),
    ('cover.revision_date', '[修订日期: 2010-XX-XX]', lambda c: f"[修订日期: {c['document_date']}]", 2),
    ('cover.document_id', '[文档标识号: TN/x-DO-DS-V{N.xx}]', lambda c: f"[文档标识号: {c['document_id']}]", 2),
    ('cover.classification', '密级：', lambda c: f"密级：{c['classification']}", 1),
]


IDENTITY = [
    ('identity.document_id', '文档标识号：TN/x-DO-DS-V{N.xx}；', lambda c: f"文档标识号：{c['document_id']}；", 1),
    ('identity.title', '标题：；', lambda c: f"标题：{c['document_title']}；", 1),
    ('identity.project_name', '软件名称：；', lambda c: f"软件名称：{c['project_name']}；", 1),
    ('identity.short_name', '软件缩写：；', lambda c: f"软件缩写：{c['short_name']}；", 1),
    ('identity.version', '软件版本号：。', lambda c: f"软件版本号：{c['version']}。", 1),
]



PATTERN_OVERRIDES = {}


INSERTION_PARENT_RULES = {'3': {'parent_title': '详细设计',
       'summary_anchor': '本条应通过项目唯一的标识符来标识软件单元，并对该单元进行说明。',
       'end_before_title': '需求可追踪性',
       'prototype_title_anchor': '3.X (软件单元的项目唯一的标识符，或者一组软件单元的标志符)',
       'prototype_body_anchor': 'a)(若有)单元设计决策',
       'cleanup_anchors': ('b)该软件单元设计中的任何约束',),
       'cleanup_to_end': True}}
