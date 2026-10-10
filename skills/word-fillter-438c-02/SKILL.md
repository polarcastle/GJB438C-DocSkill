---
name: word-fillter-438C-02
description: "当用户提到「按照438C模板填写word文档」「软件开发计划」「开发计划」「SDP」「Software Development Plan」「438C」时触发。交互式填写 GJB 438C [02] 软件开发计划模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[02]软件开发计划-438C.docx` 模板生成或修改 GJB 438C 软件开发计划（SDP）时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[02]软件开发计划-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、子章节和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷，含本模板已知限制）
- `references/terminology.md`：军用软件术语表（CSCI、构建版、基线、里程碑等）
- `references/style-rules.md`：句式与表达规范（计划句式、量化指标、如实陈述原则、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案、任务书或既有文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、研制阶段划分、组织与资源信息作为补充素材；
   - 写入规则：文档中的模块名、工具名、文档名必须与素材事实一致，禁止编造素材中不存在的内容；素材无法支撑的章节（如评审时间、人时数），提示用户补充信息或如实从简并标注"待定"。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 标识引言；1.2 系统概述为六个分条子条（1.2.1～1.2.6）；1.3 文档概述；1.4 与其它计划的关系
   - 第 2 章（引用文档）：整段引用文件清单
   - 第 3 章（策划背景概述）：章引言 + a)～f) 六个分条
   - 第 4 章（整个软件开发活动计划）：4.1 软件开发过程（含表4-1 阶段划分表）；4.2 总体计划各子条（4.2.1～4.2.7）
   - 第 5 章（详细开发活动计划）：5.1～5.17 各活动条目；5.2.1 测试环境表（表5-1）；5.17.1 风险表（表5-2）
   - 第 6 章（进度安排及活动网络）：进度方法与进度表（表6-1，22 个活动行）、活动网络图
   - 第 7 章（组织和资源）：项目组织（表7-1）、人力资源（表7-2）、设施（表7-3）、需方资源（表7-4）
   - 第 8 章（注解）：术语和缩略语
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录；然后按 `references/writing-guide.md`「模板限制」一节，在 Word 中手工补填联合评审两张表（5.16.1/5.16.2）及 12 处与正样重复的初样测试条目。

# 本模板已知限制（重要）

1. **重复指导文字（12 处不自动填写）**：5.3.7/5.3.8 与 5.4.3/5.4.4 中的"软件配置项测试的演示性运行、执行软件配置项测试、修改和再测试、软件配置项测试结果分析和记录、软件系统测试的演示性运行、执行软件系统测试、修改和再测试、软件系统测试结果分析和记录"等条目，其指导文字在初样与正样两节中逐字重复，引擎严格模式禁止一条规则命中多处，这 12 处保留模板原句不填写。已填写的独立性/环境/准备条目（5.3.7.1～5.3.7.3、5.3.8.1、5.3.8.3、5.4.3.1～5.4.3.3、5.4.4.1、5.4.4.3）已覆盖其要点；如确需填写，生成后在 Word 中手工替换。
2. **联合评审表（2 张不自动填写）**：5.16.1 联合技术评审与 5.16.2 联合管理评审的两张表表头完全相同，且数据行含空单元格，表格定位机制（`locator_rows`）无法区分两表、也不允许空单元格定位，故 `project.json` 未配置这两张表。评审时间、人员、准则、程序、取样方法、记录等内容需生成后在 Word 中按表填写。
3. **纯标题条（无指导文字）**：4.2.3 可重用软件产品（其子条 4.2.3.1/4.2.3.2 已配置）、5.9/5.10/5.13/5.17 等节中仅作分组用的标题、5.17.8 计划中未提及的其他活动，模板中没有可锚定的指导文字，不自动生成内容。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：计划句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——进度/人力/资源数据是否量化且全文一致（第 5 章时间段 ↔ 表6-1、7.2.1 文字 ↔ 表7-2）、分条列举是否逐条回答、不适用条目是否如实陈述、文档名引用是否与 5.2.3 清单一致、相关方称谓是否全文统一且无具体单位名称。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

| 字段位置 | type | 说明 | content 生成方式 |
|----------|------|------|-----------------|
| project.* | `original_text` | 项目基础信息（名称、版本、单位等） | 直接使用用户输入 |
| document.* | `original_text` | 文档元信息（编号、标题、密级、阶段、日期、总页数） | 直接使用用户输入 |
| content.overview | `background_information` | 项目概述（对应 1.2 素材） | 结合用户描述生成 |
| content.scope | `background_information` | 项目范围（对应第 3 章素材） | 结合用户描述生成 |
| content.features | `background_information` | 功能特性（对应 3.a 素材） | 结合用户描述生成 |

> `document.page_count`（总页数）为封面"共XX页"的填写值，仅当 content 非空时引擎才替换该占位符；不确定时可留空，封面保留"共XX页"。

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 用户需求生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入 |

### 章节结构类型

**静态章节**（`placeholders` 数组中的条目，无 `subsections`）：
```json
{
  "id": "5.5",
  "name": "软件测评",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**带子条的章节**（`subsections` 为**平铺**字典，键为点分编号）：
```json
{
  "id": "5.1",
  "name": "项目计划及监督",
  "type": "content_generation",
  "replacement_pattern": "本条应描述软件开发策划、CSCI测试策划...",
  "content": "string（本条正文）",
  "subsections": {
    "5.1.1": { "name": "软件开发策划（制定）", "replacement_pattern": "...", "content": "string" },
    "5.1.1.1": { "name": "软件开发策划（调整）", "replacement_pattern": "...", "content": "string" }
  }
}
```

> **结构机制约束（重要）**：
> - 引擎只展开两层：`structure → placeholders → subsections`。`subsections` 必须是**平铺**字典， deeper 层级（如 5.2.2.1）直接以完整编号为键与上级并列，**禁止再嵌套 `subsections`**。
> - `subsections` 中每个子条**必须同时有 `replacement_pattern` 和 `content`**（模板中的整段指导文字作锚点），否则报错；模板中只有标题、没有指导文字的分组条（如 4.2.3、5.17.8）不配置条目。
> - 占位符自身的 `replacement_pattern` 不得与其任一子条的锚点重复（同一锚点只能被一条规则消费）。
> - 分条列举式小节（1.2 六个分条、第 3 章 a)～f)、5.2.2 开发库清单、7.2.1 的 1)2)3)）每个分条是一个子条，`content` 以该分条的编号/引导语开头再作答，如 `"a)所要开发系统、软件的需求和约束：……"`。

**表格填充**：
```json
{
  "id": "6",
  "tables": [{
    "table_id": "schedule",
    "locator_rows": [
      ["软件开发活动", "活动的起始点", "活动的完成点", "提交的草案/最终交付结果", "所属里程碑"]
    ],
    "data_start_row": 1,
    "preserve_tail_rows": 0,
    "columns": ["activity", "start_point", "end_point", "deliverable", "milestone"],
    "rows": [
      { "activity": "初样第一次需求原型", "start_point": "2026年1月", "end_point": "2026年2月", "deliverable": "第一版原型系统", "milestone": "初样" }
    ]
  }]
}
```

### 处理规则

1. 只修改各条目的 `content` 和表格的 `rows` 值；不修改 `id`、`type`、`columns`、`locator_rows`、`data_start_row`、`preserve_tail_rows`、`replacement_pattern` 等结构字段
2. `rows` 中每行的字段必须严格等于 `columns` 定义，且**所有单元格值必须非空**（引擎拒绝空串）
3. 行数可以多于或少于模板现有数据行：引擎自动克隆数据行原型补齐、并把多余模板数据行清空
4. 表4-1（开发阶段，19 行）与表6-1（进度，22 行）的"提交的草案/最终交付结果"等列，模板已预置内容，填写时保留模板预置值、只补空缺列（如表6-1 的起止时间）

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符。修改后会导致报错 `期望命中 1 张表，实际 0 张`。
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
  --template "documents/[02]软件开发计划-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[02]软件开发计划-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
