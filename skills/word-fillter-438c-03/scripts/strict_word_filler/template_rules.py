from __future__ import annotations


# [03] 软件配置管理计划模板的标识行锚点（1.1 标识节）。
# 注意：本模板“软件名称”行原文为“软件名称；”（分号前无冒号，为模板原文），
# 替换时由 loader 补全为“软件名称：<名称>；”格式。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称；",
    "short_name": "软件缩写：",
    "version": "软件版本号。",
}


# 本模板所有章节的 replacement_pattern 在全文均只出现 1 次，无需子串锚定覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# [03] 模板不存在 X 占位原型子节（如“3.2.X（软件能力）”），无动态章节。
INSERTION_PARENT_RULES: dict[str, dict] = {}
