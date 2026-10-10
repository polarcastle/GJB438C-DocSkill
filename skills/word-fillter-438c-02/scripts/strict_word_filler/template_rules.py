from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


# 本模板的指导文字均唯一（重复条目已在 project.json 中如实标注并跳过），
# 故无需覆盖子串锚点；若后续发现某 replacement_pattern 在模板中出现多次，
# 可在此为该章节 id 改写为可唯一命中的锚点子串。
PATTERN_OVERRIDES: dict[str, str] = {}


# [02] 软件开发计划模板不含 "X.X.X" 形式的占位原型子节，
# 不支持动态章节插入，必须保持为空 dict。
INSERTION_PARENT_RULES: dict[str, dict] = {}
