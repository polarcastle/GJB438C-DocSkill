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
    "4.X": {
        "parent_title": "软件测试环境",
        "summary_anchor": "本章应分为如下小条描述每个预期测试现场",
        "end_before_title": "测试标识",
        "prototype_title_anchor": "4.X(测试现场名称)",
        "prototype_body_anchor": "注：若只有一个测试现场",
        "cleanup_anchors": (
            "注：若只有一个测试现场",
        ),
        "cleanup_to_end": True,
    },
}
