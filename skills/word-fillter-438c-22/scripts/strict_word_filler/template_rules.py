from __future__ import annotations


# [22] 测试问题报告模板 1.1 标识节的五行标识原文（逐字取自模板 docx）：
# 注意本模板"软件名称；"行无冒号、"软件缩写："行无收尾标点，锚点必须逐字一致。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称；",
    "short_name": "软件缩写：",
    "version": "软件版本号。",
}


# 本模板正文无"本章应/本条应"指导段落，所有正文段落均唯一，无需覆盖锚点。
PATTERN_OVERRIDES: dict[str, str] = {}


# 本模板无 X 占位原型子节（如 3.2.X），不支持动态章节。
INSERTION_PARENT_RULES: dict[str, dict] = {}
