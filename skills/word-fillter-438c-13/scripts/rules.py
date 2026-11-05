"""[13] 模板专属规则：封面/标识行替换与特殊规则，由共享引擎 loader.build_plan 读取。"""

from __future__ import annotations


# 图表编号后是否补空格（与原引擎副本行为一致；模板无空格时设为 False）
CAPTION_SPACE_BEFORE_REST = True


COVER = [
    ('cover.project_name', '外部型号+产品名称', lambda c: c['project_name'], 2),
    ('cover.document_title', '软件接口设计说明', lambda c: c['document_title'], 2),
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
    ('identity.project_name', '软件名称；', lambda c: f"软件名称：{c['project_name']}；", 1),
    ('identity.short_name', '软件缩写：', lambda c: f"软件缩写：{c['short_name']}", 1),
    ('identity.version', '软件版本号。', lambda c: f"软件版本号：{c['version']}。", 1),
]



PATTERN_OVERRIDES = {}


INSERTION_PARENT_RULES = {'3.2': {'parent_title': '3.x（接口的项目唯一标识符）',
         'summary_anchor': '本节（从3.2 开始编号）应通过项目唯一标识符标识接口',
         'end_before_title': '需求的可追踪性',
         'prototype_title_anchor': '3.x（接口的项目唯一标识符）',
         'prototype_body_anchor': '对于3.1 中所标识的每个接口',
         'cleanup_anchors': ('a．接口实体分配给接口的优先级别；',),
         'cleanup_to_end': True}}
