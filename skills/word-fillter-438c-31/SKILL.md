---
name: word-fillter-438C-31
description: "当用户提到「按照438C模板填写word文档」「软件配置管理报告」「配置管理报告」「配置管理」「438C」「CMR」「SCM report」时触发。交互式填写 GJB 438C [31] 软件配置管理报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[31]软件配置管理报告-438C.docx` 模板生成或修改 GJB 438C 软件配置管理报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构
- 本模板为纯文本骨架：正文第 2～14 章均只有指导段落，无数据表格、无 X 占位动态子节；`project.json` 不需要也不能配置 `tables`/`subsections`

# 目录结构

- `documents/[31]软件配置管理报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容配置
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件配置管理术语表（CI、基线、CCB、配置审核等）
- `references/style-rules.md`：陈述句式、量化指标、如实陈述原则与禁用表达
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 若用户能提供配置库（如 git/svn 仓库）信息，形成「配置管理画像」：模块划分与目录结构（支撑第 6 章配置项）、提交历史与里程碑标签（支撑第 7、8 章变更与基线）、分支/合并记录（支撑第 9、10 章出入库）、评审与检查记录（支撑第 11 章审核）；
   - 若用户提供了建设方案或计划类文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取项目背景、组织分工、进度安排作为补充素材；
   - 写入规则：配置项名称、模块名、单据编号必须与素材事实一致，禁止编造素材中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1 标识、1.2 系统概述、1.3 文档概述）
   - 第 2～14 章（引用文档、配置管理情况综述、基本信息、专业组划分、配置项记录、变更记录、基线记录、入库记录、出库记录、审核记录、备份记录、测量、注释）均为静态章节，每章一个 `replacement_pattern` 锚点，只修改其 `content`
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：配置管理术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：陈述句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的配置管理画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——必填要素是否齐全（单据号、日期、人员、数量）、各章统计数字是否相互一致（第 3 章综述与第 7/9/10/11/13 章）、无活动的条目是否如实陈述、章节号引用是否真实存在、配置项划分是否与素材一致。
4. **再写入**：自查通过后写入 `content`，保持 JSON 结构不变。
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

本模板全部为**静态章节**（无 `subsections`、无 `tables`）：

```json
{
  "id": "3",
  "title": "软件配置管理情况综述",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

第 1 章为 `placeholders` 数组（1.1/1.2/1.3 三个 placeholder，结构同上，含 `id`/`name`）。

### 处理规则

1. 静态章节只修改其 `content`；每章 `replacement_pattern` 已按模板指导文字原文配置，**严禁修改**
2. 不修改 `id`、`type`、顶层章节的 `title` 与 `replacement_pattern` 等模板结构字段
3. content 中的换行符 `\n` 会生成独立段落：条内列举（配置项、变更、测量指标等）建议每项一行
4. 无实质内容可写的章节如实写"报告期内无……"类陈述，引擎拒绝空 content

> **统计一致性（重要）**：第 3 章（综述）、第 7 章（变更）、第 9/10 章（出入库）、第 11 章（审核）、第 13 章（测量）之间的数量必须相互一致（变更总数＝批准＋拒绝；入库单份数＝第 9 章条数等）。填写完成后按 `references/style-rules.md` 第 2 条逐项核对。

> **`replacement_pattern` 严禁修改！**
> `replacement_pattern` 是引擎在模板 docx 中定位指导段落的锚点，其中的文本必须与模板 docx 中的实际段落文字完全一致（包括全角标点）。
> 修改后会导致报错 `期望命中 1 个段落，实际 0 个`。
>
> 若不确定实际文本，用以下脚本提取：
> ```python
> from docx import Document
> doc = Document("模板文件.docx")
> for i, p in enumerate(doc.paragraphs):
>     if p.text.strip():
>         print(i, repr(p.text))
> ```

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[31]软件配置管理报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[31]软件配置管理报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
