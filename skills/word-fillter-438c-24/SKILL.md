---
name: word-fillter-438C-24
description: "当用户提到「按照438C模板填写word文档」「软件版本说明」「版本说明」「438C」「SVD」「Software Version Description」「发布说明」时触发。交互式填写 GJB 438C [24] 软件版本说明模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[24]软件版本说明-438C.docx` 模板生成或修改 GJB 438C 软件版本说明（SVD）时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[24]软件版本说明-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、SVD、适应性数据、已知错误等）
- `references/style-rules.md`：句式与表达规范（陈述句式、六要素完整、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、构建产物（可执行程序/配置文件/数据文件）、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 收集版本发布信息：上一基线以来的变更记录、问题跟踪单、交付物清单、安装/部署方式；
   - 写入规则：文档中的文件名、模块名、更改记录必须与源码和配置库事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节（如发布介质形式、求助联系地点），提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1 标识、1.2 系统概述、1.3 文档概述）
   - 第 2 章（引用文档）为静态章节，直接修改 `content`（本模板第 2 章无表格，引用文档以文字清单书写）
   - 第 3 章（版本说明）使用 `placeholders` 数组（3.1～3.7），其中 3.6 安装说明拆分为 `3.6`、`3.6.1`～`3.6.4` 共 5 个 placeholder（见下文「3.6 安装说明的拆分机制」）
   - 第 4 章（注释）为静态章节，写术语和缩略语
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：陈述句式、六要素完整、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——六要素（标识号/标题/缩略名/日期/版本号/发布号）是否齐全、初始版本是否如实陈述"本条不适用"、安装检查规程是否可执行、已知错误是否给出规避与纠正措施、文件名与交付介质是否一致。
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
| `original_text` | 原始文本 | 直接使用用户输入 |

### 章节结构类型

**静态章节/条目**（本模板全部为静态条目，无动态章节、无数据表格）：
```json
{
  "id": "3.1",
  "name": "发布的材料清单",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**3.6 安装说明的拆分机制（重要）**

模板把 3.6 的安装指导文字分散在 5 个连续段落中（引言+a）项、b）项、c）项、d）项、e）项，其中 a）b）两项合并在同一段落）。project.json 对应 5 个 placeholder：

| placeholder id | 承接内容 | 说明 |
|----------------|----------|------|
| `3.6` | 引言句 + a）安装软件版本的说明 | 锚点为模板引言段 |
| `3.6.1` | b）应安装的其他更改的标识 | 锚点覆盖模板中 a）b）合并段，content 只写 b）项 |
| `3.6.2` | c）与安装有关的保密性和安全性提示 | |
| `3.6.3` | d）判定版本是否正确安装的规程 | |
| `3.6.4` | e）安装中遇到问题后的求助联系地点 | |

`3.6.1`～`3.6.4` 是普通 placeholder（不是子章节、不是动态章节），其 `content` 写对应清单项内容；不要把五项全部堆进 `3.6` 的 `content`。

### 处理规则

1. 所有 placeholder 只修改其 `content`；`id`、`type`、`replacement_pattern`、`name` 等模板结构字段不得修改
2. 本模板正文无数据表格（第 2 章引用文档以文字清单写在 `content` 中；封面后的「文件更改记录表」为前置管理表格，不在填写范围）
3. 无动态章节（无 X 占位子节），`subsections` 机制本模板不使用
4. 确实无内容的条目（如初始版本的 3.3 更改说明、无适应性数据的 3.4）如实写"本条不适用"类陈述，不留空（引擎拒绝空 content）

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[24]软件版本说明-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[24]软件版本说明-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
