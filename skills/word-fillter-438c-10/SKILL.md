---
name: word-fillter-438C-10
description: "当用户提到「438C 软件概要设计说明」「[10] 软件概要设计说明」「SDD」「概要设计模板填写」「设计说明」时触发。基于 GJB 438C [10] 软件概要设计说明模板，严格填写封面、章节内容、CSCI 体系结构块和追踪表，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[10]软件概要设计说明-438C.docx` 模板生成或修改 GJB 438C 软件概要设计说明时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[10]软件概要设计说明-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容、CSCI 结构和表格数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、CSC、HWCI、IDD 等）
- `references/style-rules.md`：句式与表达规范（设计决策句式、标识规范、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的模块名、接口名、功能描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组
   - 第 2 章（引用文档）使用 `tables`
   - 第 3 章（系统设计决策）为静态章节
   - 第 4 章（系统体系结构设计）使用 `cscis` 数组定义 CSCI 块
   - 第 5 章（需求可追踪性）使用 `tables`
   - 第 6 章（注释）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content`（含 `cscis` 各字段或表格 `rows`）时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：设计描述句式、标识与引用规范、概要设计定位和禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——决策是否带理由、部件/接口是否有项目唯一标识、动态行为是否覆盖例外处理、追踪表章节号是否真实存在、部件与接口描述是否第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`/`rows`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

所有字段只修改 `content` 值，结构与 [08] Skill 完全一致，包含 `project`、`document`、`content` 三部分。

## project.json

### 通用规则

- 普通章节（无 `cscis`/`tables` 的章节）只修改其 `content`；章节引言类 `content` 为摘要段
- `cscis` 数组中每个 CSCI 项的 9 个字段（`title`、`overview`、`component_design` 等）均为内容字段，按素材收集得到的项目画像填写
- 表格只修改 `rows`
- `locator_rows`、`columns`、章节编号和模板锚点不得改动

> **注意**：编辑 `templates/project.json` 前先用 `file` 或编辑器确认换行风格；若存在 CRLF/LF 混合换行，应对 `content`/`rows` 值做字节级精确替换，不要整文件重写或经编辑器另存（会统一行尾、制造大量无效 diff）。

### 第 4 章 cscis 结构

第 4 章使用 `cscis` 数组，每个 CSCI 项必须提供以下 9 个字段：

| 字段 | 说明 |
|------|------|
| `title` | CSCI 名称 |
| `overview` | CSCI 概述 |
| `component_title` | 部件标题 |
| `component_design` | 部件设计描述 |
| `execution_plan` | 执行计划 |
| `interface_overview` | 接口概述 |
| `interface_identification` | 接口标识规则 |
| `interface_detail_title` | 接口详细标题 |
| `interface_details` | 接口详细描述 |

> **`locator_rows` 严禁修改！**
> `locator_rows` 用于在模板 docx 中定位表格，脚本通过逐行比较单元格文本查找目标表格。
> 其中的文本必须与模板 docx 中的实际表头文本完全一致，包括标点符号、空格和特殊字符。
>
> 修改后会导致报错 `期望命中 1 张表，实际 0 张`。
>
> 若不确定实际表头文本，用以下脚本提取：
> ```python
> from docx import Document
> doc = Document("模板文件.docx")
> for i, table in enumerate(doc.tables):
>     for j, row in enumerate(table.rows[:3]):
>         print(f"Table {i} Row {j}: {[c.text.strip() for c in row.cells]}")
> ```

# 运行

安装依赖（首次）：

```bash
pip install -r scripts/requirements.txt
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[10]软件概要设计说明-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[10]软件概要设计说明-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
