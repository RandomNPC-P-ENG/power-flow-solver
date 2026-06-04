"""Run power flow on IEEE 14-bus system.
在IEEE 14节点系统上运行潮流计算
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from solver.newton_raphson import newton_raphson
from data.ieee14 import IEEE14_BUS, IEEE14_LINE
from utils.plotting import plot_voltage_profile

print("=" * 50)
print("IEEE 14-Bus Power Flow Analysis")
print("IEEE 14节点潮流计算分析")
print("=" * 50)

# Run Newton-Raphson / 运行牛顿-拉夫逊法
result = newton_raphson(IEEE14_BUS, IEEE14_LINE)

if result.converged:
    print(f"\n✓ Converged in {result.iterations} iterations")
    print(f"✓ 在 {result.iterations} 次迭代后收敛")
else:
    print("\n✗ Did not converge / 未收敛")

# Print results / 打印结果
print(f"\n{'Bus':<6} {'Type':<6} {'V (p.u.)':<10} {'θ (°)':<10}")
print("-" * 35)
for i, bus in enumerate(IEEE14_BUS):
    btype = {1: "PQ", 2: "PV", 3: "Slack"}[bus["type"]]
    print(f"{bus['name']:<16} {btype:<6} {result.voltage_mag[i]:<10.4f} {result.voltage_angle[i]:<10.2f}")

print(f"\nTotal losses / 总损耗: {result.losses:.4f} p.u.")

# Plot / 绘图
bus_names = [bus["name"] for bus in IEEE14_BUS]
plot_voltage_profile(result, bus_names)
