from __future__ import annotations


# [05]软件标准化大纲-438C 的 1.1 节标识行原文（逐字摘自模板 docx）。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


# 本模板各 placeholder 的 replacement_pattern 均为整段原文，全文唯一，
# 无需子串锚定或命中数覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# 本模板无 X 编号占位原型子节（3.2.X 之类），不启用动态章节。
INSERTION_PARENT_RULES: dict[str, dict] = {}
