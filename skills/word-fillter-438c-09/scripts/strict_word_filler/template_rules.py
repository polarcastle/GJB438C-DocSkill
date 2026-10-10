from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：；",
    "project_name": "软件名称：；",
    "short_name": "软件缩写：；",
    "version": "软件版本号：。",
}


PATTERN_OVERRIDES: dict[str, str] = {}


INSERTION_PARENT_RULES = {
    "3.1": {
        "parent_title": "需求",
        "summary_anchor": "对3.1 节中标识的每一个接口，本节应包含项目唯一标识符",
        "end_before_title": "3.y 需求的优先顺序和关键性",
        "prototype_title_anchor": "3.x （接口的项目唯一标识符）",
        "prototype_body_anchor": "本节（从3.2 开始）通过项目唯一标识符来标识接口",
        "cleanup_anchors": (
            "本节（从3.2 开始）通过项目唯一标识符来标识接口",
        ),
        "cleanup_to_end": True,
    },
}
