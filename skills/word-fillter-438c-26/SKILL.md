---
name: word-fillter-438C-26
description: "当用户提到「按照438C模板填写word文档」「软件质量保证报告」「质量报告」「质量保证」「SQAR」「SQA」「[26]」时触发。交互式填写 GJB 438C [26] 软件质量保证报告模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[26]软件质量保证报告-438C.docx` 模板生成或修改 GJB 438C 软件质量保证报告时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构

# 目录结构

- `documents/[26]软件质量保证报告-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容（本模板无数据表格、无动态章节，全部为静态章节条目）
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷、模板已知怪癖）
- `references/terminology.md`：军用软件术语表（CSCI、基线、三库、评审归零、第三方测评等）
- `references/style-rules.md`：句式与表达规范（总结报告句式、量化指标、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 收集用户提供的质量记录类素材：软件质量保证计划、评审记录、测试报告、配置管理报告、第三方测评报告、风险管理记录等（.docx 用 python-docx 读取，.md/.txt 直接读取）；
   - 若用户指定了项目源码目录，扫描形成「项目画像」（开发语言、模块划分、功能特性），用于 1.2/3.3 中软件功能与范围的描述；
   - 写入规则：文档中的组织职责、评审次数、问题数、覆盖率、指标实测值必须与素材事实一致，禁止编造；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1 标识、1.2 系统概述、1.3 文档概述）
   - 第 2 章（引用文档）为静态章节，逐条列出引用文档
   - 第 3 章（质量目标和要求的完成情况）使用 `placeholders` 数组（3.1 质量保证组织、3.2 质量目标完成情况、3.3 质量要求完成情况）
   - 第 4 章（质量管理）为静态引言 + `placeholders` 数组（4.1.1～4.1.5、4.2、4.3.1、4.3.2、4.4、4.5/4.6 节的标题与正文条目），其中 `4.5.title`、`4.5.1.title`、`4.5.2.title`、`4.6.1.title`、`4.6.2.title` 是 X 占位遗留标题的替换项，`4.5.1`/`4.6.1` 是评审结论/测评结果正文条目
   - 第 5 章（项目风险监控）、第 6 章（记录的管理情况）、第 7 章（质量审核和质量监督的落实）、第 8 章（注解）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷（**先读「模板已知怪癖」一节**，了解 9.5.X/9.6.X 遗留编号、4.1.4 空四级标题、4.5.2/4.6.2 共用改进陈述等模板缺陷的处理方式）；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：总结报告句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步收集的质量素材生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全（目标值＋达成值）、评审问题是否有归零闭环、单位/机构名称是否留白待确认、文档编号全文一致、引用文档是否真实存在。
4. **再写入**：自查通过后写入 `content`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

| 字段位置 | type | 说明 | content 生成方式 |
|----------|------|------|-----------------|
| project.* | `original_text` | 项目基础信息（名称、版本、单位等） | 直接使用用户输入 |
| document.* | `original_text` | 文档元信息（编号、标题、密级、阶段、日期等） | 直接使用用户输入 |
| content.overview | `background_information` | 项目概述 | 结合用户描述生成 |
| content.scope | `background_information` | 项目范围 | 结合用户描述生成 |
| content.features | `background_information` | 功能特性 | 结合用户描述生成 |

## project.json

### type 取值

| type | 说明 | content 生成方式 |
|------|------|-----------------|
| `content_generation` | 根据提示生成内容 | 结合 `generation_prompt` + 素材生成 |
| `text_generation` | 文本生成（较简单） | 根据用户描述生成 |
| `original_text` | 原始文本 | 直接使用用户输入（如 4.5.title 等标题替换项） |

### 章节结构类型

本模板全部为**静态章节**（无 `subsections`、无 `tables`），统一结构：

```json
{
  "id": "4.2",
  "name": "测试过程",
  "type": "content_generation",
  "replacement_pattern": "锚点文本（模板引导文字原文）",
  "content": "string"
}
```

- `replacement_pattern` 必须与模板中的引导文字**逐字一致**（含标点），引擎用包含匹配定位该段落并以 `content` 替换；多行 `content`（`\n` 分隔）会生成多个连续段落。
- 第 4 章除 `placeholders` 外还有一个特殊字段 `duplicate_guidance_shared_content`：模板 4.5.2 与 4.6.2 两处引导文字逐字相同（"描述改进落实情况。"），引擎无法分别定位，改用一次全等匹配将两处替换为这句共用陈述。**不要删除该字段、不要改其字段名**；如需两处不同内容，生成后在 Word 中手动拆分。

### 处理规则

1. 只修改各条目的 `content` 值，不修改 `id`、`type`、`name`、`replacement_pattern` 等结构字段
2. 无实质内容可写的条目，如实写"无……"类陈述，不留空（引擎拒绝空 content）
3. 章节号引用与本文档实际章节一致（第 3 章质量目标和要求的完成情况、第 4 章质量管理、第 5 章项目风险监控、第 6 章记录的管理情况、第 7 章质量审核和质量监督的落实）

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[26]软件质量保证报告-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[26]软件质量保证报告-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
