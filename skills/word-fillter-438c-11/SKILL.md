---
name: word-fillter-438C-11
description: "当用户提到「按照438C模板填写word文档」「数据库设计说明」「数据库设计」「438C」「DBDD」「Database Design Description」时触发。交互式填写 GJB 438C [11] 数据库设计说明模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[11]数据库设计说明-GJB438C.docx` 模板生成或修改 GJB 438C 数据库设计说明时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构
- 本模板正文无数据表格（第 2 章引用文档、第 6 章追踪性均为正文段落），不要臆造 `tables` 配置

# 目录结构

- `documents/[11]数据库设计说明-GJB438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、动态设计级别子条和软件单元子条
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件与数据库术语表（DBDD、DBMS、数据元素、数据元素集合等）
- `references/style-rules.md`：句式与表达规范（设计决策句式、量化指标、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、数据库访问层代码（数据访问类/模块/SQL 或 ORM 定义）、建库脚本或表结构定义、数据备份/维护脚本、对外接口/API；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的表名、字段名、单元标识、接口描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1 标识 / 1.2 系统概述 / 1.3 文档概述）
   - 第 2 章（引用文档）为静态章节，正文逐条列出引用文档
   - 第 3 章（数据库级设计决策）为静态章节，逐项给出"决策＋理由"
   - 第 4 章（数据库详细设计）为动态章节，`subsections` 按设计级别（概念设计/逻辑设计/物理设计）建子条
   - 第 5 章（用于数据库访问或操纵的软件单元详细设计）为动态章节，`subsections` 按软件单元建子条
   - 第 6 章（需求可追踪性）为静态章节，含 6.1/6.2 两个正向/反向追踪条目
   - 第 7 章（注释）为静态章节（术语和缩略语）
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：设计决策句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——设计决策是否带理由、数据元素是否有类型/长度/取值范围、软件单元标识是否与代码一致、追踪条目章节号是否真实存在、表名字段名是否第 0 步的源码事实。
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

**动态章节**（4 / 5，有 subsections）：
```json
{
  "id": "4",
  "name": "数据库设计级别",
  "type": "content_generation",
  "generation_prompt": "生成子章节的提示...",
  "content": "string（本章引言）",
  "subsections": {
    "4.1": { "name": "概念设计", "content": "string" },
    "4.2": { "name": "逻辑设计", "content": "string" },
    "4.3": { "name": "物理设计", "content": "string" }
  }
}
```

> **动态章节的机制约束（重要，涉及 4 / 5 两章）**
> 引擎将这两章视为动态章节：`subsections` 中每个子条的 `name` 会作为章节标题写入文档（如 `4.1概念设计`）、`content` 作为正文段落，且 `subsections` **不允许为空**（空则报错）。
> 当数据库实际只有一个设计级别、软件实际只有一个访问单元时，**禁止为填满机制而编造多个子条**：只建一个子条并如实说明。子条中的 `replacement_pattern` 字段在动态模式下被引擎静默忽略，无需填写；子条 `name` 应以中文开头，避免标题出现"4.1REST…"这类数字与英文连排无空格的观感问题。

### 处理规则

1. 静态章节只修改其 `content`；动态章节（4/5）placeholder 级的 `content` 为该章引言，同样只修改 `content`
2. 不修改 `id`、`type`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 动态章节 `subsections` 中每个子条的 `name` **会作为章节标题写入文档，必须改为实际设计级别名/软件单元名**（以中文开头）；`content` 为该子条正文

> **模板说明**：
> - 本模板正文**没有数据表格**：第 2 章引用文档、第 6 章需求可追踪性均为正文段落，`project.json` 不含 `tables`，禁止自行添加表格配置。
> - 第 3 章 guidance 之后的"数据库级设计决策的例子"段落是模板自带的选题参考，引擎不会删除它们；填写的 `content` 应覆盖这些主题，但不要把示例原文当正文照抄。
> - 封面"产品型号-XXXX"一行在模板中带前导空格，引擎已按原样处理，用户无需关心。

# 运行

安装依赖（首次）：

```bash
pip install -r scripts/requirements.txt
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[11]数据库设计说明-GJB438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[11]数据库设计说明-GJB438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
