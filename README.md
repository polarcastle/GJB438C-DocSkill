<div align="center">

# GJB 438C 文档填写工具集

**基于 Claude Code 的军用软件文档自动填写工具 — 告别手工填表，让 AI 替你写文档**

[![GitHub Stars](https://img.shields.io/badge/Stars-999+-yellow?style=social&logo=github)](https://github.com/polarcastle/GJB438C-DocSkill/stargazers)
[![License](https://img.shields.io/badge/License-Mulan_PSL_v2-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-7C3AED?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](https://github.com/polarcastle/GJB438C-DocSkill/pulls)

---

</div>

> 📌 本项目 fork 自 [potato-vita/GJB438C-DocSkill](https://github.com/potato-vita/GJB438C-DocSkill)，在其基础上进行了「素材驱动 + 写作知识库」改造，改造内容详见 [建设方案.md](建设方案.md)。

## 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [使用方式](#-使用方式)
- [模板覆盖](#-模板覆盖)
- [技术架构](#-技术架构)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## ✨ 功能特性

<table>
<tr>
<td width="50%">

### 📝 [08] 软件需求规格说明书

基于 GJB 438C 标准的 SRS 文档自动生成

- 交互式填写封面信息
- 自动生成章节内容（范围、需求、接口…）
- 合格性规定表格自动填充
- 需求追踪表双向关联
- 严格模式校验模板锚点

</td>
<td width="50%">

### 🏗️ [10] 软件概要设计说明书

基于 GJB 438C 标准的 SDD 文档自动生成

- CSCI 体系结构自动组织
- 部件设计与接口描述生成
- 执行计划与接口详细设计
- 需求可追踪性矩阵
- 严格模式校验模板锚点

</td>
</tr>
</table>

### 🔍 素材驱动 + 写作知识库

本次改造的核心差异：生成内容以**事实**为依据，而不是让模型自由发挥。

- **素材驱动生成**：以项目源代码（可选补充建设方案文档）为事实依据——先扫描源码形成「项目画像」（模块划分、接口签名、数据结构、依赖关系），文档中的模块名、接口名、功能描述与代码一致，代码中不存在的内容禁止写入
- **写作知识库**：每个模板配套章节级写作要点（`writing-guide.md`）、军用软件术语表（`terminology.md`）、句式与表达规范（`style-rules.md`），生成前必读、写后对照自查
- **待确认清单收尾**：生成结束前自动汇总全文「待与用户确认」事项（所在章节、缺失信息、建议默认值）；无源码依据的量化指标如实标注「待定」，不编造数值

💡 **核心理念**：用户只需用自然语言描述项目信息，Claude 自动完成模板匹配、内容生成和文档导出。

---

## 🚀 快速开始

### 前置要求

- [Claude Code CLI](https://claude.ai/code) 已安装并登录
- Python 3.10+（由 skill 自动调用）

### 安装

**方式一：直接安装 Plugin**（推荐 ✅）

```bash
claude plugin add polarcastle/GJB438C-DocSkill
```

或在 Claude Code 对话中执行：

```
/plugin add polarcastle/GJB438C-DocSkill
```

**方式二：通过 Marketplace 添加**

```bash
claude plugin marketplace add https://github.com/polarcastle/GJB438C-DocSkill
claude plugin install gjb438c-doc-filler
```

---

## 📖 使用方式

安装后，在 Claude Code 对话中用自然语言描述需求即可自动触发对应 Skill。全部 31 类模板均已支持，触发词为各类文档的名称或缩写，例如：

| 触发关键词 | 触发 Skill |
|:---|:---|
| `438C` `需求规格说明` `SRS` `软件需求` | `[08]` 软件需求规格说明书 |
| `概要设计` `SDD` `设计说明` `概要设计说明` | `[10]` 软件概要设计说明书 |
| `开发计划` `SDP` | `[02]` 软件开发计划 |
| `测试计划` `STP` / `测试报告` `STR` / `用户手册` `SUM` | `[15]` / `[19]` / `[20]` |
| 其余文档以此类推（见下方「模板覆盖与完成情况」表） | `[01]`～`[31]` |

### 使用流程

1. **提供素材**：给出项目源码目录（必选）和建设方案文档（可选，.docx/.md/.txt）——生成内容以这些素材为事实依据
2. **素材收集**：Claude 扫描源码形成「项目画像」（模块划分、接口签名、数据结构、依赖关系），作为全部章节内容的事实来源
3. **填写确认**：引导完成封面信息与各章节内容填写，量化指标无源码依据时如实标注「待与用户确认」
4. **生成输出**：运行脚本输出合规 `.docx`，并汇总「待确认清单」请用户逐项确认或接受建议默认值

### 示例对话

```
# 生成需求规格说明书（附源码目录）
> 帮我按照438C模板生成一份软件需求规格说明书，
> 源码在 /path/to/mybackend，项目名称是"XXX系统"，开发单位是"XX研究所"

# 生成概要设计说明书（源码 + 建设方案）
> 按照GJB 438C标准填写软件概要设计说明，
> 源码在 /path/to/project，建设方案见 /path/to/方案.docx
```

Claude 会依次引导你完成素材收集、封面信息、章节内容的填写，最终输出合规的 `.docx` 文件。

---

## 📋 模板覆盖与完成情况

GJB 438C 标准共 31 类文档，**全部建有独立 Skill 并通过端到端生成验证**（`pytest` 873 项用例全绿，每个 Skill 均用真实模板跑通「JSON 填写 → 引擎生成 .docx → 锚点消除校验」全流程）。

完成情况分为两级：

- ✅ **完整支持**：封面、标识行、全部正文章节、数据表格均可引擎自动生成
- ⚠️ **部分支持**：模板本身为骨架/含重度合并单元格，标注的章节或表格需生成后在 Word 中人工补写（各 Skill 的 `SKILL.md` 与 `references/writing-guide.md` 已写明补写要点）

| 序号 | 文档类型 | 完成情况 |
|:---:|:---|:---|
| 01 | 软件总体技术方案 | ⚠️ 骨架模板：封面与第 1 章可生成，第 3～11 章正文模板无锚点，需人工补写 |
| 02 | 软件开发计划 (SDP) | ✅ 完整支持 |
| 03 | 软件配置管理计划 | ✅ 完整支持 |
| 04 | 软件质量保证计划 | ✅ 完整支持 |
| 05 | 软件标准化大纲 | ✅ 完整支持 |
| 06 | 可靠性和可维护性大纲 | ✅ 完整支持 |
| 07 | 安全性大纲 | ✅ 完整支持 |
| 08 | 软件需求规格说明 (SRS) | ✅ 完整支持（含 3.1～3.4 动态章节、合格性/追踪表） |
| 09 | 接口需求规格说明 (IRS) | ✅ 完整支持 |
| 10 | 软件概要设计说明 (SDD) | ✅ 完整支持（含 CSCI 体系结构块、追踪表） |
| 11 | 数据库设计说明 (DBDD) | ✅ 完整支持 |
| 12 | 软件详细设计说明 | ✅ 完整支持（第 3 章为动态软件单元子节；封面"拟制/审核/批准"签字栏人工填写） |
| 13 | 软件接口设计说明 (IDD) | ✅ 完整支持 |
| 14 | 软件可靠性和可维护性设计 | ✅ 完整支持 |
| 15 | 软件测试计划 (STP) | ✅ 完整支持 |
| 16 | 软件测试说明 (STD) | ✅ 完整支持 |
| 17 | 软件测试记录 | ⚠️ 正文可生成；表 8/9/10（齐套审查/功能测试记录）为重度合并单元格，保留空白网格手工填写 |
| 18 | 软件测评大纲 | ✅ 完整支持 |
| 19 | 软件测试报告 (STR) | ✅ 完整支持（统计表合并单元格由本 Skill 引擎副本专项适配） |
| 20 | 软件用户手册 (SUM) | ✅ 完整支持 |
| 21 | 计算机编程手册 | ✅ 完整支持 |
| 22 | 测试问题报告 | ✅ 完整支持 |
| 23 | 软件变更报告 | ⚠️ 1.2 系统概述 / 1.3 文档概述模板无指导文字锚点，该两节需人工补充；其余完整 |
| 24 | 软件版本说明 | ✅ 完整支持 |
| 25 | 软件产品规格说明 | ✅ 完整支持 |
| 26 | 软件质量保证报告 | ✅ 完整支持 |
| 27 | 软件标准化工作报告 | ✅ 完整支持 |
| 28 | 研制总结报告 | ✅ 完整支持 |
| 29 | 技术总结报告 | ⚠️ 纯标题骨架：封面/签署/更改记录可生成，各章正文需人工补写 |
| 30 | 软件安全性设计 | ✅ 完整支持 |
| 31 | 软件配置管理报告 | ✅ 完整支持 |

**所有模板的共通人工项**（引擎按设计不处理，生成后在 Word 中完成）：封面签署栏（拟制/审核/标准化/批准）、`共XX页` 页数域（Word 打开后自动更新）、文件更改记录表（随更改登记）、首次打开时按提示刷新目录。

> 🎯 每个模板对应 `skills/word-fillter-438c-NN/` 下的独立 Skill，用自然语言提到文档名称（如"测试计划""用户手册"）即可触发。

---

## 🛠️ 技术架构

```
GJB438C-DocSkill/
├── .claude-plugin/
│   ├── plugin.json              # 插件清单
│   └── marketplace.json         # Marketplace 注册表
├── skills/
│   ├── word-fillter-438c-01/    # [01] 软件总体技术方案
│   ├── ...                      # [02]～[31] 每个模板一个独立 Skill，结构相同
│   ├── word-fillter-438c-08/    # [08] 软件需求规格说明书
│   │   ├── SKILL.md             # Skill 定义
│   │   ├── documents/           # 模板 .docx
│   │   ├── templates/           # config.json + project.json
│   │   ├── references/          # 写作知识库
│   │   │   ├── writing-guide.md #   章节写作要点
│   │   │   ├── terminology.md   #   军用软件术语表
│   │   │   └── style-rules.md   #   句式与表达规范
│   │   └── scripts/             # Python 填写引擎
│   │       ├── main.py          # CLI 入口
│   │       ├── process.py       # 免参数入口
│   │       └── strict_word_filler/  # 核心引擎
│   └── word-fillter-438c-31/    # [31] 软件配置管理报告
├── demo/                        # 示例输出文档
└── GJB438C全套模版/             # GJB 438C 标准全部模板
```

**技术栈：**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![python-docx](https://img.shields.io/badge/python--docx-1.1.0+-orange)
![Claude](https://img.shields.io/badge/Claude-Code-7C3AED?logo=anthropic&logoColor=white)

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](https://github.com/polarcastle/GJB438C-DocSkill/pulls)
[![Issues](https://img.shields.io/github/issues/polarcastle/GJB438C-DocSkill)](https://github.com/polarcastle/GJB438C-DocSkill/issues)

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/new-template`)
3. 提交变更 (`git commit -m 'feat: 添加 [XX] 模板支持'`)
4. 推送到分支 (`git push origin feature/new-template`)
5. 创建 Pull Request

### 致谢

感谢所有为本项目做出贡献的开发者：

[![Contributors](https://img.shields.io/github/contributors/polarcastle/GJB438C-DocSkill?color=blue)](https://github.com/polarcastle/GJB438C-DocSkill/graphs/contributors)

---

## 📄 许可证

本项目基于 [木兰宽松许可证 第2版 (Mulan PSL v2)](LICENSE) 开源。

---

<div align="center">

[![Made with Claude Code](https://img.shields.io/badge/Made_with-Claude_Code-7C3AED?logo=anthropic&logoColor=white)](https://claude.ai/code)

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

</div>
