from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


PATTERN_OVERRIDES: dict[str, str] = {}


# [19] 软件测试报告的章节标题采用 Word 自动多级编号（标题样式绑定 numId 3），
# 正文中原有的 "4.X" / "4.X.2.Y" 等是原型标题里的字面 instructional 文字。
# 动态章节机制（apply_dynamic_section）会把条目编号直接写进标题文本，
# 对本模板会造成 "4.1 4.1功能测试" 式的双重编号，因此本 skill 不配置动态章节。
# 第 4 章的 X 占位原型块按静态方式填写：整段替换标题文本（剥掉字面 "4.X" 编号），
# 由自动编号生成真实条号。INSERTION_PARENT_RULES 保持为空。
INSERTION_PARENT_RULES: dict[str, dict] = {}
