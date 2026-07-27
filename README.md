# 三衍 Agent 协作审计协议

[中文](README.md) | [English](README_EN.md)

[![CI](https://github.com/sanyan-project/agent-protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/sanyan-project/agent-protocol/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![MIT License](https://img.shields.io/badge/License-MIT-E8D7B5.svg)](LICENSE)

![两条独立 Agent 路径经过审计门，汇入证据天平](docs/assets/repository-cover.jpg)

> **v1.0-alpha · runnable reference · not production-ready**

**把 Agent 协作中的角色分离、证据引用、人工授权和停止条件，变成会失败关闭的确定性硬门。**

这是一个面向“一个 Agent 执行、另一个角色审阅”的最小协作协议。它把几条最重要的规则变成可运行检查，而不是只写在提示词里：

- 执行者与审阅者必须不同；
- 任务记录必须完整经过观察、判断、决策、行动、反思、沉淀六阶段；
- 每条事实性声明必须引用工作区内真实、非空的 `file:line`；
- 高风险任务必须记录人工批准；
- 任务必须记录结果与停止条件；
- 任一硬门失败，审计结论就是 `FAIL`。

它不声称 Agent 团队会自动自我进化，也不证明审阅者天然独立或判断正确。当前版本只是一个确定性协议内核和公开的合成示例。

## 快速体验

需要 Python 3.10 或更高版本，无第三方运行时依赖：

```bash
python health_check.py
```

预期得到 JSON 报告，`verdict` 为 `PASS`，5 个硬门全部通过。

关键结果如下：

```json
{"failed": 0, "passed": 5, "protocol_version": "1.0-alpha", "verdict": "PASS"}
```

也可以显式审计一份记录：

```bash
python -m sanyan_protocol.cli audit \
  --record examples/audit_record.json \
  --root examples/workspace
```

## 安装与测试

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/validate_public_package.py
```

安装后也可使用：

```bash
sanyan-audit health
```

## 它检查什么

| 硬门 | 可确定性验证的内容 | 不能证明的内容 |
|---|---|---|
| 状态机 | 六阶段完整且顺序固定 | 每一步思考是否足够深入 |
| 角色分离 | 规范化后的 executor 与 reviewer 标识不同 | 两者是否真正使用独立模型/上下文 |
| 引用存在性 | 文件在授权根目录内，行号存在且非空 | 引用是否语义支持整条结论 |
| 人工权限 | 高风险记录声明已获人工批准 | 批准者身份是否真实 |
| 收尾 | outcome 与 stop_condition 已记录 | 业务目标是否真的完成 |

完整字段合同见 [PROTOCOL.md](PROTOCOL.md)。理念背景见 [WHITEPAPER.md](WHITEPAPER.md)，其中历史数字已明确标为未经当前仓库复验的快照。

## 当前证据

本仓库提供一个完全合成的审计记录和一组回归测试，覆盖通过路径，以及缺阶段、同一角色自审、高风险无人工批准、路径穿越、绝对路径、未知文件、越界行和空白行等失败路径。[GitHub CI](https://github.com/sanyan-project/agent-protocol/actions/workflows/ci.yml) 已在 Python 3.10、3.11 和 3.12 上通过同一组检查。

## 安全与范围

不要提交客户资料、真实聊天、凭证、私有仓库路径或内部审计日志。公开示例必须是合成数据。若审计输入含敏感材料，请在受控本地环境运行，不要把输入附到公开 issue。

贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)，安全报告见 [SECURITY.md](SECURITY.md)。项目采用 [MIT License](LICENSE)。
