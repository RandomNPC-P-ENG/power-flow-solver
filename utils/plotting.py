"""Voltage profile visualization.
电压分布可视化
"""

import numpy as np
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def plot_voltage_profile(result, bus_names=None):
    """Plot voltage magnitude profile / 绘制电压幅值分布图"""
    if not HAS_MPL:
        print("matplotlib not installed")
        for i, (mag, ang) in enumerate(zip(result.voltage_mag, result.voltage_angle)):
            name = bus_names[i] if bus_names else f"Bus {i+1}"
            print(f"  {name}: V={mag:.4f} p.u., θ={ang:.2f}°")
        return

    n = len(result.voltage_mag)
    x = range(1, n + 1)
    labels = bus_names if bus_names else [f"Bus {i}" for i in x]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    ax1.bar(x, result.voltage_mag, color='steelblue')
    ax1.axhline(y=1.05, color='r', linestyle='--', label='Upper limit / 上限')
    ax1.axhline(y=0.95, color='r', linestyle='--', label='Lower limit / 下限')
    ax1.set_ylabel('Voltage (p.u.) / 电压')
    ax1.set_title('Voltage Magnitude Profile / 电压幅值分布')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.bar(x, result.voltage_angle, color='coral')
    ax2.set_xlabel('Bus Number / 母线编号')
    ax2.set_ylabel('Angle (°) / 相角')
    ax2.set_title('Voltage Angle Profile / 电压相角分布')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('voltage_profile.png', dpi=150)
    plt.show()
