from __future__ import annotations

# [29] 技术总结报告模板为纯标题骨架：正文各章只有标题、没有任何
# "本条应……"类指导文字段落，也没有封面标识行（文档标识号/标题/软件名称等），
# 因此标识行与动态章节（X 占位原型子节）规则均为空。
# 模板中唯一的 X 占位是标题 "3.2.X 行为设计"，按占位标题改名处理
# （见 templates/project.json 中 3.2 节的 placeholders）。

IDENTITY_LINE_ANCHORS: dict[str, str] = {}


PATTERN_OVERRIDES: dict[str, str] = {}


INSERTION_PARENT_RULES: dict[str, dict] = {}
