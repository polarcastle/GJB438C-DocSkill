---
name: word-fillter-438C-19
description: "当用户提到「按照438C模板填写word文档」「软件测试报告」「测试报告」「438C」「STR」「Test Report」「软件测试」时触发。交互式填写 GJB 438C [19] 软件测试报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[19]软件测试报告-438C.docx` 模板生成或修改 GJB 438C 软件测试报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[19]软件测试报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、第 3 章统计表数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、STR、测试项、问题等级等）
- `references/style-rules.md`：句式与表达规范（测试结论句式、缺陷五要素、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 收集测试执行记录与问题台账（测试管理系统导出、测试用例清单、问题/更改报告），形成「测试画像」：测试项划分、测试用例标识与完成状态、问题类型/等级/轮次/处置状态；
   - 扫描被测项目源码目录，佐证软件特性、模块划分描述（开发语言、模块、入口、对外接口）；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取项目背景、建设目标作为第 1 章素材；
   - 写入规则：测试用例数、通过率、问题数、报告编号必须与测试记录和台账一致，禁止编造；记录无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组
   - 第 2 章（引用文档）为静态章节，按 a) b) c) 分段填写
   - 第 3 章（测试结果概述）使用 `placeholders` 数组：3.1 总体评估按 a)～ｄ) 分项填写并配两张统计表（`tables`），3.2/3.3 各为静态条
   - 第 4 章（详细测试结果）按 X 原型条填写一个完整测试项：4.X 标题、4.X.1 总结、4.X.2.Y 问题用例五要素、4.X.3.Y 偏差用例三要素
   - 第 5 章（注释）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：测试结论句式、量化口径、缺陷/偏差要素规范与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的测试画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——数字是否与统计表一致、缺陷三要素/问题五要素/偏差三要素是否齐全、完成状态引用条号是否真实、测试用例与问题报告标识是否与台账一致。
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
| content.scope | `background_information` | 测试范围 | 结合用户描述生成 |
| content.features | `background_information` | 功能特性 | 结合用户描述生成 |

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 用户需求生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入 |

### 章节结构类型

**静态章节/条目**（无 subsections）：
```json
{
  "id": "1.2",
  "name": "系统概述",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**第 4 章 X 原型条的填写机制（重要）**
本模板全部标题使用 Word 自动多级编号，`4.X(测试的项目唯一的标识符)` 等原型标题中的 `4.X` / `4.X.2.Y` 是字面 instructional 文字。引擎对标题段落做**整段替换**：
- `4.X` 条目的 `content` 填测试项名称（如"功能测试"），显示为"4.1 功能测试"；
- `4.X.2.Y` 条目的 `content` 填用例标识（如"测试用例TC-FUN-003"），显示为"4.1.2.1 测试用例TC-FUN-003"；
- 正文中引用这些子条时写自动编号后的真实条号（4.1.2.1、4.1.3.1）。
- 被测软件有多个测试项时，在 Word 中对填好的 4.1 节整块复制后修改标题与内容；JSON 中的原型条目只覆盖一个测试项。

**表格填充**（第 3 章两张统计表）：
```json
{
  "id": "3",
  "tables": [{
    "table_id": "problem_type_statistics",
    "locator_rows": [
      ["测试轮次", "测试轮次", "问题总计", "问题类型", "问题类型", "问题类型", "问题类型"],
      ["测试轮次", "测试轮次", "问题总计", "功能缺失", "功能错误", "界面问题", "其它"]
    ],
    "data_start_row": 2,
    "preserve_tail_rows": 0,
    "columns": ["round", "disposition", "total", "missing", "error", "ui", "other"],
    "rows": [
      { "round": "首轮测试", "disposition": "首轮测试", "total": "12", "missing": "1", "error": "5", "ui": "3", "other": "3" }
    ]
  }]
}
```

统计表填写要点：
- 模板数据行的前两列（测试轮次、处置状态）为固定标签，`rows` 中前两列必须逐字沿用模板标签（"首轮测试"、"已纠正"、"新引入"、"未纠正"、"合计"）；
- 第 1 行是"合计"行（`data_start_row: 2` 起全部为数据行，合计行也在 `rows` 内），合计＝全部轮次累计发现的问题数；回归轮次的"已纠正/新引入/未纠正"行为当轮处置情况；
- 单元格不允许为空，无问题的填 "0"；各行"问题总计"应等于该行各分类之和，合计行应与 3.1 正文数字一致。

### 处理规则

1. 静态条目只修改其 `content`；`id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段不得修改
2. `rows` 中每行的字段必须严格等于 `columns` 定义
3. 无实质内容可写的条目如实写"无……"类陈述，不留空（引擎拒绝空 content）

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
  --template "documents/[19]软件测试报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[19]软件测试报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
