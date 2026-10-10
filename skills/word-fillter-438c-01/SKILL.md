---
name: word-fillter-438C-01
description: "当用户提到「按照438C模板填写word文档」「软件总体技术方案」「总体技术方案」「OTP」「Overall Technical Plan」「[01]」时触发。交互式填写 GJB 438C [01] 软件总体技术方案模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[01]软件总体技术方案-438C.docx` 模板生成或修改 GJB 438C 软件总体技术方案时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 模板骨架说明（本模板的重要特性）

[01] 模板是方案类骨架模板，正文各章"可填充性"不同，务必先读再写：

- **引擎自动填充**：封面信息（密级、阶段、版次、单位、日期、型号、产品名称）、1.1 标识指导段、1.2 系统概述的 a）～f）六个列表项、引用文档表（第 2 章 tables）。
- **模板无锚点、引擎不处理，需人工在 Word 中补写**：1.3 文档概述（标题下无任何段落）、第 3～11 章（总体方案与结构、模型设计方案、资源配置方案、系统配置方案、接口配置方案、组织机构及人员配置、关键技术、方案实施的技术路线和实施计划、经费概算及规划——各节仅有标题，正文为空）。严格模式禁止向无锚点位置插入文本，project.json 中这些章节只保留 `title`/`description` 说明，**不得**给它们编 `replacement_pattern`（锚点不匹配会报错）。人工补写时按 `references/writing-guide.md` 逐章执行。
- 1.2 的 a）～f）是自动编号列表：每个子条 `content` 必须单行、禁止换行符，否则换行会被克隆成新列表项、破坏编号。

# 目录结构

- `documents/[01]软件总体技术方案-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容（1.1/1.2）和引用文档表数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷，覆盖全部 11 章，含人工补写章）
- `references/terminology.md`：军用软件术语表（CSCI、HWCI、配置项、方案类术语等）
- `references/style-rules.md`：句式与表达规范（方案句式、量化指标、如实陈述原则、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：直接用 templates/ 下的 config/project，输出到 scripts/output/）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的模块名、接口名、功能描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders`：1.1 只改 `content`；1.2 只改六个子条（1.2.1～1.2.6）的 `content`，每个子条单行；1.3 无锚点，引擎不处理
   - 第 2 章（引用文档）使用 `tables`，只改 `rows`
   - 第 3～11 章为无锚点骨架章节，引擎不处理；按 `references/writing-guide.md` 生成内容后，由用户在 Word 中人工补写
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录；随后在 Word 中人工补写 1.3 与第 3～11 章正文。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：方案句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——标识五要素是否齐全、1.2 各子条是否单行、量化指标是否有依据、无内容条目是否如实陈述、方案各章名称是否前后一致、模块与接口描述是否第 0 步的源码事实一致。
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
| content.scope | `background_information` | 方案范围 | 结合用户描述生成 |
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
  "id": "1.1",
  "name": "标识",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**带子条的章节**（1.2 系统概述，子条对应模板 a）～f）列表项）：
```json
{
  "id": "1.2",
  "name": "系统概述",
  "type": "content_generation",
  "generation_prompt": "生成子章节的提示...",
  "subsections": {
    "1.2.1": { "name": "用途、使用对象和时机", "replacement_pattern": "本文档适用系统和软件的用途、使用对象和时机；", "content": "string（单行）" }
  }
}
```

> **1.2 子条的机制约束（重要）**
> 引擎把 1.2 的六个子条作为普通段落替换规则处理：`subsections` 中每个子条的 `replacement_pattern` 逐字对应模板中的一个列表项原文，`content` 替换该列表项。`content` **必须单行**——模板列表项是自动编号段落，含换行符的 content 会把克隆段落变成额外列表项，破坏 a）～f）编号。子条 `name` 仅作展示说明，不写入文档。

**表格填充**：
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

1. 1.1 只修改 `content`；1.2 只修改六个子条的 `content`（单行）；1.3 与第 3～11 章无锚点，不要给它们添加 `replacement_pattern`/`content`/`rows` 之外的字段，也不要自行编造锚点
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. `rows` 中每行的字段必须严格等于 `columns` 定义

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
  --template "documents/[01]软件总体技术方案-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[01]软件总体技术方案-438C-filled.docx"
```

或使用免参数入口（不推荐：输出到 scripts/output/，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录；随后在 Word 中人工补写 1.3 文档概述与第 3～11 章正文（参见"模板骨架说明"）。
