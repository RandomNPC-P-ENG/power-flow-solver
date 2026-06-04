"""Y-bus admittance matrix formation.
导纳矩阵形成
"""

import numpy as np


def form_ybus(bus_data, line_data):
    """Form the Y-bus admittance matrix / 形成导纳矩阵
    
    Args:
        bus_data: List of bus info dicts / 母线信息列表
        line_data: List of line info dicts / 线路信息列表
            Each line: {"from": int, "to": int, "r": float, "x": float, "b": float}
    
    Returns:
        Complex Y-bus matrix / 复数导纳矩阵
    """
    n = len(bus_data)
    ybus = np.zeros((n, n), dtype=complex)

    for line in line_data:
        f = line["from"] - 1  # 0-indexed
        t = line["to"] - 1
        r = line["r"]
        x = line["x"]
        b = line.get("b", 0)

        # Series admittance / 串联导纳
        y_series = 1.0 / complex(r, x)

        # Shunt admittance (charging) / 对地导纳（充电）
        y_shunt = complex(0, b / 2)

        # Off-diagonal / 非对角元素
        ybus[f, t] -= y_series
        ybus[t, f] -= y_series

        # Diagonal / 对角元素
        ybus[f, f] += y_series + y_shunt
        ybus[t, t] += y_series + y_shunt

    # Add bus shunt admittance / 添加母线并联导纳
    for i, bus in enumerate(bus_data):
        if "gshunt" in bus or "bshunt" in bus:
            ybus[i, i] += complex(bus.get("gshunt", 0), bus.get("bshunt", 0))

    return ybus


def print_ybus(ybus):
    """Print Y-bus matrix / 打印导纳矩阵"""
    n = ybus.shape[0]
    print(f"Y-bus matrix ({n}x{n}):")
    for i in range(n):
        row = "  ".join(f"{ybus[i,j]:8.4f}" for j in range(n))
        print(f"  [{row}]")
