from __future__ import annotations


# [17] 软件测试记录-438C 标识行原文（正文缩进段落 a）～e））。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


# [17] 模板各 placeholder 的锚点在正文中均唯一出现，无需覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# [17] 模板没有可被动态章节机制克隆的 X 占位原型子节
# （4.1.X/4.1.Y 行为静态原型段落，4.2 下 3 个相同标题由 loader 封面规则块统一置空）。
INSERTION_PARENT_RULES: dict[str, dict] = {}
