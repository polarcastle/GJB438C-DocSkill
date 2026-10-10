from __future__ import annotations


IDENTITY_LINE_ANCHORS = {
    "document_id": '文档标识号：TN/x-DO-DS-V{N.xx}；',
    "title": '标题：；',
    "project_name": '软件名称；',
    "short_name": '软件缩写：',
    "version": '软件版本号。',
}


PATTERN_OVERRIDES: dict[str, str] = {}


INSERTION_PARENT_RULES = {
    "3.2": {
        "parent_title": '3.x（接口的项目唯一标识符）',
        "summary_anchor": '本节（从3.2 开始编号）应通过项目唯一标识符标识接口',
        "end_before_title": '需求的可追踪性',
        "prototype_title_anchor": '3.x（接口的项目唯一标识符）',
        "prototype_body_anchor": '对于3.1 中所标识的每个接口',
        "cleanup_anchors": (
            'a．接口实体分配给接口的优先级别；',
        ),
        "cleanup_to_end": True,
    },
}
