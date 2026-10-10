---
name: word-fillter-438C-20
description: "当用户提到「按照438C模板填写word文档」「软件用户手册」「用户手册」「使用手册」「438C」「SUM」时触发。交互式填写 GJB 438C [20] 软件用户手册模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[20]软件用户手册-438C.docx` 模板生成或修改 GJB 438C 软件用户手册时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[20]软件用户手册-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容与子条（a）～e）类条目）数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、SUM、MTBF 等）
- `references/style-rules.md`：句式与表达规范（操作句式、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系、界面路由、命令行参数、错误码/消息定义、定时任务与部署脚本；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的模块名、菜单名、参数名、文件名、消息编号必须与软件事实一致，禁止编造软件中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1～1.3）
   - 第 2 章（引用文档）为章节级 `content` 段落陈述，**本模板无引用文档表格**
   - 第 3 章（软件综述）使用 `placeholders` 数组（3.1～3.7），其中 3.3 的 a）～e）、3.4 的 a）～d）及 b）下 1）～7）为静态子条
   - 第 4 章（软件入门）使用 `placeholders` 数组，4.1 的 4.1.1～4.1.3 为静态子条（其下 a）～e）、a）～c）再作为 4.1 的平铺子条）
   - 第 5 章（使用指南）为章节级引言 `content` 加 `placeholders` 数组（5.1～5.8），5.3 见下方机制约束
   - 第 6 章（注释）为章节级 `content`
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：操作句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——性能特性是否量化、规程是否逐步可执行、无内容的条目是否如实陈述、章节号引用是否真实存在、菜单/参数/消息名是否第 0 步的软件事实一致、全文是否无具体单位名称。
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

**静态章节**（无子条）：
```json
{
  "id": "3.1",
  "name": "软件应用",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**带子条的静态章节**（如 3.3、3.4、4.1、5.3；子条只替换对应段落，不生成新标题）：
```json
{
  "id": "3.3",
  "name": "软件环境",
  "type": "content_generation",
  "replacement_pattern": "本条应描述用户安装并运行该软件所需的硬件、软件、手工操作和其他的资源。",
  "content": "用户安装并运行本软件所需的资源如下：",
  "subsections": {
    "3.3.1": { "name": "计算机设备", "replacement_pattern": "a)应提供的计算机设备...", "content": "a）应提供的计算机设备：……" }
  }
}
```

> **静态子条的机制约束（重要）**
> 子条 `replacement_pattern` 逐字等于模板中对应段落（含 a）～e）编号、全/半角标点）；子条 `content` 写入后**保留原编号字母**（如替换 a）段落的 content 仍以"a）"开头）。子条 `name` 仅用于 JSON 阅读，不写入文档。键名为层级式编号（如 4.1 的 a）～e）子条键为 4.1.1.1～4.1.1.5），仅用于排序与阅读。

> **5.3 处理规程的机制约束（重要，涉及 5.3/5.3.1）**
> 本模板的 5.3 仅含一个 `5.3.X(软件使用方面)` 原型标题段落及其指导段落，引擎按静态方式填充：
> - placeholder `5.3` 的 `content` **即新的三级标题文本**，必须写成「5.3.1 ＋使用方面名称」格式（如"5.3.1 任务调度处理"），引擎将其整体替换模板原型标题；
> - 子条 `5.3.1` 的 `content` 为该使用方面的正文规程（换行生成独立段落），建议按「功能描述／菜单与数据项／用户输入／输出／诊断或错误消息／报警／帮助工具」分行书写；
> - 输出文档只生成一个 5.3.1 条目：软件有多个使用方面时在 5.3.1 的 content 内分段或按 a）b）c）分别描述，**禁止为凑结构编造软件中不存在的功能**。详见 `references/writing-guide.md` 的「5.3 处理规程」小节。

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`；有子条的 placeholder 级 `content` 为该条引言（或 5.3 的标题行），同样只修改 `content`
2. 不修改 `id`、`type`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 子条只修改 `name`（阅读用）与 `content`；`replacement_pattern` 逐字对应模板段落，严禁修改——锚点不匹配会报"期望命中 1 个段落，实际 0 个"
4. 本模板**无动态章节**（无 `subsections` 自动生成标题的机制），**无数据表格**（引用文档、消息等均以正文段落/列表形式书写）；封面后的「文件更改记录表」由文档控制过程填写，不在本 skill 填写范围
5. 无实质内容可写的章节如实写"无……"类陈述并说明理由，不留空（引擎拒绝空 content）

> **锚点校验**
> `replacement_pattern` 必须与模板 docx 中的段落文本逐字一致（引擎为包含匹配，默认期望恰好命中 1 个段落），包括标点符号、全/半角括号、空格和模板原文的笔误（如 5.3.1 锚点中的"特性d描述"）。若不确定实际文本，用以下脚本提取：
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
  --template "documents/[20]软件用户手册-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[20]软件用户手册-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
