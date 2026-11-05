"""[29] 模板专属规则：封面/标识行替换与特殊规则，由共享引擎 loader.build_plan 读取。"""

from __future__ import annotations


# 图表编号后是否补空格（与原引擎副本行为一致；模板无空格时设为 False）
CAPTION_SPACE_BEFORE_REST = True


COVER = [
    ('cover.project_name', '外部型号+产品名称', lambda c: c['project_name'], 2),
    ('cover.document_title', '软件技术总结报告', lambda c: c['document_title'], 2),
    ('cover.short_name', '产品型号-XXXX', lambda c: f"产品型号-{c['short_name']}", 2),
    ('cover.company', 'XXXXXXXXXX', lambda c: c['company'], 1),
    ('cover.date', 'XXXX年XX月XX日', lambda c: c['document_date'], 1),
    ('cover.classification', '密  级： 内部', lambda c: f"密  级： {c['classification']}", 1),
    ('cover.phase', '阶  段：     ', lambda c: f"阶  段： {c['phase']}", 1),
    ('cover.version', '版  次： A 版', lambda c: f"版  次： {c['version']}", 1),
]


IDENTITY = [
]



PATTERN_OVERRIDES = {}


INSERTION_PARENT_RULES = {}
