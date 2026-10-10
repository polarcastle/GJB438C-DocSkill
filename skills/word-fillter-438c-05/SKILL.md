---
name: word-fillter-438C-05
description: "当用户提到「按照438C模板填写word文档」「软件标准化大纲」「标准化大纲」「438C」「Standardization Outline」时触发。交互式填写 GJB 438C [05] 软件标准化大纲模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[05]软件标准化大纲-438C.docx` 模板生成或修改 GJB 438C 软件标准化大纲时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[05]软件标准化大纲-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、题注与表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（标准化系数、三化、重大标准、剪裁等）
- `references/style-rules.md`：句式与表达规范（大纲句式、量化指标、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系、已有文档清单；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的模块名、接口名、标准引用必须与项目事实一致，禁止编造项目中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 标识由 config.json 自动填写，本章无 project.json 占位
   - 第 2 章（引用文档）：`2.caption` 题注 placeholder + `tables`（引用文件表）
   - 第 3 章（标准化目标）：`placeholders` 按条组织（3.1～3.5，条内列项为 `.a/.b/.c` 等子 id）
   - 第 4 章（标准实施要求）：`placeholders`（4.1～4.4，4.3 含 `major.*`/`plan.*` 两组列项）
   - 第 5 章（建立标准化文件体系要求）：`placeholders`（5.1～5.4）
   - 第 6 章（标准化工作范围和研制各阶段的主要工作）：`placeholders`（6.1～6.3）
   - 第 7 章（技术文档编制格式要求）：`placeholders`（7.1～7.9，规定性内容基本沿用模板表述）
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录；随后在 Word 中**手工补写 1.2 系统概述、1.3 文档概述**（见「已知限制」）。

## 已知限制（模板结构所致，非引擎缺陷）

- **1.2 / 1.3 无锚点**：模板中"系统概述""文档概述"标题下没有任何占位段落，引擎无锚点可替换，生成后必须手工编写（写作要点见 `references/writing-guide.md` 第 1 章）。
- **附录 A/B/C 为静态内容**：封面/签署页格式样例、模板使用说明、字体字号汇总不配置、不填充，生成后原样保留，确需调整时在 Word 中手工修改。
- **文件更改记录表与签署页不机器填写**：首版无更改记录；签署栏由评审时手签。
- **封面日期规则覆盖 4 处**：模板封面日期与附录 A 三栏示例封面中的日期是相同文本，精确替换会一并替换（示例封面日期与真实日期一致，无害）。
- **题注按 placeholder 处理**：本模板题注占位为"表-X引用文件"风格（非"表X-X"），引擎的图表自动重编号正则不匹配该风格，故 `2.caption` 按普通段落 placeholder 填写，编号遵循模板 7.7 条"表＋连续阿拉伯数字"规则（"表1  引用文件"）。
- **列表项半角括号**：模板列项编号使用半角右括号（"a)"），`replacement_pattern` 与 `content` 中的列项编号必须与模板一致，不得写成全角"）"。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：大纲句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全（标准化系数、比例、数量）、句式是否符合"应……"规范、规定性内容是否沿用模板表述、标准引用是否真实存在、章节号引用是否真实存在、模块与接口描述是否与第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

| 字段位置 | type | 说明 | content 生成方式 |
|----------|------|------|-----------------|
| project.* | `original_text` | 项目基础信息（名称、版本、单位等） | 直接使用用户输入 |
| document.* | `original_text` | 文档元信息（编号、标题、密级、阶段、日期等） | 直接使用用户输入 |
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

### 章节结构

本模板无动态章节（无 X 编号占位子节），全部为静态 placeholder——每条指导文字一个 placeholder：

```json
{
  "id": "3.2.a",
  "name": "内容-水平目标",
  "type": "content_generation",
  "replacement_pattern": "（逐字等于模板中的指导/示例段落原文，含行首空格与半角括号）",
  "content": "string"
}
```

- `id` 为语义编号：章.条（.列项），如 `4.3.major.a`、`7.9.A1`；只作规则键，不写入文档。
- `content` 为该段的完整替换文本；换行符 `\n` 会生成多个独立段落（本模板示例 content 均为单段）。
- 第 7 章等规定性内容的 `content` 默认沿用模板表述，项目另有规定时才替换。

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
      { "number": "1", "name": "《GJB 438C-2021 军用软件开发文档通用要求》", "version": "2021", "release_date": "2021-XX-XX", "source": "军用标准化主管部门" }
    ]
  }]
}
```

### 处理规则

1. 只修改 placeholder 的 `content` 与表格的 `rows`，不修改 `id`、`type`、`columns`、`locator_rows`、`replacement_pattern` 等结构字段
2. `rows` 中每行的字段必须严格等于 `columns` 定义；行数可增加（引擎自动克隆模板行）

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
  --template "documents/[05]软件标准化大纲-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[05]软件标准化大纲-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录，并手工补写 1.2、1.3 两节。
