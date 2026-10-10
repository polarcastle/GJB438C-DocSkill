from __future__ import annotations


# [28] 研制总结报告模板 1.1 标识节中的标识行原文（逐字取自转换后 docx）。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


# 各 placeholder 的 replacement_pattern 在模板中均只出现 1 次，无需覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# [28] 模板无 X 编号占位原型子节，不启用动态章节。
INSERTION_PARENT_RULES: dict[str, dict] = {}
