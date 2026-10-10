from __future__ import annotations


# 1.1 节标识行原文（全文全等匹配，替换格式见 loader.py 封面规则块）。
# 本模板五段标识行与 [10] 模板逐字一致。
IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


# 章节引导文字在模板中均唯一出现，无需子串锚定覆盖。
PATTERN_OVERRIDES: dict[str, str] = {}


# 本模板虽存在 "9.5.X 软件XX阶段评审情况" 等 X 占位标题（4.5 节），但该节
# 父标题与 X 占位标题之间没有任何摘要/引导段落，动态章节机制要求
# parent < summary < end_before 三者齐备，此处无法满足；且该原型是
# "三级标题 + 两个四级子标题" 的两级结构，单原型动态克隆无法复现。
# 故 4.5/4.6 节均改用静态段落规则处理（见 project.json），此字典保持为空。
INSERTION_PARENT_RULES: dict[str, dict] = {}
