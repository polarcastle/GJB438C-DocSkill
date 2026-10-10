---
name: word-fillter-438C-09
description: "当用户提到「按照438C模板填写word文档」「接口需求」「接口需求规格说明」「IRS」「Interface Requirements Specification」「438C」时触发。交互式填写 GJB 438C [09] 接口需求规格说明书模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[09]接口需求规格说明-438C.docx` 模板生成或修改 GJB 438C 接口需求规格说明书（IRS）时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[09]接口需求规格说明-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、动态接口子条和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、接口实体、合格性方法等）
- `references/style-rules.md`：句式与表达规范（假设句式、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API（路由、函数签名、协议、端口、消息格式）、关键类与函数、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的接口名、数据元素名、功能描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1 标识五要素行由 config 自动填写，1.1 content 概述标识信息）
   - 第 2 章（引用文档）改写章引言并填写 `tables`（引用文件表）
   - 第 3 章（需求）中 3.1 为**动态章节**：placeholder 级 `content` 写接口标识和接口图引言，`subsections` 每个子条写一个接口（a.～g. 特性）；随后改写"需求的优先顺序和关键性"标题（id `3.4`）及其正文（id `3.4.1`）
   - 第 4 章（合格性规定）改写章引言及 a.～e. 五个方法占位符（4.1～4.5）
   - 第 5 章（需求可追踪性）改写章引言及 a./b. 两个占位符（5.1、5.2）
   - 第 6 章（注解）为术语和缩略语
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：假设句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——接口是否有项目唯一标识符、数据元素量化指标是否齐全、对外部实体是否用"当……时，本软件应……"假设句式、无内容的项是否如实写"无"、增删接口后 id `3.4` 标题编号是否同步、章节号引用是否真实存在、接口与数据元素描述是否与第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

| 字段位置 | type | 说明 | content 生成方式 |
|----------|------|------|-----------------|
| project.* | `original_text` | 项目基础信息（名称、版本、单位等） | 直接使用用户输入 |
| document.* | `original_text` | 文档元信息（编号、标题、日期等） | 直接使用用户输入 |
| content.overview | `background_information` | 项目概述 | 结合用户描述生成 |
| content.scope | `background_information` | 项目范围 | 结合用户描述生成 |
| content.features | `background_information` | 功能特性 | 结合用户描述生成 |

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 用户需求生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入 |

### 章节结构类型

**静态章节**（无 subsections）：
```json
{
  "id": "1.2",
  "name": "系统概述",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**动态章节**（3.1 接口标识和接口图，有 subsections）：
```json
{
  "id": "3.1",
  "name": "接口标识和接口图",
  "type": "content_generation",
  "generation_prompt": "生成子章节的提示...",
  "content": "string（本节引言）",
  "subsections": {
    "3.2": { "name": "任务数据接口", "content": "string" },
    "3.3": { "name": "状态反馈接口", "content": "string" }
  }
}
```

> **动态章节的机制约束（重要，涉及 3.1）**
> 引擎将 3.1 视为动态章节：`subsections` 中每个子条的 `name` 会作为二级标题写入文档（标题形如"3.2任务数据接口"，编号与名称之间无空格）、`content` 作为正文段落，且 `subsections` **不允许为空**（空则报错）。
> 当软件实际只有一个接口时，**禁止为填满机制而编造多个接口**：只建一个子条（`3.2`），`name` 如实命名，`content` 首句标识该接口的项目唯一标识符。详见 `references/writing-guide.md`「3.1 接口标识和接口图」。
> 子条中的 `replacement_pattern` 字段在动态模式下被引擎静默忽略，无需填写；子条 `name` 应以中文开头，避免标题出现"3.2REST……"这类数字与英文连排无空格的观感问题。
> **编号联动**：子条数量决定"需求的优先顺序和关键性"的章节号。示例配置 2 个接口，标题占位符（id `3.4`）写为"3.4 需求的优先顺序和关键性"；增删接口子条时，必须同步改写 id `3.4` 的 content（N 个接口时为 3.{N+2}），否则文档章节号不连续。

**表格填充**（第 2 章引用文件表）：
```json
{
  "id": "2",
  "tables": [{
    "table_id": "reference_documents",
    "locator_rows": [["序号", "名称", "版本", "发布日期", "来源"]],
    "data_start_row": 1,
    "preserve_tail_rows": 0,
    "columns": ["number", "name", "version", "release_date", "source"],
    "rows": [
      { "number": "1", "name": "...", "version": "...", "release_date": "...", "source": "..." }
    ]
  }]
}
```

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`；动态章节（3.1）placeholder 级的 `content` 为该节引言，同样只修改 `content`
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 动态章节 `subsections` 中每个子条的 `name` **会作为章节标题写入文档，必须改为实际接口名**（以中文开头）；`content` 为该接口正文（按 a.～g. 分行）；子条中的 `replacement_pattern` 被引擎静默忽略，无需填写
4. `subsections` 的 key 必须是有效章节编号（如 `"3.2"`），从 3.2 开始连续编号
5. `rows` 中每行的字段必须严格等于 `columns` 定义

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。
> 其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符。
>
> 修改后会导致报错 `期望命中 1 张表，实际 0 张`。
>
> 若不确定实际表头文本，用以下脚本提取：
> ```python
> from docx import Document
> doc = Document("模板文件.docx")
> for i, table in enumerate(doc.tables):
>     for j, row in enumerate(table.rows[:3]):
>         print(f"Table {i} Row {j}: {[c.text.strip() for c in row.cells]}")
> ```

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[09]接口需求规格说明-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[09]接口需求规格说明-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
