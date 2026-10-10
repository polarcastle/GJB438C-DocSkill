from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称；",
    "short_name": "软件缩写：",
    "version": "软件版本号。",
}


PATTERN_OVERRIDES: dict[str, str] = {}


INSERTION_PARENT_RULES: dict[str, dict] = {
    "4": {
        "parent_title": "数据库详细设计",
        "summary_anchor": "本章应根据需要分条描述数据库的详细设计。",
        "end_before_title": "用于数据库访问或操纵的软件单元详细设计",
        "prototype_title_anchor": "X（数据库设计级别的名称）",
        "prototype_body_anchor": "本条应标识数据库设计级别",
        "cleanup_anchors": (
            "a)数据库设计中各个数据元素的特征",
        ),
        "cleanup_to_end": True,
    },
    "5": {
        "parent_title": "用于数据库访问或操纵的软件单元详细设计",
        "summary_anchor": "本章应分为以下子条描述用于数据库访问或操纵的软件单元。",
        "end_before_title": "需求可追踪性",
        "prototype_title_anchor": "X（软件单元的唯一标识符，或者一组软件单元的标志符）",
        "prototype_body_anchor": "本条应该通过唯一标识符来标识软件单元",
        "cleanup_anchors": (
            "（若有）单元设计决策",
        ),
        "cleanup_to_end": True,
    },
}
