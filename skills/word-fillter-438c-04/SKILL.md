---
name: word-fillter-438C-04
description: "当用户提到「按照438C模板填写word文档」「软件质量保证计划」「质量保证计划」「质量保证」「SQAP」「SQA」「Quality Assurance Plan」时触发。交互式填写 GJB 438C [04] 软件质量保证计划模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[04]软件质量保证计划-438C.docx` 模板生成或修改 GJB 438C 软件质量保证计划时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构
- 本模板无动态章节（无 X 占位子节），章节均为静态段落替换 + 表格填充

# 目录结构

- `documents/[04]软件质量保证计划-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（SQA、CSCI、评审、回归测试等）
- `references/style-rules.md`：句式与表达规范（计划句式、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；同时收集项目组织架构、质量管理制度、测试工具链、里程碑计划等计划类素材；
   - 写入规则：文档中的模块名、文档名、活动描述必须与项目事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组，1.2 系统概述按 6 个并列子条（1.2.1～1.2.6）逐条填写
   - 第 2 章（引用文档）以条文形式列出引用文件（本模板无引用文档表格）
   - 第 3 章（质量保证组织）正文 + 组织设置表（org_roles）
   - 第 4 章（质量目标）章引言 + 6 个量化目标子条（4.1～4.6）
   - 第 5 章（研制开发过程中的质量保证）各子条 + 两张表：技术文件表（tech_files）、计划的评审表（planned_reviews）
   - 第 6 章（交付使用、售后服务的质量保证）使用 `placeholders` 数组
   - 第 7 章（日程表）引言 + 日程表（schedule）
   - 第 8 章（质量审核和质量监督）只替换章引导句，模板保留的并列项不得改动
   - 第 9 章（注解）为术语和缩略语
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：计划句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——质量目标是否量化（抽样率/缺陷率/通过率）、计划条文句式是否规范、无内容的条目是否如实陈述、模板示例单位名称（如"总装综合计划部"）是否已改写、章节号引用是否真实存在、表格行数是否与模板合并单元格结构一致。
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

**静态章节**（本模板全部为静态章节，无 `subsections` 动态章节机制）：

```json
{
  "id": "1.4",
  "name": "与其他计划之间的关系",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**表格填充**：

```json
{
  "tables": [{
    "table_id": "org_roles",
    "locator_rows": [["角色", "人员", "职责"]],
    "data_start_row": 1,
    "preserve_tail_rows": 0,
    "columns": ["role", "person", "responsibility"],
    "rows": [
      { "role": "...", "person": "...", "responsibility": "..." }
    ]
  }]
}
```

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 章级 placeholder（如 4.1～4.6、5.4.1.1～5.4.1.5）各对应模板中的一个引导段落，只修改其 `content`
4. `rows` 中每行的字段必须严格等于 `columns` 定义
5. **纵向合并单元格约束（重要）**：「技术文件」表种类列（前 13 行/后 7 行各为一个纵向合并块）与「日程表」阶段/日期列（需求分析 5 行/软件设计 10 行/测试 11 行/初样正样评审 7 行）存在纵向合并，数据行数必须与模板一致（20 行/33 行），且合并块内各行的对应值必须相同（续行值在 Word 中不显示，取首行值）；详见 project.json 中对应表格的 `generation_prompt` 与 `references/writing-guide.md`

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
  --template "documents/[04]软件质量保证计划-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[04]软件质量保证计划-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
