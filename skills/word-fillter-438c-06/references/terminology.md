# 军用软件文档常用术语表（[06] 软件可靠性和可维护性大纲适用）

> 术语依据 GJB 438C-2021、GJB 5235 及 [06] 模板正文用法整理。全文术语必须与本表保持一致；首次出现时用"中文全称（英文缩写）"格式。只收录正文实际出现的术语，不得为凑数照搬通用词表。

## 配置管理与标识

| 术语 | 英文/缩写 | 含义与使用场景 |
|------|-----------|----------------|
| 计算机软件配置项 | CSCI（Computer Software Configuration Item） | 软件配置项，可靠性大纲中可靠性、可维护性目标分配与度量的对象。 |
| 基线 | Baseline | 经正式评审确认的文档/产品版本，后续更改受配置管理控制；大纲评审后纳入基线管理。 |
| 文档标识号 | — | 格式示例 `TN/x-DO-DS-V{N.xx}`，见 1.1 节标识行。 |
| 配置管理 | SCM（Software Configuration Management） | 大纲、度量数据、评审记录的更改控制与追踪。 |

## 文档类型

| 术语 | 英文/缩写 | 含义与使用场景 |
|------|-----------|----------------|
| 软件可靠性和可维护性大纲 | RAM 大纲（Reliability and Maintainability Program Plan） | [06] 本文档，规定软件生存周期各阶段可靠性、可维护性工作的要素、任务与职责。 |
| 软件开发计划 | SDP（Software Development Plan） | 本大纲纳入其中并与之协调的计划文档。 |
| 软件需求规格说明 | SRS（Software Requirements Specification） | 可靠性、可维护性需求（定量指标）的出处文档。 |
| 软件概要设计说明 | SDD（Software Design Description） | 可靠性、可维护性概要设计的载体文档。 |
| 软件研制任务书 | — | 可靠性、可维护性要求与经费的来源文件。 |

## 可靠性与可维护性专业术语

| 术语 | 英文/缩写 | 含义与使用场景 |
|------|-----------|----------------|
| 可靠度 | R(t)（Reliability） | 规定时间 t 内完成规定功能的概率；目标分配的顶层指标，写作"可靠度R（T）"。 |
| 平均故障间隔时间 | MTBF（Mean Time Between Failures） | 可修复产品相邻故障间的平均时间；定量指标必写单位 h。 |
| 平均修复时间 | MTTR（Mean Time To Repair） | 可维护性核心指标，含故障定位与恢复时间；定量指标必写单位 min 或 h。 |
| 失效发生率 | ROCOF/DROCOF（Rate/Density of Occurrence Of Failures） | 单位时间失效次数；模板"在需求分析阶段"条提到的定量目标示例。 |
| 故障模式、影响及危害度分析 | FMECA（Failure Mode, Effects and Criticality Analysis） | 设计阶段可靠性分析方法，识别故障模式、影响与危害度。 |
| 容错 | Fault Tolerance | 软件检出故障后维持规定功能的能力；详细设计评审关注点。 |
| 故障定位与隔离 | Fault Localization and Isolation | 定位故障到可更换单元并隔离其影响；影响 MTTR 的设计技术。 |
| 降额 / 降级 | Derating / Degraded Mode | 降低应力提高可靠性；功能降低使用方式下的最低功能保证。 |
| 故障树分析 | FTA（Fault Tree Analysis） | 系统级可靠性分析手段，按需采用。 |
| 可靠性和可维护性增长 | R&M Growth | 通过试验与维护使指标随时间提高的过程；使用维护阶段的度量主题。 |
| 定性估计 / 定量预测 / 测量 | Qualitative Estimation / Quantitative Prediction / Measurement | 3.2 条度量方法的三个类别，写作时区分早期估计与后期实测。 |

## 通用软件术语（按源码实际出现选用）

> 纯软件、信息化项目正文中高频出现的通用术语。首次出现写"中文全称（英文缩写）"，此后用缩写；源码中未出现的不得收录。

| 术语 | 英文/缩写 | 规范写法与使用场景 |
|------|-----------|----------------|
| 应用程序编程接口 | API（Application Programming Interface） | 对外接口的统称。 |
| 超文本传输协议 | HTTP（Hypertext Transfer Protocol） | 接口通信协议；注明方法（GET/POST）、状态码。 |
| JavaScript 对象表示法 | JSON（JavaScript Object Notation） | 数据交换格式；接口数据元素、消息体的默认格式。 |
| 远程过程调用 | RPC（Remote Procedure Call） | 远程调用协议的上位概念。 |
| 结构化查询语言 | SQL（Structured Query Language） | 数据库访问语言；涉及数据记录时使用。 |

## 术语裁剪指引

- 只收录正文实际出现的术语；「通用软件术语」一表按源码实际出现选用，不得为凑数整表照搬。
- 本大纲为计划类文档，不编制"合格性方法"（演示/测试/分析/检查/特殊方法）类术语；该类词汇属于 [08] SRS 第 4 章专用。
- 通用术语与 GJB 术语定义冲突时，以本表 GJB 定义为准，正文避免混用。
