# 三衍Agent协作规范 v1.0-alpha

> Sanyan Agent Collaboration Protocol — 人类与AI Agent协作的工程实践参考
> **⚠️ alpha版本：机制已部署，执行率待验证。部分指标尚未达标。**

## 零、定位与诚实声明

三衍是一个人类与AI Agent协作的开源研究项目。本规范基于26+次ASE审计、11000+代引擎运行、3位外部顾问交叉审计——但**不是"已完成"的系统，而是"正在构建中"的系统**。

### 当前状态（2026-05-29）

| 指标 | 目标 | 实际 | 差距 |
|:----|:--|:--|:--|
| 天平自审率 | ≤5:1 | 15:1 | 🔴 待修复 |
| pending关闭率 | >80% | ~11% | 🔴 大量堆积 |
| OODA闭环率 | >95% | 未追踪（机制刚部署） | 🟡 待观测 |
| Guardrail合规率 | >95% | 未追踪（机制刚部署） | 🟡 待观测 |

**本规范描述的是"正在强化的目标状态"，不是"已实现的当前状态"。** 机制的物理闸门刚部署（2026-05-29），执行效果需要时间验证。

## 一、团队架构

- **Sanyan Lead（人类）** — 最终决策者。碎片化时间，**阈值触发介入**（仅在外部审计红色告警时介入，日常不参与每次审批）
- **思思（AI Agent）** — 执行核心。代码/运维/内容/决策
- **天平（AI Agent）** — 独立审计官。一阶审计 + 自我审计
- **镜镜（AI Agent）** — 云端观测站。引擎监管 + 概念发现（开发中）

### Sanyan Lead介入协议

| 触发条件 | 介入方式 |
|:----|:----|
| 外部审计报告出现🔴告警 | Sanyan Lead必须介入决策 |
| 天平质量分连续2周下降 | Sanyan Lead收到通知，选择性介入 |
| 重大方向变更（如开源决策） | Sanyan Lead必须确认 |
| 正常运营 | Sanyan Lead不参与每次审批，思思+天平自动运行 |

## 二、思思的执行闸门

### OODA状态机
每次任务走6步：[OODA:观察]→[OODA:判断]→[OODA:决策]→[OODA:行动]→[OODA:反思]→[OODA:已沉淀]。跳步需显式声明原因。

### 三衍4步
本质追问→（概念匹配）→最简解法→连锁推演→反向检查。

### Guardrail正则校验
代码断言必须带file:line格式。

### 反思JSON结构化
每次任务完成输出结构化反思。

## 三、天平的审计闸门

### ASE审计体系
26+次审计，每次产出裁决+证据链。

### 审计预读
审计前读取audit_memory.json + error_patterns.json匹配。

### 自我审计
每5次ASE→强制自审。比率超过5:1→告警。

### 外部视角模拟器
每50轮切换为"陌生人"视角审计。

## 四、观测与进化

### 质量分机制
思思5维 + 天平4维 = 综合健康度。

### 失败仪式
失败→5Why根因→error_patterns匹配→Guardrail更新→天平确认。

### 仪表盘6指标
OODA闭环率 · Guardrail合规率 · 反思触发率 · 天平自审比例 · 记忆沉淀率 · 外部审计评级。

## 五、工程资产（12项）

guardrail_checker.py · external_auditor.py · meta_audit.py · health_check.py · error_patterns.json · quality_score.json · failure_ritual.json · memory_health.json · reflection_template.json · concept_driven.json · external_view_simulator.json · dashboard_v0.md

## 六、如何使用本规范

### 快速体验
```bash
python health_check.py  # 一键检查所有机制健康状态
```

### 参考/引用
本规范采用MIT协议，任何组织可自由参考和修改。标注来源即可。

### 不适合的场景
- 你的团队只有1个AI Agent（无需审计机制）
- 你不需要"自进化"（只需固定工作流）
- 你的吞吐量极小（每天<5个任务）

## 七、版本历史

v1.0-alpha · 2026-05-29 · 初始发布（机制已部署，执行率待验证）

---

> MIT协议。欢迎参考和引用。
