---
name: word-fillter-438C-17
description: "当用户提到「按照438C模板填写word文档」「软件测试记录」「测试记录」「438C」「STR」「Software Test Record」时触发。交互式填写 GJB 438C [17] 软件测试记录模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[17]软件测试记录-438C.docx` 模板生成或修改 GJB 438C 软件测试记录时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[17]软件测试记录-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、测试记录标题和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷、已知限制）
- `references/terminology.md`：军用软件术语表（CSCI、CSU、测试用例标识等）
- `references/style-rules.md`：句式与表达规范（记录句式、量化指标、如实陈述原则）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、对外接口/API、依赖关系；
   - 收集测试相关文档（测试计划、测试说明、需求规格说明），提取测试项、测试用例标识和量化性能指标作为事实依据；
   - 写入规则：文档中的测试项、用例标识、指标数值必须与测试文档事实一致，禁止编造未执行的测试和未实测的数据；源码或测试文档无法支撑的条目，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 文件更改记录表（structure."0"）填写 `rows`
   - 第 1 章（范围）1.1 标识使用 `placeholders`；1.2 被测软件概述模板无锚点，见 references/writing-guide.md 已知限制
   - 第 2 章（引用文件）使用 `tables`
   - 第 3 章（测评环境说明）使用 `tables`（软件环境、硬件环境、环境差异分析）
   - 第 4 章（测试记录）使用 `placeholders`（测试记录标题、指标要求、系统测试说明）和 `tables`（性能测试记录）；测试记录正文表格（文档齐套审查、功能测试）为合并单元格表格，引擎不填充、保留空白网格，由测试执行时手工填写
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件：4.2 下 4.2.1～4.2.3 为引擎置空的占位标题，按 references/writing-guide.md「4.2」小节手工重命名或删除；首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度、常见缺陷与已知限制；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：记录句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像与测试文档生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——测试项与用例标识是否与测试说明一致、指标是否量化（数值＋单位）、无测试的条目是否如实陈述、环境表与测评实际环境是否一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项（如无实测依据的性能指标、待补的测试用例标识），在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

| 字段位置 | type | 说明 | content 生成方式 |
|----------|------|------|-----------------|
| project.* | `original_text` | 项目基础信息（名称、版本、单位等） | 直接使用用户输入 |
| document.* | `original_text` | 文档元信息（编号、标题、日期等） | 直接使用用户输入 |
| content.overview | `background_information` | 被测软件概述 | 结合用户描述生成 |
| content.scope | `background_information` | 测试记录覆盖范围 | 结合用户描述生成 |
| content.features | `background_information` | 被测功能特性/测试类型 | 结合用户描述生成 |

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
  "id": "4.1.1",
  "name": "文档审查测试记录标题",
  "type": "content_generation",
  "replacement_pattern": "XXX文档审查测试/XXX标识",
  "content": "文档齐套审查测试/STR-DR-001"
}
```

**表格填充**：
```json
{
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
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. `rows` 中每行的字段必须严格等于 `columns` 定义
4. **排序约束（重要）**：第 4 章 `placeholders` 数组中 4.1.3（4.1.X 重复原型行）必须排在 4.1.2.1（功能测试记录表表题）之前，否则 4.1.2.1 的锚点会同时命中两个段落而报错；调整章节顺序时不得破坏该次序
5. **置空机制**：4.2 下 3 个相同的原型标题"XXX测试/XXX标识"由引擎统一置空（loader 封面规则块），测试项信息在 4.2 正文中汇总，不得为其编造多个相同标题

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。
> 其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符（如"页 次"中的空格、"测试\n次数"中的换行）。
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
  --template "documents/[17]软件测试记录-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[17]软件测试记录-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
