from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


PATTERN_OVERRIDES: dict[str, str] = {}


# [12] 模板第 3 章「详细设计」的原型块结构（与 [08] 不同）：
#   3.X (软件单元的项目唯一的标识符...)   <- 原型标题（Heading 2），位于引言段之前
#   本条应通过项目唯一的标识符来标识软件单元...  <- 原型正文（段38，作为 summary 保留）
#   a)(若有)单元设计决策...  b)...  c)...  f)... 1)~5) 等指导文字（删除）
# 适配方案：
#   - 段37（原型标题）由 project.json 第 3 章章节级规则替换为首个软件单元标题
#     "3.1 <名称>（SU-01）"（Heading 2 样式正确），不进删除集；
#   - 段38（原型正文）作为 summary_anchor 承载 3.1 单元正文；
#   - 动态子节从 3.2 开始，由引擎克隆原型标题/原型正文样式插入；
#   - cleanup_to_end 从段39（a）项指导文字）删到「需求可追踪性」之前。
INSERTION_PARENT_RULES = {
    "3": {
        "parent_title": "详细设计",
        "summary_anchor": "本条应通过项目唯一的标识符来标识软件单元，并对该单元进行说明。",
        "end_before_title": "需求可追踪性",
        "prototype_title_anchor": "3.X (软件单元的项目唯一的标识符，或者一组软件单元的标志符)",
        "prototype_body_anchor": "a)(若有)单元设计决策",
        "cleanup_anchors": (
            "b)该软件单元设计中的任何约束",
        ),
        "cleanup_to_end": True,
    },
}
