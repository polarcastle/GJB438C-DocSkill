"""[08] 软件需求规格说明：模板专属规则（由共享引擎 loader.build_plan 读取）。"""

from __future__ import annotations


# [08] 模板的图表占位为「表X-X需求…」（无空格），编号后保持原样不补空格。
CAPTION_SPACE_BEFORE_REST = False


IDENTITY_LINE_ANCHORS = {
    "document_id": "文档标识号：TN/x-DO-DS-V{N.xx}；",
    "title": "标题：",
    "project_name": "软件名称：",
    "short_name": "软件缩写：",
    "version": "软件版本号。",
}


COVER = [
    ("cover.project_name", "外部型号+产品名称", lambda c: c["project_name"], 2),
    ("cover.document_title", "软件需求规格说明", lambda c: c["document_title"], 2),
    ("cover.short_name", "产品型号-XXXX", lambda c: f"产品型号-{c['short_name']}", 2),
    ("cover.company", "XXXXXXXX公司", lambda c: c["company"], 1),
    ("cover.date", "XXXX年XX月XX日", lambda c: c["document_date"], 1),
    ("cover.classification", "密  级： 内部", lambda c: f"密  级： {c['classification']}", 1),
    ("cover.phase", "阶  段：     ", lambda c: f"阶  段： {c['phase']}", 1),
    ("cover.version", "版  次： A 版", lambda c: f"版  次： {c['version']}", 1),
]


IDENTITY = [
    ("identity.document_id", IDENTITY_LINE_ANCHORS["document_id"], lambda c: f"文档标识号：{c['document_id']}；", 1),
    ("identity.title", IDENTITY_LINE_ANCHORS["title"], lambda c: f"标题：{c['document_title']}", 1),
    ("identity.project_name", IDENTITY_LINE_ANCHORS["project_name"], lambda c: f"软件名称：{c['project_name']}", 1),
    ("identity.short_name", IDENTITY_LINE_ANCHORS["short_name"], lambda c: f"软件缩写：{c['short_name']}", 1),
    ("identity.version", IDENTITY_LINE_ANCHORS["version"], lambda c: f"软件版本号：{c['version']}。", 1),
]


PATTERN_OVERRIDES = {
    "1.2": "本条应概述本文档所适用软件的用途。它还应描述软件的一般特性，概述系统开发、运行和维护的历史；标识项目的需方、用户、开发方和保障机构等；标识当前和计划的运行现场；列出其他有关文档。",
    "5": "本章应描述",
}


INSERTION_PARENT_RULES = {
    "3.1": {
        "parent_title": "要求的状态和方式",
        "summary_anchor": "如果要求软件在多种状态或方式下运行，并且不同的状态或方式具有不同的需求，则应标识和定义每一状态和方式。",
        "end_before_title": "软件能力需求",
        "prototype_title_anchor": "3.10.1计算机硬件需求",
        "prototype_body_anchor": "本条应描述针对本软件必须使用的计算机硬件的需求（若有）。",
        "cleanup_anchors": (),
        "cleanup_to_end": False,
    },
    "3.2": {
        "parent_title": "软件能力需求",
        "summary_anchor": "为详细说明与软件各个能力相关的需求，本条可分为若干子条。",
        "end_before_title": "软件外部接口需求",
        "prototype_title_anchor": "3.10.1计算机硬件需求",
        "prototype_body_anchor": "本条应描述针对本软件必须使用的计算机硬件的需求（若有）。",
        "cleanup_anchors": ("3.2.X（软件能力）",),
        "cleanup_to_end": True,
    },
    "3.3": {
        "parent_title": "软件外部接口需求",
        "summary_anchor": "本条可分为若干个小条来规定关于软件的外部接口的需求（若有）。",
        "end_before_title": "软件内部接口需求",
        "prototype_title_anchor": "3.10.1计算机硬件需求",
        "prototype_body_anchor": "本条应描述针对本软件必须使用的计算机硬件的需求（若有）。",
        "cleanup_anchors": (
            "接口标识和接口图",
            "本条应标识所需要的软件外部接口（即，与涉及共享、提供或交换数据的其他实体的关系）。",
        ),
        "cleanup_to_end": True,
    },
    "3.4": {
        "parent_title": "软件内部接口需求",
        "summary_anchor": "本条应描述施加于软件内部接口的需求（若有）。",
        "end_before_title": "软件内部数据需求",
        "prototype_title_anchor": "3.10.1计算机硬件需求",
        "prototype_body_anchor": "本条应描述针对本软件必须使用的计算机硬件的需求（若有）。",
        "cleanup_anchors": (),
        "cleanup_to_end": False,
    },
}
