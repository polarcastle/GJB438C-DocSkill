from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


PATTERN_OVERRIDES: dict[str, str] = {}


# [16] 软件测试说明模板的第 3 章（测试准备）与第 4 章（测试说明）虽然带有
# "3.X(测试的项目唯一的标识符)"、"4.X.Y(测试用例的项目唯一的标识符)" 等
# X 占位原型标题，但两章的引言段（"本章应分为以下几条。适用时应包括用……"）
# 在模板中逐字重复出现 2 次，动态章节机制要求的 summary/prototype/cleanup
# 锚点均无法唯一命中（find_single_body_paragraph 要求恰好 1 个匹配）。
# 因此本模板不配置动态章节，第 3/4 章按"就地改名 + 逐段替换"的静态方式填写
# （见 templates/project.json 中第 3/4 章的 placeholders）。
INSERTION_PARENT_RULES: dict[str, dict] = {}
