---
name: word-fillter-438C-30
description: "当用户提到「按照438C模板填写word文档」「软件安全性设计」「安全性设计」「安全关键软件设计」「438C」「SSDD」时触发。交互式填写 GJB 438C [30] 软件安全性设计模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[30]软件安全性设计-438C.docx` 模板生成或修改 GJB 438C 软件安全性设计文档时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[30]软件安全性设计-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容（第 3 章为展平 placeholders 数组）
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷、本文档特殊性）
- `references/terminology.md`：军用软件术语表（安全关键软件、N版本程序设计、恢复块、监控定时器等）
- `references/style-rules.md`：句式与表达规范（设计准则句式、量化指标、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：依赖 scripts/ 内路径约定，常规请用 main.py）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；特别留意看门狗、超时检测、参数校验、报警、容错、故障记录等安全性相关模块；
   - 若用户提供了建设方案、SRS 等文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、危险源与安全性要求作为补充素材；
   - 写入规则：文档中的模块名、接口名、机制描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 标识由 config.json 自动填写，**无 placeholder**；1.2/1.3 在模板中无指导文字，**不要添加 placeholder**
   - 第 2 章（引用文档）：使用 `tables` 填写引用文档表
   - 第 3 章（软件安全性设计）：约 240 个 `placeholders` 数组项，覆盖全部指导/列举段落（含 a～x 准则清单逐项）
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；**先读「本文档的特殊性」一节**（展平 id 规则、1.2/1.3 无指导文字、第 3 章标题即文档名等）；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：设计准则句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、写作依据、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全、准则是否逐条响应、不适用项是否如实陈述、列举序号是否与模板原文衔接、模块与机制描述是否与源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

> **document.title 固定为「软件安全性设计」**：本模板第 3 章一级标题与文档同名，"软件安全性设计"在封面两处与第 3 章标题共出现 3 处，引擎会同时替换这三处；填其它标题会把第 3 章标题一并改掉。

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

### 章节结构（第 3 章展平结构，重要）

[30] 模板第 3 章为层级最深四级的准则清单结构，`project.json` 中**展平为 `placeholders` 数组**：每个含指导/列举文字的段落对应一项：

```json
{
  "id": "3.8.2.1",
  "name": "监控定时器的设计",
  "type": "text_generation",
  "description": "第3章「监控定时器的设计」第1段指导文字",
  "replacement_pattern": "    a.必须提供监控定时器或类似措施……",
  "content": "    a.本软件提供由独立硬件监控定时器……"
}
```

id 规则：首段 `id` 即所属标题的层级编号；同一标题含多个段落时，其余段落 `id` 为标题编号＋段内序号（从 2 起），如 `3.1.7.2`（3.1.7 节第 2 段）、`3.13.9.1.25`（通用类第 24 条准则）。**`replacement_pattern` 逐字等于模板段落原文（含段首 4 空格与列举字母），严禁修改。**

- 无 `subsections`、无动态章节：本模板不含 `3.2.X（软件能力）` 类 X 编号原型子节，`subsections` 机制不启用
- 表格填充（第 2 章引用文档表）：

```json
{
  "table_id": "reference_documents",
  "locator_rows": [["序号", "名称", "版本", "发布日期", "来源"]],
  "data_start_row": 1,
  "preserve_tail_rows": 0,
  "columns": ["number", "name", "version", "release_date", "source"],
  "rows": [{"number": "1", "name": "...", "version": "...", "release_date": "...", "source": "..."}]
}
```

### 处理规则

1. 只修改各 placeholder 的 `content`；不修改 `id`、`type`、`replacement_pattern`、`description` 等结构字段
2. 列举型条目（a. b. c. …）的 `content` **保留原列举字母**开头（如 `a.本软件……`），段首保持 4 空格缩进
3. 模板原文有明显排字误差（"藕合""内顺""公共变""FQRTRAN"等）时，`replacement_pattern` 逐字保留原文，`content` 中用正确写法
4. `rows` 中每行的字段必须严格等于 `columns` 定义
5. 不适用本项目的准则，content 如实写"本软件不涉及……"并说明原因，禁止留空（引擎拒绝空 content）

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格，修改后会报错 `期望命中 1 张表，实际 0 张`。

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[30]软件安全性设计-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[30]软件安全性设计-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需按 scripts/process.py 内路径约定放置文件，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
