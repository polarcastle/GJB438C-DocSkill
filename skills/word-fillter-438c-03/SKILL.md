---
name: word-fillter-438C-03
description: "当用户提到「按照438C模板填写word文档」「软件配置管理计划」「配置管理计划」「438C」「SCMP」「CMP」时触发。交互式填写 GJB 438C [03] 软件配置管理计划模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[03]软件配置管理计划-438C.docx` 模板生成或修改 GJB 438C 软件配置管理计划时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[03]软件配置管理计划-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、子条目和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（SCM、SCI、基线、软件三库、FCA/PCA 等）
- `references/style-rules.md`：句式与表达规范（管理要求句式、量化周期、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、仓库目录结构、工具链（版本控制/CI/缺陷跟踪）、入口文件、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容、组织分工作为补充素材；
   - 写入规则：文档中的配置项划分、工具、角色、规程必须与项目事实一致，禁止编造素材中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息（`project.company`、`project.department` 必须由用户提供，见下）。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1～1.4）
   - 第 2 章（引用文档）为静态章节，引用文件以正文列举形式写入 `content`（本模板无引用文档表格）
   - 第 3 章（组织和职责）为章节级 `content` + 职责分工 `tables`（角色/人员/管理范围和职责）
   - 第 4 章（一般要求）使用 `placeholders` 数组（4.1～4.4，围绕"软件三库"）
   - 第 5 章（软件配置管理活动）为章节级引言 `content` + `placeholders`：5.1 配置标识；5.2～5.5 的 a)/b)/c)/d) 分项为各 placeholder 的 `subsections` 子条
   - 第 6 章（工具、技术和方法）、第 7 章（对供货单位的控制）、第 8 章（进度表）、第 9 章（注释）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：管理要求句式、量化周期、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——周期与权限是否量化到角色、三库分工是否交叉矛盾、基线/配置项标识是否唯一、第 8 章日程与第 5 章活动时机是否一致、配置项划分是否第 0 步的仓库事实一致。
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

**静态章节 / 静态 placeholder**（无 `subsections`）：
```json
{
  "id": "1.2",
  "name": "系统概述",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**分项 placeholder**（5.2～5.5 的 a)/b)/c)/d) 分项）：placeholder 的 `replacement_pattern`/`content` 替换本节引言段，`subsections` 中每个子条按 `replacement_pattern` 锚定模板中的一条分项指导文字并替换为实际内容：
```json
{
  "id": "5.2",
  "name": "配置控制",
  "replacement_pattern": "锚点文本...",
  "content": "string（本节引言）",
  "subsections": {
    "5.2.1": { "replacement_pattern": "a)在本计划所描述的……", "content": "a）更改批准权限……" },
    "5.2.2": { "replacement_pattern": "b)对己有配置项的……", "content": "b）对已有配置项的……" }
  }
}
```

> **5.4/5.5 引言段说明（重要）**：模板中 5.4 配置审核与 5.5 软件发行管理和交付的引言段均为同一句"本条应描述:"（全文 2 处、文本无法区分），引擎将其统一替换为固定引言"本条给出本节的配置管理规程与方法，具体规定如下。"。因此 5.4/5.5 的 placeholder **不配置** `replacement_pattern`/`content`，只配置 `subsections`；分节具体内容写在各子条的 `content` 中，建议新文本保留与原分项一致的 a）b）c）d）编号。
>
> **5.3 c)/d) 合并段落说明**：模板中 5.3 的 c）、d）两项为同一段落，`5.3.3` 子条的 `content` 用换行拆成两行分别承载。

**表格填充**（第 3 章职责分工表）：
```json
{
  "id": "3",
  "tables": [{
    "table_id": "organization_responsibilities",
    "locator_rows": [["角色", "人员", "管理范围和职责"]],
    "data_start_row": 1,
    "preserve_tail_rows": 0,
    "columns": ["role", "person", "responsibility"],
    "rows": [
      { "role": "项目负责人", "person": "王工", "responsibility": "定期检查项目的配置管理工作" }
    ]
  }]
}
```

### 处理规则

1. 静态章节与静态 placeholder 只修改其 `content`；分项 placeholder 的引言 `content` 与各子条 `content` 均只修改内容值
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern`、子条的 `replacement_pattern` 等模板结构字段
3. `subsections` 的 key 必须按章节编号排序有效（如 `"5.2.1"`），子条 `content` 不允许为空（无内容时按 `references/style-rules.md` 如实陈述，如"本项目当前无……"）
4. `rows` 中每行的字段必须严格等于 `columns` 定义；`person` 列的人员未定时写"由项目组指定"并列入待确认清单，不得编造真实人名
5. 第 2 章引用文档无表格，以 `content` 多行文本列举（每行一条：编号 标题（来源，日期））

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
  --template "documents/[03]软件配置管理计划-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[03]软件配置管理计划-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
