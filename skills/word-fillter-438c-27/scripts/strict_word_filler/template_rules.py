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
    "5": {
        "parent_title": "软件标准化工作情况",
        "summary_anchor": "本章应逐项说明在保证软件标准化方面所开展的各项工作及其完成情况，包括各阶段的标准化分析、标准确定、标准化保证以及标准化审查等。",
        "end_before_title": "标准化要求实施情况",
        "prototype_title_anchor": "5.X 阶段1",
        "prototype_body_anchor": "描述在软件设计和开发方面开展的标准化工作。",
        "cleanup_anchors": (
            "5.X.1标准化分析",
            "5.X.2标准化确定",
            "5.X.3标准化保证",
            "5.X.4标准化审查",
        ),
        "cleanup_to_end": True,
    },
}
