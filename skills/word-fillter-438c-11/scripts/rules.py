"""[11] 模板专属规则：封面/标识行替换与特殊规则，由共享引擎 loader.build_plan 读取。"""

from __future__ import annotations


# 图表编号后是否补空格（与原引擎副本行为一致；模板无空格时设为 False）
CAPTION_SPACE_BEFORE_REST = True


COVER = [
    ('cover.project_name', '外部型号+产品名称', lambda c: c['project_name'], 2),
    ('cover.document_title', '数据库设计说明', lambda c: c['document_title'], 2),
    ('cover.short_name', '  产品型号-XXXX', lambda c: f"  产品型号-{c['short_name']}", 1),
    ('cover.short_name_tail', '产品型号-XXXX', lambda c: f"产品型号-{c['short_name']}", 1),
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
    ('identity.short_name', '软件缩写：', lambda c: f"软件缩写：{c['short_name']}；", 1),
    ('identity.version', '软件版本号。', lambda c: f"软件版本号：{c['version']}。", 1),
]



PATTERN_OVERRIDES = {}


INSERTION_PARENT_RULES = {'4': {'parent_title': '数据库详细设计',
       'summary_anchor': '本章应根据需要分条描述数据库的详细设计。',
       'end_before_title': '用于数据库访问或操纵的软件单元详细设计',
       'prototype_title_anchor': 'X（数据库设计级别的名称）',
       'prototype_body_anchor': '本条应标识数据库设计级别',
       'cleanup_anchors': ('a)数据库设计中各个数据元素的特征',),
       'cleanup_to_end': True},
 '5': {'parent_title': '用于数据库访问或操纵的软件单元详细设计',
       'summary_anchor': '本章应分为以下子条描述用于数据库访问或操纵的软件单元。',
       'end_before_title': '需求可追踪性',
       'prototype_title_anchor': 'X（软件单元的唯一标识符，或者一组软件单元的标志符）',
       'prototype_body_anchor': '本条应该通过唯一标识符来标识软件单元',
       'cleanup_anchors': ('（若有）单元设计决策',),
       'cleanup_to_end': True}}
