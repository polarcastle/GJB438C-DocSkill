from __future__ import annotations


# [30] 软件安全性设计模板 1.1 标识节的标识行锚点（逐字取自模板 docx）。
# 注意：本模板"软件名称；"行原文无冒号（模板排版如此），锚点须逐字保留。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称；",
    "short_name": "软件缩写：",
    "version": "软件版本号。",
}


# [30] 模板的章节锚点均为全文唯一，无需子串覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# [30] 模板不含 "3.2.X（软件能力）" 类 X 编号原型子节，无动态章节。
INSERTION_PARENT_RULES: dict[str, dict] = {}
