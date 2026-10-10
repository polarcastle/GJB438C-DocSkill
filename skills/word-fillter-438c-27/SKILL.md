---
name: word-fillter-438C-27
description: "当用户提到「按照438C模板填写word文档」「软件标准化工作报告」「标准化工作报告」「SWR」「标准化工作」时触发。交互式填写 GJB 438C [27] 软件标准化工作报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[27]软件标准化工作报告-438C.docx` 模板生成或修改 GJB 438C 软件标准化工作报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构

# 目录结构

- `documents/[27]软件标准化工作报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、第 5 章动态阶段子条
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（标准化、标准化审查、基线等）
- `references/style-rules.md`：句式与表达规范（工作陈述句式、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 收集研制过程记录：配置管理记录、阶段评审记录、标准化审查记录、测试记录、文档审签记录——本 Skill 生成的文档是**工作报告**，陈述的是已完成的标准化工作，事实依据以研制记录为主、源码为辅；
   - 若用户提供了建设方案或标准化大纲等文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、研制阶段划分、标准化要求作为补充素材；
   - 写入规则：文档中的阶段名称、文档名称、标准编号、问题统计必须与素材事实一致，禁止编造素材中不存在的工作内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1/1.2/1.3）
   - 第 2 章（引用文档）为章级 placeholder，模板无表格，用编号列举引用文档
   - 第 3 章（软件标准化工作概述）、第 4 章（标准化工作成果）为章级 placeholder
   - 第 5 章（软件标准化工作情况）为**动态章节**：placeholder 级 `content` 为本章引言，`subsections` 每个子条对应一个研制阶段，`content` 按"标准化分析／标准化确定／标准化保证／标准化审查"四行组织
   - 第 6 章（标准化要求实施情况）使用 `placeholders` 数组（6.1～6.4）
   - 第 7 章（标准化要求执行结果）、第 8 章（标准化工作的保障情况）、第 9 章（注释）为章级 placeholder
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：工作陈述句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像与研制记录生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——四个 aspect 是否齐全、句式是否符合"开展了/完成了"工作报告句式、无成果/无活动的条目是否如实陈述、阶段数与素材事实是否一致、引用标准编号是否真实存在。
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

**动态章节**（第 5 章，有 subsections）：
```json
{
  "id": "5",
  "name": "软件标准化工作情况",
  "type": "content_generation",
  "generation_prompt": "生成子章节的提示...",
  "content": "string（本章引言）",
  "subsections": {
    "5.1": { "name": "软件需求分析阶段", "content": "标准化分析：……\n标准化确定：……\n标准化保证：……\n标准化审查：……" },
    "5.2": { "name": "软件设计阶段", "content": "标准化分析：……\n标准化确定：……\n标准化保证：……\n标准化审查：……" }
  }
}
```

> **动态章节的机制约束（重要，涉及第 5 章）**
> 引擎将第 5 章视为动态章节：`subsections` 中每个子条的 `name` 会作为阶段标题写入文档（如"5.1 软件需求分析阶段"）、`content` 的每一行生成一个独立正文段落，且 `subsections` **不允许为空**（空则报错）。
> 当项目实际只有一个研制阶段时，**禁止为填满机制而编造多个阶段子条**：只建一个子条（如 `5.1`），`name` 如实命名（如"软件研制阶段"），`content` 照常按四个 aspect 分行陈述。详见 `references/writing-guide.md`「第 5 章」。
> 子条中的 `replacement_pattern` 字段在动态模式下被引擎静默忽略，无需填写；子条 `name` 应以中文开头，避免标题出现"5.1Design…"这类数字与英文连排无空格的观感问题。

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`；动态章节（第 5 章）placeholder 级的 `content` 为本章引言，同样只修改 `content`
2. 不修改 `id`、`type`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 动态章节 `subsections` 中每个子条的 `name` **会作为阶段标题写入文档，必须改为实际研制阶段名**（以中文开头）；`content` 按"标准化分析／标准化确定／标准化保证／标准化审查"四行书写，每行一个段落
4. `subsections` 的 key 必须是有效章节编号（如 `"5.1"`）
5. 本模板无章节数据表格，`project.json` 未配置 `tables`；封面表格（密级/阶段/版次/单位/日期）与文件更改记录表由引擎封面规则和模板自身处理，不在可编辑范围

> **`replacement_pattern` 严禁修改！**
> `replacement_pattern` 用于在模板 docx 中定位指导文字段落，脚本通过包含匹配查找目标段落且期望恰好命中 1 次。
> 其中的文本必须与模板 docx 中的实际文本完全一致，包括标点符号（全角/半角冒号、括号）和空格。
> 修改后会导致报错 `期望命中 1 个段落，实际 0 个`。
>
> 若不确定实际文本，用以下脚本提取：
> ```python
> from docx import Document
> doc = Document("模板文件.docx")
> for i, p in enumerate(doc.paragraphs):
>     if p.text.strip():
>         print(i, p.style.name if p.style else "", repr(p.text))
> ```

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[27]软件标准化工作报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[27]软件标准化工作报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
