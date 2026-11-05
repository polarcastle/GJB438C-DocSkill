"""[27] 模板专属规则：封面/标识行替换与特殊规则，由共享引擎 loader.build_plan 读取。"""

from __future__ import annotations


# 图表编号后是否补空格（与原引擎副本行为一致；模板无空格时设为 False）
CAPTION_SPACE_BEFORE_REST = True


COVER = [
    ('cover.project_name', '外部型号+产品名称', lambda c: c['project_name'], 2),
    ('cover.document_title', '软件标准化工作报告', lambda c: c['document_title'], 2),
    ('cover.short_name', '产品型号-XXXX', lambda c: f"产品型号-{c['short_name']}", 2),
    ('cover.company', 'XXXXXXXXXX', lambda c: c['company'], 1),
    ('cover.date', 'XXXX年XX月XX日', lambda c: c['document_date'], 1),
    ('cover.classification', '密  级： 内部', lambda c: f"密  级： {c['classification']}", 1),
    ('cover.phase', '阶  段：     ', lambda c: f"阶  段： {c['phase']}", 1),
    ('cover.version', '版  次： A 版', lambda c: f"版  次： {c['version']}", 1),
]


IDENTITY = [
    ('identity.document_id', '文档标识号：TN/x-DO-DS-V{N.xx}；', lambda c: f"文档标识号：{c['document_id']}；", 1),
    ('identity.title', '标题：；', lambda c: f"标题：{c['document_title']}；", 1),
    ('identity.project_name', '软件名称：；', lambda c: f"软件名称：{c['project_name']}；", 1),
    ('identity.short_name', '软件缩写：；', lambda c: f"软件缩写：{c['short_name']}；", 1),
    ('identity.version', '软件版本号：。', lambda c: f"软件版本号：{c['version']}。", 1),
]



PATTERN_OVERRIDES = {}


INSERTION_PARENT_RULES = {'5': {'parent_title': '软件标准化工作情况',
       'summary_anchor': '本章应逐项说明在保证软件标准化方面所开展的各项工作及其完成情况，包括各阶段的标准化分析、标准确定、标准化保证以及标准化审查等。',
       'end_before_title': '标准化要求实施情况',
       'prototype_title_anchor': '5.X 阶段1',
       'prototype_body_anchor': '描述在软件设计和开发方面开展的标准化工作。',
       'cleanup_anchors': ('5.X.1标准化分析', '5.X.2标准化确定', '5.X.3标准化保证', '5.X.4标准化审查'),
       'cleanup_to_end': True}}
