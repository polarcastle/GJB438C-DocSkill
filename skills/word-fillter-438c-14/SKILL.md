---
name: word-fillter-438C-14
description: "当用户提到「按照438C模板填写word文档」「438C」「软件可靠性和可维护性设计」「可靠性和可维护性设计」「可靠性设计」「可维护性设计」「RMS设计」时触发。交互式填写 GJB 438C [14] 软件可靠性和可维护性设计模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[14]软件可靠性和可维护性设计-438C.docx` 模板生成或修改 GJB 438C 软件可靠性和可维护性设计方案时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[14]软件可靠性和可维护性设计-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、子章节和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、MTBF、容错、避错、维护类型等）
- `references/style-rules.md`：句式与表达规范（设计策略句式、量化指标、如实陈述原则与禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的模块名、接口名、功能描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息（`company`/`department` 见下文「单位名称无默认值」）。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 标识由 config.json 自动生成；1.2/1.3 无锚点，见「无锚点章节」
   - 第 2 章（引用文档）使用 `tables`（表头：标识/标题/日期/来源）
   - 第 3 章（软件可靠性设计）使用 `subsections`（3.1～3.8）；3.9 无锚点，见「无锚点章节」
   - 第 4 章（软件可维护性设计）使用 `placeholders`（4.1.1～4.8，含 `-N` 后缀的列举项占位）；4.6.1～4.6.3 无锚点，见「无锚点章节」
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录；对无锚点章节手工补充内容（已为用户准备好的内容在对话中交付）。

# 无锚点章节（重要）

本模板下列章节**没有 guidance 段落**，引擎无法自动填写，生成后须手工补充：

- 1.2 系统概述、1.3 文档概述
- 3.9 其它
- 4.6.1 人力资源分析、4.6.2 环境资源分析、4.6.3 财政资源分析

为上述章节生成的素材应通过对话交付给用户，并提示在 Word 中插入对应章节标题之下。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷（先读其「机制说明」）；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：设计策略句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全、句式是否符合"本软件……"规范、不采纳的策略是否如实陈述、列举项结构是否保留、模块与接口描述是否第 0 步的源码事实一致。
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
| content.overview | `background_information` | 项目概述（素材字段，供第 3、4 章写作参照） | 结合用户描述生成 |
| content.scope | `background_information` | 设计范围（素材字段） | 结合用户描述生成 |
| content.features | `background_information` | 功能特性（素材字段） | 结合用户描述生成 |

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 用户需求生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入 |

### 章节结构类型

**静态章节**（第 3 章 subsections、第 4 章 placeholders 均是）：
```json
{
  "id": "3.1",
  "name": "结构复杂度控制",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "generation_prompt": "生成内容的提示...",
  "content": "string"
}
```

**表格填充**（第 2 章引用文档）：
```json
{
  "id": "2",
  "tables": [{
    "table_id": "reference_documents",
    "locator_rows": [["标识", "标题", "日期", "来源"]],
    "data_start_row": 1,
    "preserve_tail_rows": 0,
    "columns": ["identifier", "title", "date", "source"],
    "rows": [
      { "identifier": "...", "title": "...", "date": "...", "source": "..." }
    ]
  }]
}
```

### 处理规则

1. 第 3 章 `subsections` 与第 4 章 `placeholders` 中的每个条目只修改其 `content`（有 `generation_prompt` 的按其生成）；引导段写项目化陈述，`-N` 后缀的列举项逐条改写并保留 a）b）c）或"—"样式
2. 不修改 `id`、`type`、`columns`、`locator_rows`、`replacement_pattern` 等模板结构字段
3. 通用条文类列举项（维护成本因素、退役考虑项等）允许与模板原文逐字相同，不得为"消除重复"强行改写
4. `rows` 中每行的字段必须严格等于 `columns` 定义

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
pip install -r scripts/requirements.txt
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[14]软件可靠性和可维护性设计-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[14]软件可靠性和可维护性设计-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
