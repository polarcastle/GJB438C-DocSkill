---
name: word-fillter-438C-06
description: "当用户提到「按照438C模板填写word文档」「可靠性和可维护性大纲」「可维护性大纲」「可靠性大纲」「RAM大纲」「R&M大纲」「438C」时触发。交互式填写 GJB 438C [06] 软件可靠性和可维护性大纲模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[06]可靠性和可维护性大纲-438C.docx` 模板生成或修改 GJB 438C 软件可靠性和可维护性大纲时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构
- 本模板正文内嵌标准通用要求描述（3.1、4.1、4.2 各条），为**固定文本**，必须原样保留，禁止作为 placeholder 替换

# 目录结构

- `documents/[06]可靠性和可维护性大纲-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节可填写段内容与引用文件表数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷，含填写范围对照表）
- `references/terminology.md`：军用软件术语表（CSCI、MTBF、FMECA、可靠度等）
- `references/style-rules.md`：句式与表达规范（要求句式、量化指标、如实陈述原则、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案、研制合同或软件开发计划文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的可靠性/可维护性目标、组织职责、评审安排作为补充素材；
   - 写入规则：文档中的模块名、指标、活动安排必须与素材事实一致，禁止编造项目中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息（1.1 标识五行由本配置精确替换填写）。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 2 章（引用文档）使用 `tables` 填写引用文件表
   - 3.2（软件生存周期可靠性和可维护性度量方法）使用 `placeholders`，替换总述段为本项目各阶段度量方法
   - 第 4 章（软件可靠性和可维护性大纲要求）章首引言段，替换为本项目的大纲编制依据与组织实施说明
   - 3.1、4.1、4.2 各条为模板固定标准文本，不配置 placeholder
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录；随后按 `references/writing-guide.md` 第 1 章说明，在 Word 中为空白的 1.2 系统概述、1.3 文档概述两节补充内容（引擎无法向无锚点的空白节插入段落）。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：要求句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全、句式是否符合"应……"规范、固定文本是否原样未动、章节号引用是否真实存在、活动安排是否第 0 步素材事实一致。
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
| content.overview | `background_information` | 项目概述（兼作 1.2 系统概述写作素材） | 结合用户描述生成 |
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

**静态章节**（本模板全部章节均为静态，无动态子节）：
```json
{
  "id": "3.2",
  "name": "软件生存周期可靠性和可维护性度量方法",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**章首引言段**（第 4 章，replacement_pattern 位于章节顶层）：
```json
{
  "4": {
    "title": "软件可靠性和可维护性大纲要求",
    "replacement_pattern": "锚点文本...",
    "content": "string"
  }
}
```

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

1. 只修改 `content` 与 `rows`；不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
2. `rows` 中每行的字段必须严格等于 `columns` 定义
3. 本模板无 X 占位原型子节，**不支持 `subsections` 动态章节**；引擎会对固定文本段落（3.1、4.1、4.2 各条）保持原样，不要为这些段落配置 placeholder
4. 第 4 章 `description` 中注明了固定文本的范围，填写前先阅读 `references/writing-guide.md` 的「本文档的填写范围」

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
  --template "documents/[06]可靠性和可维护性大纲-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[06]可靠性和可维护性大纲-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
