---
name: word-fillter-438C-21
description: "当用户提到「按照438C模板填写word文档」「计算机编程手册」「编程手册」「438C」「CPM」「Computer Programming Manual」时触发。交互式填写 GJB 438C [21] 计算机编程手册模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[21]计算机编程手册-438C.docx` 模板生成或修改 GJB 438C 计算机编程手册时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、表格表头或章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段和 `rows` 数组，不得修改模板结构

# 目录结构

- `documents/[21]计算机编程手册-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容与固定子条数据
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、CPM、宿主机/目标机、交叉编译等）
- `references/style-rules.md`：句式与表达规范（陈述句式、量化指标、如实陈述原则、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 获取目标计算机系统的数据手册/用户手册，形成「目标机画像」：处理器架构与主频、存储器容量、指令集特性、中断能力、寄存器、外设接口、错误指示与诊断特性；
   - 扫描项目的构建配置（Makefile、CMakeLists.txt、CI 配置、构建脚本），识别编辑、编译、汇编、连接工具及其版本号，交叉编译与加载校验方式；
   - 扫描接口相关源码（驱动、寄存器定义、中断服务程序），提取外设寄存器地址、设备号、接口指令的真实用法；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、研制阶段、相关方作为补充素材；
   - 写入规则：文档中的部件名、指令助记符、寄存器名、地址、工具版本必须与数据手册和构建配置事实一致，禁止编造不存在的内容；素材无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组（1.1 标识的五要素标识行由引擎按 config.json 自动替换，1.1 的 `content` 只写总述段）
   - 第 2 章（引用文档）为静态章节，以文字列举引用文档
   - 第 3 章（软件编程环境）使用 `placeholders`；3.2 操作信息的 a）～j）固定子条用 `subsections` 静态填写
   - 第 4 章（编程信息）使用 `placeholders`；4.1、4.2、4.3 的固定子条用 `subsections` 静态填写
   - 第 5 章（注释）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：陈述句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的目标机画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——量化指标是否齐全、技术参数与数据手册是否一致、无内容的条目是否如实陈述、章节号引用是否真实存在、指令与接口描述是否第 0 步的素材事实一致。
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

**带固定子条的章节**（3.2、4.1、4.2、4.3）：
```json
{
  "id": "3.2",
  "name": "操作信息",
  "type": "content_generation",
  "replacement_pattern": "本条应描述软件系统的操作特性、能力和限制，(若适用)应包括:",
  "content": "string（本条引言）",
  "subsections": {
    "3.2.1": {
      "name": "时钟周期",
      "replacement_pattern": "a)时钟周期",
      "content": "a)时钟周期：……"
    }
  }
}
```

> **固定子条的机制约束（重要，涉及 3.2/4.1/4.2/4.3）**
> 模板中这些章节自带固定的子条清单（如 3.2 的 a)时钟周期 ～ j)特殊特性），引擎按 `replacement_pattern` 逐条定位并替换为子条 `content`；子条编号字母按模板原样保留在 `content` 开头（模板中 f)、i）两处缺字，按字母顺序补全）。
> `replacement_pattern` 必须与模板中的原型条目文字**逐字一致**（含全角/半角标点），不得修改；确无内容的子条在 `content` 中如实写"本系统不涉及……"，不得编造参数。

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`；带子条的章节 placeholder 级 `content` 为该条引言，子条只修改各自的 `content`
2. 不修改 `id`、`type`、子条的 `name` 与 `replacement_pattern` 等模板结构字段
3. `subsections` 的 key 必须是有效章节编号（如 `"3.2.1"`），且与模板子条顺序一致

> **本模板无内容表格**：`[21] 计算机编程手册` 模板中没有需要填充的数据表格（封面表格与"文件更改记录表"由模板自带、不在填写范围），因此 `project.json` 不使用 `tables` 配置；`tables` 相关的 `locator_rows` 规则不适用。

# 运行

安装依赖（首次）：

```bash
pip install -r scripts/requirements.txt
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[21]计算机编程手册-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[21]计算机编程手册-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
