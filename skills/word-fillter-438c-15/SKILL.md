---
name: word-fillter-438C-15
description: "当用户提到「按照438C模板填写word文档」「软件测试计划」「测试计划」「438C」「STP」时触发。交互式填写 GJB 438C [15] 软件测试计划模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[15]软件测试计划-438C.docx` 模板生成或修改 GJB 438C 软件测试计划时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构

# 目录结构

- `documents/[15]软件测试计划-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、动态章节和测试项信息
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、STP、STD、STR 等）
- `references/style-rules.md`：句式与表达规范（计划句式、量化指标、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案或需求文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、功能清单、资源与周期约束作为补充素材；
   - 向用户收集测试环境信息（软硬件设备、提供方、人员名单）与测试周期约束，作为第 4、6 章的事实依据；
   - 写入规则：文档中的模块名、接口名、功能描述必须与源码事实一致，禁止编造源码中不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1～1.4）
   - 第 2 章（引用文档）、第 3 章（测试依据）为静态章节，修改其 `content`
   - 第 4 章（软件测试环境）使用 `4.X` 动态章节，`subsections` 每个子条为一个测试现场
   - 第 5 章（测试标识）5.1.1～5.1.5 为静态小节；5.2 计划执行的测试按 5.2、5.2.1、5.2.1.1 及 a）～j）逐项填写
   - 第 6 章（测试进度）章节引言 + 进度条目 a）、b）及其子项
   - 第 7 章（测试终止条件）、第 8 章（需求的可追踪性）、第 9 章（注释）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：计划句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全、计划安排是否有明确时间与责任人、无内容的条目是否如实陈述、章节号与测试项/需求标识符引用是否真实存在、模块与接口描述是否与第 0 步的源码事实一致、全文是否出现具体单位名称（必须无）。
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

**静态章节**（无 subsections）：
```json
{
  "id": "1.2",
  "name": "系统概述",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

**动态章节**（第 4 章测试现场，有 subsections）：
```json
{
  "id": "4.X",
  "name": "测试现场",
  "type": "content_generation",
  "generation_prompt": "生成子章节的提示...",
  "content": "string（本章引言）",
  "subsections": {
    "4.1": { "name": "任务实验室测试现场", "content": "软件项：...\n硬件和固件项：...\n..." },
    "4.2": { "name": "外场试验测试现场", "content": "string" }
  }
}
```

> **动态章节的机制约束（重要，涉及 4.X）**
> 引擎将 `4.X` 视为动态章节：`subsections` 中每个子条的 `name` 会作为二级标题写入文档、`content` 的每一行生成一个正文段落，且 `subsections` **不允许为空**（空则报错）。模板自带的 4.X.1～4.X.11 原型小条会被引擎整体删除，因此每个子条 `content` 必须按十一方面逐行书写（软件项／硬件和固件项／软硬件环境部署关系／其他材料／所有者的特性、需方权利和许可证／安装、测试和控制／测试环境的差异性分析和有效性说明／参与组织／人员及分工／人员培训／要执行的测试）。只有一个测试现场时只建一个子条并如实说明，**禁止为填满机制而编造多个现场**。子条 `name` 应以中文开头。

**测试项标题改写**（5.2、5.2.1 为 `original_text`）：
```json
{
  "id": "5.2",
  "name": "测试项标题",
  "type": "original_text",
  "replacement_pattern": "5.2.X(测试项)",
  "content": "5.2.1功能测试"
}
```
> `5.2` 与 `5.2.1` 将模板原型标题改写为实际测试项编号与名称；改写后的编号必须与 `5.2.1.1` 概述及 a）～j）各项中的测试项标识符一致。模板只有一个 5.2.X.Y 原型块，测试项多于一个时需在 Word 中复制该块后手工扩展。

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`；动态章节（4.X）placeholder 级的 `content` 为该节引言，同样只修改 `content`
2. 不修改 `id`、`type`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 动态章节 `subsections` 中每个子条的 `name` **会作为章节标题写入文档，必须改为实际测试现场名称**（以中文开头）；`content` 按十一方面逐行书写；子条中的 `replacement_pattern` 被引擎静默忽略，无需填写
4. `subsections` 的 key 必须是有效章节编号（如 `"4.1"`）
5. 5.2.1.1.a～5.2.1.1.j 对应模板 a）～j）十个列表项，逐项填写，条目内容首句应体现所答方面（如"测试对象：……"）

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[15]软件测试计划-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[15]软件测试计划-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
