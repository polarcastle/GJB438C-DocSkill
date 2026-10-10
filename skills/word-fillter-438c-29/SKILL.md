---
name: word-fillter-438C-29
description: "当用户提到「按照438C模板填写word文档」「技术总结报告」「438C」「[29] 技术总结」「TSR」「研制总结」时触发。交互式填写 GJB 438C [29] 技术总结报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[29]技术总结报告-438C.docx` 模板生成或修改 GJB 438C 技术总结报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 模板特点（重要）

[29] 技术总结报告模板是**纯标题骨架**模板，与 [08]/[10] 不同：

- 正文第 1～5 章只有章节标题，**没有任何"本条应……"类指导文字段落**，因此引擎无法向章节内写入正文；本 Skill 的填写范围是：封面与签署页信息、文件更改记录表、占位小节标题（`3.1.2.3 XX技术指标`、`3.2.3  XX设计`、`3.2.X 行为设计`）。
- 模板**没有封面标识行**（"文档标识号：""标题：""软件名称："等），引擎的标识行规则为空；文档编号通过文件更改记录表的"更改文件号"列写入。
- 各章正文需生成后按 `references/writing-guide.md` 在 Word 中人工撰写；`references/` 三件套即按此用途编写，素材收集与写后自查流程仍然适用。

# 目录结构

- `documents/[29]技术总结报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：占位标题改名与文件更改记录表数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷），供生成后人工补写正文使用
- `references/terminology.md`：军用软件术语表（CSCI、CSC、MTBF 等）
- `references/style-rules.md`：句式与表达规范（总结陈述句式、量化指标、如实陈述原则、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 收集研制任务书/合同中的考核指标条目（编号、要求值），作为 3.1 节指标对比的依据；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的模块名、接口名、功能描述必须与源码事实一致，禁止编造源码中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息（`company`/`department` 见下文"单位名称无默认值"）。
2. 修改 `templates/project.json`：
   - `change_record` 章节的文件更改记录表 `rows`（每次更改一行；文档编号写入 `change_doc_no` 列，须与 `config.json` 的 `document.id` 一致）；
   - `3` 章节的三个占位标题 `content`：改为实际的小节标题（保持编号不变，只替换 XX/X 部分，如 `3.1.2.3 XX技术指标` → `3.1.2.3 可靠性技术指标`）。
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。
5. 按 `references/writing-guide.md` 在各章标题下人工补写正文（引擎不负责此部分），写后按 `references/style-rules.md` 自查。

# 内容生成规范

生成或修改任何 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：对应章节的必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：总结陈述句式、量化指标对比、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——指标是否"要求值＋实现值"双写、成果是否有证据、占位标题编号是否与模板层级一致、模块与接口描述是否与第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在位置、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

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

> 本模板无标识行，`document.id` 不落封面，而是通过 `project.json` 中文件更改记录表的 `change_doc_no` 列写入正文；两处取值必须一致。

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 用户需求生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入 |

### 结构说明

- `change_record`：文件更改记录表，只修改 `rows` 数组（每行字段严格等于 `columns`）。
- `3`：第 3 章的占位标题改名，只修改三个 placeholder 的 `content`；`content` 是**完整的替换后标题文本**（含编号），且必须与模板原文格式一致——`3.2.3` 的编号后是两个空格（`3.2.3  XX设计` → `3.2.3  实际名称`）。

### 处理规则

1. 只修改 `content` 与 `rows`，不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 的 `name` 与 `replacement_pattern` 等模板结构字段
2. `rows` 中每行的字段必须严格等于 `columns` 定义
3. 正文各章（1、2、4、5 章及第 3 章的小节正文）模板中没有可锚定的段落，**不要**为它们新增 placeholder——锚点不匹配会触发严格报错；这些内容在 Word 中按 `references/writing-guide.md` 补写

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
  --template "documents/[29]技术总结报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[29]技术总结报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
