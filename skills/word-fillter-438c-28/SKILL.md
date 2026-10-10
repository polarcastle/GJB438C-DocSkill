---
name: word-fillter-438C-28
description: "当用户提到「按照438C模板填写word文档」「研制总结报告」「研制总结」「438C」「development summary」时触发。交互式填写 GJB 438C [28] 研制总结报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[28]研制总结报告-438C.docx` 模板生成或修改 GJB 438C 研制总结报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点或章节指导文字不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构

# 目录结构

- `documents/[28]研制总结报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容配置
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、基线、MTBF 等）
- `references/style-rules.md`：句式与表达规范（陈述句规范、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、关键类与函数、代码规模；
   - 收集研制过程记录：软件研制任务书、需求/设计/测试文档、测评报告、配置管理记录、问题归零记录；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标作为补充素材；
   - 写入规则：文档中的模块名、指标数值、测试结论、问题描述必须与素材事实一致，禁止编造素材中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）：1.1 标识、1.2 系统概述、1.3 文档概述三个 placeholder
   - 第 2～3 章（任务来源与研制依据、软件概述）：各 1 个 placeholder
   - 第 4 章（软件研制过程）：4.1～4.10 共 10 个 placeholder
   - 第 5～7 章（指标满足情况、主要研制成果、关键技术）：各 1 个 placeholder
   - 第 8～9 章（质量保证、配置管理）：8.1/8.2、9.1～9.3 共 5 个 placeholder
   - 第 10 章（测试和分析）：引言 `10` 与条目 `10-a`～`10-e` 共 6 个 placeholder
   - 第 11～13 章（研制成果评价、结论、注解）：各 1 个 placeholder
   - 本文档无内容数据表，模板的"文件更改记录表"为文档管理用表，保持空白、不填写
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：陈述句规范、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的事实生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——要素是否齐全、数值是否与素材一致、无事实依据的内容是否如实陈述、章节引用是否真实存在。
4. **再写入**：自查通过后写入 `content`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# 模板特殊机制（重要）

1. **1.2 系统概述的残句接续**：模板指导文字被断为两段，引擎只替换第一段，第二段残句"运行现场；并列出其它有关文档。"保留并自动接续在 content 末尾之后。content 最后一个分段必须以"……已标识了当前和计划的"结尾（详见 writing-guide.md「1.2」）。
2. **第 10 章的条目式 placeholder**：引言 id 为 `10`；a.～e. 五个数据条目各为独立 placeholder（id `10-a`～`10-e`），content 保留条目序号与结尾标点。
3. **第 11 章的统一评价**：11.1～11.5 子条标题下无指导段，五方面评价统一写在 placeholder `11` 的 content 中。
4. **封面文档名占位**：模板封面标题占位原文为"软件接口设计说明"（模板固有笔误），引擎会将其替换为 config.json 的 `document.title`（应填"研制总结报告"）。

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

### 章节结构

本文档全部为静态章节（无 subsections、无 tables）：

```json
{
  "id": "4.1",
  "name": "软件研制过程概述",
  "type": "content_generation",
  "replacement_pattern": "锚点文本（模板指导文字原文，严禁修改）",
  "content": "string"
}
```

### 处理规则

1. 只修改各 placeholder 的 `content`，不修改 `id`、`type`、`name`、`replacement_pattern` 等结构字段
2. `replacement_pattern` 逐字等于模板中的指导文字原文（含全角标点），锚点不匹配时引擎报错，禁止为跑通而修改锚点
3. content 不能为空（引擎拒绝空文本），无实质内容时如实写"无……"类陈述
4. content 中的换行符将生成独立段落；长内容按要点分段书写

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[28]研制总结报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[28]研制总结报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
