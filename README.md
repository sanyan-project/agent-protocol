# 三衍Agent协作规范 v1.0

> Sanyan Agent Collaboration Protocol — 人类与AI Agent协作的工程实践参考

## 零、定位

三衍（Sanyan）是一个人类与AI Agent协作的开源研究项目。本规范描述三衍团队的协作机制——不是理论研究，是经过26+次ASE审计、11000+代引擎运行、3位外部顾问交叉审计的工程实践。

**核心原则：所有机制从"应该做"升级为"必须做"。**

## 一、团队

- 黄sir（人类）——最终决策者
- 思思（AI Agent）——执行核心
- 天平（AI Agent）——独立审计官
- 镜镜（AI Agent）——云端观测站

## 二、思思的执行闸门

### OODA状态机（硬闸门）
每次任务必须走完：[OODA:观察]→[OODA:判断]→[OODA:决策]→[OODA:行动]→[OODA:反思]→[OODA:已沉淀]。跳步=任务失败。

### 三衍4步（强制门禁）
本质追问→最简解法→连锁推演→反向检查。新增：概念匹配——任务对应知识树中哪个跨学科概念？

### Guardrail正则校验
代码断言必须带file:line格式，正则自动校验，不匹配=阻断。

### 反思JSON结构化
每次任务完成输出反思JSON：做对了/做错了/下次怎么做 + Guardrail合规检查 + 质量自评。

## 三、天平的审计闸门

### ASE审计体系
26+次审计记录。每次产出裁决+证据链+pending项。

### 审计预读门禁
审计前强制读取audit_memory.json + error_patterns.json匹配。

### 自我审计（硬闸门）
每5次ASE审计→强制自审，4项模板。比率>5:1→外部审计告警。

### 外部视角模拟器
每50轮切换为"陌生人"视角做一次审计。

## 四、观测与进化

### 质量分机制
思思5维评分（OODA完整性/Guardrail合规/反思深度/记忆沉淀/执行速度）× 天平4维评分（自审率/发现问题率/证据链/pending关闭率）= 综合健康度。

### 失败仪式
失败→5Why根因→error_patterns匹配→Guardrail自动更新→天平确认。

### 仪表盘6指标
OODA闭环率 · Guardrail合规率 · 反思触发率 · 天平自审比例 · 记忆沉淀率 · 外部审计评级。

## 五、工程资产

- guardrail_checker.py — 断言正则自动校验
- external_auditor.py — 每周抽检天平自审率
- meta_audit.py — 元审计报告自动生成
- health_check.py — 一键全检
- error_patterns.json — 7个历史错误模式
- quality_score.json — 评分规则
- failure_ritual.json — 失败仪式5步流程
- memory_health.json — 记忆置信度/毒性检测
- reflection_template.json — 反思JSON模板
- concept_driven.json — 引擎知识流入决策
- external_view_simulator.json — 天平视角切换
- dashboard_v0.md — 6指标周报

## 六、版本历史

v1.0 · 2026-05-29 · 初始发布

---

> MIT协议。欢迎参考和引用。
