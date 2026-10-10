---
name: word-fillter-438C-22
description: "当用户提到「按照438C模板填写word文档」「测试问题报告」「软件测试问题」「问题报告」「438C」「Test Problem Report」「TPR」时触发。交互式填写 GJB 438C [22] 测试问题报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[22]测试问题报告-438C.docx` 模板生成或修改 GJB 438C 测试问题报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[22]测试问题报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：测评依据表与两张问题统计表数据
- `references/writing-guide.md`：章节级写作要点（必写内容、填写深度、常见缺陷与模板已知限制）
- `references/terminology.md`：军用软件术语表（CSCI、STP/STD/STR、问题类型/等级/状态等）
- `references/style-rules.md`：句式与表达规范（如实陈述、量化计数、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部内容的事实依据：
   - 获取实际测试记录（测试用例标识、执行结果、问题现象描述、日志/截图索引），作为第 4 章问题单与第 5 章统计的唯一事实来源；
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API，用于核对问题描述中的模块名、接口名与源码事实一致；
   - 若用户提供了建设方案或测试计划文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的文档清单、测试项作为测评依据素材；
   - 写入规则：第 5 章统计数字必须由第 4 章问题单汇总得出，禁止编造问题或数字；测试记录无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json`：
   - 第 2 章（测评依据）使用 `tables`，逐行填写依据文档
   - 第 5 章（测试问题统计）使用 `tables`，按问题类型、按问题等级各填一行计数
   - 第 1/3/4/6 章无可填写占位（见下文"已知限制"），保持 `description` 不动
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录；然后在 Word 中完成引擎不代填的部分：1.2/1.3/第 6 章补写、第 4 章按实际问题逐张填写问题报告单、签署页签字。

# 内容生成规范

生成每处 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、填写深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：如实陈述、量化计数与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的测试记录生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——统计分项之和是否等于总计、分类口径是否与第 3 章定义一致、测评依据编号版本是否可核查、问题描述是否测试记录事实。
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

本模板正文无"本章应/本条应"指导段落，可填写项只有三张表：

| 章节 | 结构 | 可修改内容 |
|------|------|-----------|
| 1 范围 | 无占位 | 不可填（1.1 标识由 config.json 自动填写；1.2/1.3 模板空白） |
| 2 测评依据 | `tables` | 只修改 `rows`：序号、名称、版本、发布日期、来源 |
| 3 软件问题类型、严重性等级说明 | 标准固定文字 | 不可填、不得改 |
| 4 测试问题报告 | 空白表单 | 不代填，Word 中按实际问题逐张填写 |
| 5 测试问题统计 | `tables` | 只修改 `rows`：两张统计表各一行计数 |
| 6 其他 | 无占位 | 不可填（模板空白，需要时 Word 中补写） |

### 处理规则

1. 表格只修改 `rows`，每行字段严格等于 `columns` 定义
2. 不修改 `id`、`type`、`columns`、`locator_rows`、`table_id`、`data_start_row`、`preserve_tail_rows` 等模板结构字段
3. 第 5 章两张统计表的计数必须与实际问题单一致：5.1 各类型计数之和 = 总计；5.2 各等级计数之和 = 总计；两表总计相等

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。
> 其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符（如统计表表头的全角"ＸＸ"占位符）。
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

### 已知限制（模板固有）

1. **1.2/1.3/第 6 章无占位文字**：模板本身空白，引擎无法插入内容，生成后在 Word 中手工补写。
2. **统计表表头全角占位符**：5.1/5.2 表头第 2 行的"ＸＸ""ＸＸＸ"是模板固定文字，不在可编辑范围，生成文档中原样保留，使用时在 Word 中改为完整类型/等级名称。
3. **第 4 章问题报告单**：每问题一张的空白表单，引擎不生成问题内容（禁止编造问题），由测试人员按实际记录填写。
4. 详见 `references/writing-guide.md`「已知限制」。

# 运行

安装依赖（首次）：

```bash
pip install -r scripts/requirements.txt
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[22]测试问题报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[22]测试问题报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
