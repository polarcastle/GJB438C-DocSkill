---
name: word-fillter-438C-07
description: "当用户提到「438C 安全性大纲」「[07] 安全性大纲」「软件安全性大纲」「安全性」「SSP」「Safety Program」时触发。基于 GJB 438C [07] 软件安全性大纲模板，严格填写封面、标识、各生存周期阶段安全性要求与安全性活动项目，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[07]安全性大纲-438C.docx` 模板生成或修改 GJB 438C 软件安全性大纲时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[07]安全性大纲-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、静态子条和引用文档表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷、模板机制说明）
- `references/terminology.md`：军用软件安全性术语表（CSCI、FMECA、安全关键功能等）
- `references/style-rules.md`：句式与表达规范（大纲句式、量化指标、如实陈述原则、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系、日志与容错机制；
   - 若用户提供了建设方案、研制任务书或项目计划文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、研制周期、经费与资源约束作为补充素材；
   - 写入规则：文档中的模块名、机制描述、活动安排必须与源码和项目资料事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息（1.1 标识五行由本文件自动生成）。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 由 config.json 精确规则填写；1.2 系统概述、1.3 文档概述在模板中无锚点文字，**生成后需在 Word 中手工补写**（见 references/writing-guide.md 第 1 章）
   - 第 2 章（引用文档）：使用 `tables` 填写引用文档表；"表-X"题注由引擎替换为"表2-1"
   - 第 3 章（软件生存周期）：3.1 各阶段安全性要求为 8 个静态子条（3.1.1～3.1.8），3.2 度量方法为静态章节
   - 第 4 章（软件安全性大纲要求）：章引言 + 4.1 考虑的主要因素 + 4.2 主要活动项目（含 4.2.1～4.2.9 静态子条；其中 4.2.6 评审检查单为模板标准条款，保留不填）
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，**在 Word 中补写 1.2 系统概述、1.3 文档概述两节**，首次打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：大纲句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——各阶段活动是否项目化改写、量化指标是否有依据、以冒号收束的引言是否与后续清单衔接、章节号引用是否真实存在、机制与模块描述是否与第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项（研制周期、经费占比、主管机构名称等），在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

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
  "id": "3.2",
  "name": "软件生存周期安全性度量方法",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**静态子条章节**（本模板 3.1 的 8 个阶段子条、4.2 的活动项目子条）：

```json
{
  "id": "3.1",
  "name": "软件生存周期各阶段对安全性要求",
  "type": "content_generation",
  "subsections": {
    "3.1.1": {
      "name": "可行性研究与计划阶段",
      "replacement_pattern": "可行性研究与计划阶段——进行项目安全可行性分析。",
      "content": "string"
    }
  }
}
```

> **本模板无动态章节**：INSERTION_PARENT_RULES 为空，所有子条均为静态子条——`replacement_pattern` 为模板对应段落的原文（逐字，含标点），`content` 整段替换该段落；子条 `name` 仅作 JSON 内说明，不写入文档。不得以动态章节（空 `subsections` 之外的形式）改写这些子条。
> **收束句式**：4.2.1、4.2.2、4.2.4、4.2.5、4.2.8、4.2.9 的 content 以冒号"："收束，衔接模板保留的 a）～x）清单；4.2.3 的 content 为单个列表项，以"；"结尾；4.1 的 content 写项目特定的限制条件。

**表格填充**（第 2 章引用文档表）：

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

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`
2. 静态子条章节只修改各子条的 `content`；不修改 `id`、`subsections` 的 key、`replacement_pattern` 等模板结构字段
3. `subsections` 的 key 必须是有效章节编号（如 `"3.1.1"`、`"4.2.5"`）
4. `rows` 中每行的字段必须严格等于 `columns` 定义
5. 第 1 章 `placeholders` 为空数组：1.1 由 config.json 精确规则填写，1.2/1.3 无锚点，生成后手工补写
6. 4.2.6 评审检查单不在 `subsections` 中配置，模板原文保留

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
  --template "documents/[07]安全性大纲-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[07]安全性大纲-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。**生成后在 Word 中补写 1.2 系统概述、1.3 文档概述，并按提示刷新目录。**
