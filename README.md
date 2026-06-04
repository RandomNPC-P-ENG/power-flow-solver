# Power Flow Solver ⚡

Newton-Raphson power flow solver for electrical power system analysis.

用于电力系统分析的牛顿-拉夫逊法潮流计算求解器。

---

## Features / 功能特性

- **Newton-Raphson method** — Full AC power flow with Jacobian matrix
  牛顿-拉夫逊法 — 含雅可比矩阵的完整交流潮流
- **Bus types** — PQ (load), PV (generator), Slack (reference)
  母线类型 — PQ（负荷）、PV（发电机）、平衡（参考）
- **Y-bus formation** — Automatic admittance matrix from line data
  导纳矩阵 — 从线路数据自动形成
- **Voltage profile** — Magnitude and angle at every bus
  电压分布 — 每条母线的幅值和相角
- **Power loss analysis** — Total system losses
  功率损耗分析 — 系统总损耗
- **IEEE test systems** — 14-bus, 30-bus, 57-bus, 118-bus
  IEEE 测试系统 — 14节点、30节点、57节点、118节点
- **Visualization** — Voltage profile charts
  可视化 — 电压分布图表

---

## Algorithm / 算法

```
Input: Bus data, Line data / 输入：母线数据、线路数据
        │
        ▼
Form Y-bus matrix / 形成导纳矩阵
        │
        ▼
Initialize: V=1.0∠0° (flat start) / 初始化：平启动
        │
        ▼
┌───▶ Calculate ΔP, ΔQ / 计算功率不平衡
│     │
│     ▼
│     Check |ΔP,ΔQ| < tol? / 检查收敛？
│     │YES                    │NO
│     ▼                       ▼
│     Output results          Build Jacobian J / 构建雅可比矩阵
│     (V, θ, P, Q, Losses)   Solve [J][Δx] = [ΔS]
│                             Update V, θ / 更新电压、相角
│                               │
└───────────────────────────────┘
```

---

## Project Structure / 项目结构

```
power-flow-solver/
├── solver/
│   ├── __init__.py
│   ├── ybus.py              # Y-bus matrix / 导纳矩阵
│   └── newton_raphson.py    # NR solver / 牛顿-拉夫逊求解器
├── data/
│   └── ieee14.py            # IEEE 14-bus data / 14节点数据
├── utils/
│   └── plotting.py          # Visualization / 可视化
├── examples/
│   └── run_ieee14.py        # Example / 示例
└── requirements.txt
```

---

## Quick Start / 快速开始

```bash
# Install dependencies / 安装依赖
pip install -r requirements.txt

# Run IEEE 14-bus example / 运行IEEE 14节点示例
python examples/run_ieee14.py
```

### Usage / 使用方法

```python
from solver.newton_raphson import newton_raphson
from data.ieee14 import IEEE14_BUS, IEEE14_LINE

result = newton_raphson(IEEE14_BUS, IEEE14_LINE)

if result.converged:
    print(f"Converged in {result.iterations} iterations")
    for i, v in enumerate(result.voltage_mag):
        print(f"  Bus {i+1}: V={v:.4f} p.u., θ={result.voltage_angle[i]:.2f}°")
    print(f"Total losses: {result.losses:.4f} p.u.")
```

---

## License / 许可证
MIT License

## Author / 作者
Isaac — Diploma in Electronic Engineering, TAR UMT

Built with ❤️ for learning power systems analysis
用 ❤️ 构建，用于学习电力系统分析
