---
name: word-fillter-438C-18
description: "当用户提到「按照438C模板填写word文档」「测评大纲」「软件测评」「测试大纲」「STO」「438C」时触发。交互式填写 GJB 438C [18] 软件测评大纲模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[18]软件测评大纲-438C.docx` 模板生成或修改 GJB 438C 软件测评大纲时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[18]软件测评大纲-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、子章节和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件测评术语表（CSCI、测试项、问题等级等）
- `references/style-rules.md`：句式与表达规范（测评句式、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案、研制总要求或需求规格说明文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、战技指标、功能要求作为补充素材；
   - 写入规则：文档中的模块名、接口名、测试对象描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写被测软件名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 标识由 config.json 驱动，本章无其他可填占位（1.2 需生成后手工编写）
   - 第 2 章（测评环境）：使用 `tables`（软件环境、硬件环境、环境差异分析三张表）和 2.1 表题 placeholder
   - 第 4 章（测试内容与方法）：使用 `placeholders`（4.3 测试定义的各测试类别标题与测试项说明、4.4 充分性分析、4.5 问题类型与等级）和 `tables`（战技指标追踪表）
   - 第 6 章（测评工作安排）：使用 `tables`（项目组成员、测评进度两张表）
   - 第 7 章（配置管理）：使用 `tables`（人员与职责表）
   - 第 8 章（质量保证）：使用 `tables`（质量保证小组组成表）
   - 其余章节（1.2、2.2、2.3、3、4.1、4.2、5、9、10、11）模板无占位文字，**引擎无法填写**，生成后在 Word 中手工编写（见 `references/writing-guide.md` 各节"引擎边界"）
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件：手工编写引擎未覆盖的章节，并在 Word 中手工填写 4.3.1～4.3.3 的三张测试项定义表；首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：测评句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全、测试项标识前缀是否与 project.short_name 一致、无内容的类别是否如实陈述、章节号引用是否真实存在、测试对象与接口描述是否与第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

| 字段位置 | type | 说明 | content 生成方式 |
|----------|------|------|-----------------|
| project.* | `original_text` | 被测软件基础信息（名称、缩写、版本、单位等） | 直接使用用户输入 |
| document.* | `original_text` | 文档元信息（编号、标题、密级、阶段、日期等） | 直接使用用户输入 |
| content.overview | `background_information` | 被测软件概述（供 1.2 手工编写与各章生成取素材） | 结合用户描述生成 |
| content.scope | `background_information` | 测评范围（供各章生成界定边界） | 结合用户描述生成 |
| content.features | `background_information` | 测试特性（供 4.3 测试定义取素材） | 结合用户描述生成 |

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 用户需求生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入 |

### 章节结构类型

**静态章节占位**（无 subsections）：
```json
{
  "id": "4.4",
  "name": "测试内容充分性及测试方法适合性分析",
  "type": "content_generation",
  "replacement_pattern": "测试内容充分性分析",
  "content": "string"
}
```

**带子条的占位**（4.3 测试定义）：
```json
{
  "id": "4.3",
  "name": "测试定义",
  "type": "content_generation",
  "generation_prompt": "生成子条的提示...",
  "content": "string（写作导引，引擎不替换正文）",
  "subsections": {
    "4.3.1": { "name": "文档审查", "replacement_pattern": "文档审查/XX_DOI", "content": "文档审查/XT_DOI" },
    "4.3.1.1": { "name": "文档审查测试项说明", "replacement_pattern": "文档审查测试项说明", "content": "string" }
  }
}
```

> **4.3 测试定义的机制约束（重要）**
> 子条的 `replacement_pattern` 是模板中的原文锚点，`content` 是替换后的全文：编号级子条（4.3.1 等）的 content 是新的测试类别标题（如"文档审查/XT_DOI"），说明级子条（4.3.1.1 等）的 content 是该类别的测试项说明正文。`4.3` 占位自身没有 `replacement_pattern`，其 `content` 仅为写作导引，引擎不会用它在文档中找锚点。
> 子条中的 `name` 应简述子条用途，保持中文开头。

**表格填充**：
```json
{
  "id": "2",
  "tables": [{
    "table_id": "software_environment",
    "locator_rows": [["序号", "软件名称", "版本号", "用途", "来源", "密级"]],
    "data_start_row": 1,
    "preserve_tail_rows": 0,
    "columns": ["number", "name", "version", "purpose", "source", "classification"],
    "rows": [
      { "number": "1", "name": "...", "version": "...", "purpose": "...", "source": "...", "classification": "..." }
    ]
  }]
}
```

### 处理规则

1. 只修改各占位（placeholder/子条）的 `content` 与表格的 `rows`；无锚点章节（1.2、2.2、2.3、3、4.1、4.2、5、9、10、11）只有 `description`，不得为其编造 `replacement_pattern`（锚点不存在会报"期望命中 1 个段落，实际 0 个"）
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 表格 `rows` 中每行的字段必须严格等于 `columns` 定义；模板数据行多于所填行时，多余行会被清空，请按需补充行数（引擎自动克隆行模板）
4. **以下模板表格不在可配置范围，禁止在 project.json 中为其配置 tables**：
   - 4.3.1～4.3.3 的三张测试项定义表——表头结构完全相同，引擎按表头定位时无法区分（会命中 3 张表而报错），生成后在 Word 中逐张手工填写；
   - 7.3.1 配置基线计划表、8.1.2 质量活动进度安排表——模板已预填内容，引擎填充会清空模板行，生成后在 Word 中核对修订
5. 表题（表-X、表6-X、表7-X、表8-X）由引擎自动重编号（如"表-X"→"表 2-1"），无需配置、无需手工改写

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。
> 其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符（如"型  号"中的两个空格、"工作量\n（人日）"中的换行）。
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
  --template "documents/[18]软件测评大纲-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[18]软件测评大纲-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
