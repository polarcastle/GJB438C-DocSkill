---
name: word-fillter-438C-12
description: "当用户提到「按照438C模板填写word文档」「详细设计」「软件详细设计说明」「438C」「SDD」「详细设计模板填写」时触发。交互式填写 GJB 438C [12] 软件详细设计说明模板，生成符合规范的 .docx 文档。"
---

# 何时使用

当用户需要基于 `[12]软件详细设计说明-438C.docx` 模板生成或修改 GJB 438C 软件详细设计说明时使用本 Skill。

# 约束

- 只处理 `.docx` 模板，不处理 `.doc`
- 严格模式运行，不做兜底和回退；模板锚点、章节原型不匹配时必须报错
- 目录通过 Word 域刷新，不直接改目录文本
- 只修改 `content` 字段，不得修改模板结构

# 目录结构

- `documents/[12]软件详细设计说明-438C.docx`：模板文档
- `templates/config.json`：封面与标识配置
- `templates/project.json`：章节内容与软件单元子条
- `references/writing-guide.md`：章节级写作要点（必写内容、写作深度、常见缺陷）
- `references/terminology.md`：军用软件术语表（CSCI、CSU、SDD、IDD、DBDD 等）
- `references/style-rules.md`：句式与表达规范（设计描述句式、量化指标、如实陈述、禁用表达）
- `scripts/main.py`：命令行入口（推荐）
- `scripts/process.py`：免参数入口（不推荐：需将 config/project 拷入 scripts/，会污染技能仓库）

# 工作流

0. **素材收集**：生成任何内容前，先收集并核实输入素材，作为全部章节内容的事实依据：
   - 扫描用户指定的项目源码目录，形成「项目画像」：识别开发语言、模块划分、入口文件、对外接口/API、关键类与函数、依赖关系；
   - 若用户提供了建设方案文档（.docx 用 python-docx 读取，.md/.txt 直接读取），提取其中的项目背景、建设目标、建设内容作为补充素材；
   - 写入规则：文档中的单元名、接口名、算法与数据元素描述必须与源码事实一致，禁止编造源码中不存在的内容；源码无法支撑的章节，提示用户补充信息或如实从简。
1. 修改 `templates/config.json` 中各字段的 `content`，填写项目名称、版本、单位、日期等封面信息。
2. 修改 `templates/project.json` 中各章节内容：
   - 第 1 章（范围）使用 `placeholders` 数组
   - 第 2 章（引用文档）为文字列举（本模板无引用文档表格）
   - 第 3 章（详细设计）按软件单元填写：章节级 `content` 为 3.1 单元标题，placeholder 级 `content` 为 3.1 单元正文，`subsections` 填写 3.2 及以后的单元
   - 第 4 章（需求可追踪性）以 a）b）两条文字给出双向追踪（本模板无追踪表）
   - 第 5 章（注释）为静态章节
3. 运行生成脚本（见"运行"章节）。
4. 检查输出 `.docx` 文件，首次在 Word 中打开时刷新目录。

# 内容生成规范

生成每章 `content` 时，必须按以下流程执行：

1. **先读知识库**：生成前阅读 `references/` 下三个文件——
   - `writing-guide.md`：本章必写内容、写作深度与常见缺陷；
   - `terminology.md`：术语的中文全称、英文缩写与使用场景，全文术语与其保持一致；
   - `style-rules.md`：设计描述句式、量化指标、如实陈述原则与禁用表达。
2. **按提示生成**：各字段的 `generation_prompt` 已给出角色定位、要点清单、句式要求和篇幅建议，以其为准并结合工作流第 0 步素材收集得到的项目画像生成内容。
3. **写后自查**：内容写入 JSON 前，对照 `writing-guide.md` 的要点清单逐条自查——每个单元是否覆盖 a）～f）方面、算法与数据结构是否有源码依据、量化指标是否齐全、是否误用"应"字需求句式、追踪表的单元标识/需求标识/章节号是否真实存在、单元与接口描述是否第 0 步的源码事实一致。
4. **再写入**：自查通过后写入 `content`，保持 JSON 结构不变。
5. **收尾汇总（全部 JSON 填写完成后、运行脚本前）**：汇总本文档中所有标注"待与用户确认/待定"的事项，在对话中集中呈现给用户——每项给出所在章节、缺失的信息与建议默认值，请用户逐项确认或接受默认值后再生成；单人/离线无法确认时，保留"待定"标注并原样列入清单，不得自行编造数值补齐。

# JSON 规则

## config.json

config.json 包含 `project`、`document`、`content` 三部分，所有字段只修改 `content` 值。

> **单位名称无默认值**：`project.company` 与 `project.department` 的 `content` 出厂为空，必须由用户明确提供后填写；禁止沿用任何示例单位名或编造。单位名称缺失时引擎会以"字段为空"报错，这是预期行为。

> **封面遗留字段**：本模板封面另有「[课题编号：  ]」和扉页「拟 制 人／审 核 人／标 准 化／批 准 人」行，config 无对应字段，引擎不处理，生成后需人工填写。`document.phase` 为必填校验字段，但本模板封面无"阶段"行，其值不参与正文替换。

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

**第 3 章 详细设计（本模板特有结构，重要）**：
```json
{
  "3": {
    "title": "详细设计",
    "replacement_pattern": "3.X (软件单元的项目唯一的标识符，或者一组软件单元的标志符)",
    "content": "3.1 单元一名称（SU-01）",
    "placeholders": [
      {
        "id": "3",
        "name": "详细设计",
        "content": "3.1 单元的正文（按 a）～f）方面分行书写）",
        "subsections": {
          "3.2": { "name": "单元二名称（SU-02）", "content": "string" },
          "3.3": { "name": "单元三名称（SU-03）", "content": "string" }
        }
      }
    ]
  }
}
```

> **机制约束（涉及第 3 章）**
> - 章节级 `content` 是 **3.1 的标题**（引擎用它替换原型标题段，Heading 2 样式自动保留），**只写标题，勿写正文**；
> - placeholder 级 `content` 是 **3.1 单元的正文**；
> - `subsections` 填写 **3.2 及以后**的单元，**不允许为空**——即全文至少 3.1、3.2 两个单元条。软件确实很小时，把单元如实划分为两个以上逻辑单元，或把 3.1 写为唯一的复合单元、3.2 写为支撑单元；**禁止为填满机制而编造源码中不存在的功能**。详见 `references/writing-guide.md`「第 3 章 详细设计」。
> - 子条中的 `replacement_pattern` 字段在动态模式下被引擎静默忽略，无需填写；子条 `name` 应与源码模块名一致、以中文开头，并带项目唯一的单元标识符（如"调度决策单元（SU-02）"），避免标题出现"3.2REST…"这类数字与英文连排无空格的观感问题。

### 处理规则

1. 静态章节（无 `subsections` 的 placeholder）只修改其 `content`
2. 不修改 `id`、`type`、placeholder 级的 `name` 与 `replacement_pattern`、第 3 章章节级的 `replacement_pattern` 等模板结构字段
3. 第 3 章：`content`（章节级）= 3.1 标题；placeholder `content` = 3.1 正文；`subsections` 中每个子条的 `name` 会作为章节标题写入文档、`content` 为该单元正文
4. `subsections` 的 key 必须是有效章节编号，从 `"3.2"` 开始递增
5. 本模板**无数据表格**（无 `tables` 配置）：第 2 章引用文档、第 4 章需求可追踪性均以文字段落形式写入对应 `content`

# 运行

安装依赖（首次）：

```bash
pip install python-docx>=1.1.0
```

生成文档（推荐，使用命令行入口）：

```bash
python scripts/main.py \
  --template "documents/[12]软件详细设计说明-438C.docx" \
  --config "templates/config.json" \
  --project "templates/project.json" \
  --output "output/[12]软件详细设计说明-438C-filled.docx"
```

或使用免参数入口（**不推荐**：需先将 config.json 和 project.json 复制到 scripts/ 目录，会污染技能仓库；常规情况请用上面的 main.py）：

```bash
cd scripts
python process.py
```

输出文档路径会打印在控制台。首次在 Word 中打开时，按提示刷新目录。
