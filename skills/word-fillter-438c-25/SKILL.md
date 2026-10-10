---
name: word-fillter-438C-25
description: "当用户提到「按照438C模板填写word文档」「软件产品规格说明」「产品规格」「SPS」「Software Product Specification」「438C」时触发。交互式填写 GJB 438C [25] 软件产品规格说明书模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[25]软件产品规格说明-438C.docx` 模板生成或修改 GJB 438C 软件产品规格说明书时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[25]软件产品规格说明-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容与子条目
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、SPS、有效拷贝等）
- `references/style-rules.md`：句式与表达规范（陈述句式、量化指标、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录与交付物目录，形成「项目画像」：识别交付物清单（可执行程序、脚本、配置文件、数据文件）、源代码文件结构与模块划分、构建脚本（Makefile/CI 配置）、对外接口/API；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、交付物构成作为补充素材；
   - 写入规则：文档中的文件名、模块名、命令与选项必须与源码和交付物事实一致，禁止编造不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组
   - 第 2 章（引用文档）为段落式引用清单（本模板无表格），用 a）b）c）分级列举
   - 第 3 章（需求）含引言与 3.1 可执行软件、3.2 源文件、3.3 包装需求三个 `placeholders`
   - 第 4 章（合格性规定）为段落式合格性方法
   - 第 5 章（软件支持信息）含 5.1～5.4 四个 `placeholders`；5.3 修改规程与 5.4 计算机硬件资源使用的模板 a）～e）列举段配置为独立子条目（5.3-a～5.3-e、5.4-a～5.4-e），逐段改写为实际内容
   - 第 6 章（需求的可追踪性）含引言与 6-a～6-d 四个追踪性子条目
   - 第 7 章（注释）为静态章节（术语和缩略语）
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：陈述句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——交付物清单是否与实际文件一致、有效拷贝判据是否写出、编译/建立规程要素是否齐全（a～e）、资源使用数据是否注明测量条件、章节号引用是否真实存在、量化指标无依据时是否标注"待与用户确认"。
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

**静态章节/子条目**：
```json
{
  "id": "3.1",
  "name": "可执行软件",
  "type": "content_generation",
  "replacement_pattern": "锚点文本...",
  "content": "string"
}
```

> **[25] 模板全部为静态章节**：本模板没有 `X` 占位的原型子节，`INSERTION_PARENT_RULES` 为空，不支持 `subsections` 动态章节写法；`subsections` 仅可用于带 `replacement_pattern` 的静态子条目。
>
> **模板 a）～e）列举段的子条目写法（5.3/5.4/6 章）**：这些章的模板自带 a）～e）指导列举段是独立段落，配置为 id 带后缀的 `placeholders`（如 `5.3-a`、`5.3-bc`、`5.4-a`～`5.4-e`、`6-a`～`6-d`），每个子条目的 `replacement_pattern` 逐字等于对应列举段原文（注意 5.3 的 b）与 c）在模板中合并为一个段落，故合并为 `5.3-bc` 一条、content 内用换行分成两段）；`content` 用全角括号 a）b）c）重写为实际内容。引擎按 `id`/`name`/`replacement_pattern`/`content` 平铺解析，子条目 id 不参与文档编号。

**表格填充**：
```json
{
  "id": "2",
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

> **[25] 模板正文无数据表格**：第 2 章引用文档、第 4 章合格性规定均为段落式内容，不配 `tables`；表格填充机制仅封面/签署页/文件更改记录表使用，出厂不配置。

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`
2. 不修改 `id`、`type`、`columns`、`locator_rows`、placeholder 级的 `name` 与 `replacement_pattern` 等模板结构字段
3. 5.3/5.4/6 章的子条目（`5.3-a` 等）同样只修改 `content`；其子条目 `replacement_pattern` 必须与模板列举段原文逐字一致
4. 无实质内容可写的条目如实写"无……"类陈述，不留空（引擎拒绝空 content）
5. `rows` 中每行的字段必须严格等于 `columns` 定义（本模板默认无表格，通常不涉及）

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。
> 其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符。
>
> 修改后会导致报错 `期望命中 1 张表，实际 0 张`。

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[25]软件产品规格说明-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[25]软件产品规格说明-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
