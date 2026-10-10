from __future__ import annotations


# [14] 软件可靠性和可维护性设计 模板的标识行锚点（1.1 标识，逐字取自模板正文）。
# 注意：本模板的"软件名称"行原文没有冒号、以分号结尾（"软件名称；"），
# 系模板原文如此，锚点必须逐字一致。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称；",
    "short_name": "软件缩写：",
    "version": "软件版本号。",
}


# 各 placeholder 的 replacement_pattern 在模板中均只出现 1 次，无需子串锚定覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# [14] 模板无 X 占位原型子节，不支持动态章节。
INSERTION_PARENT_RULES: dict[str, dict] = {}
