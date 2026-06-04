"""Newton-Raphson power flow solver.
牛顿-拉夫逊法潮流计算
"""

import numpy as np
from .ybus import form_ybus


class PowerFlowResult:
    """Power flow results / 潮流计算结果"""
    def __init__(self):
        self.voltage_mag = None      # Voltage magnitude / 电压幅值
        self.voltage_angle = None    # Voltage angle (rad) / 电压相角
        self.p_injected = None       # Active power / 有功功率
        self.q_injected = None       # Reactive power / 无功功率
        self.converged = False       # Convergence flag / 收敛标志
        self.iterations = 0          # Iteration count / 迭代次数
        self.losses = None           # Line losses / 线路损耗


def newton_raphson(bus_data, line_data, tol=1e-6, max_iter=50):
    """Solve power flow using Newton-Raphson method.
    使用牛顿-拉夫逊法求解潮流。
    
    Bus types / 母线类型:
    - 1: PQ bus (load bus) / PQ节点（负荷节点）
    - 2: PV bus (generator bus) / PV节点（发电机节点）
    - 3: Slack bus (reference) / 平衡节点（参考节点）
    
    Args:
        bus_data: Bus information / 母线信息
        line_data: Line information / 线路信息
        tol: Convergence tolerance / 收敛容差
        max_iter: Maximum iterations / 最大迭代次数
    
    Returns:
        PowerFlowResult / 潮流计算结果
    """
    n = len(bus_data)
    ybus = form_ybus(bus_data, line_data)
    
    # Extract bus types / 提取母线类型
    bus_type = [bus.get("type", 1) for bus in bus_data]
    
    # Identify bus indices / 识别母线索引
    pq_idx = [i for i in range(n) if bus_type[i] == 1]
    pv_idx = [i for i in range(n) if bus_type[i] == 2]
    slack_idx = next(i for i in range(n) if bus_type[i] == 3)
    
    # Scheduled power (P and Q) / 给定功率
    p_spec = np.array([bus.get("p", 0) for bus in bus_data])
    q_spec = np.array([bus.get("q", 0) for bus in bus_data])
    
    # Initialize voltages / 初始化电压
    v_mag = np.array([bus.get("v", 1.0) for bus in bus_data])
    v_ang = np.zeros(n)  # Flat start / 平启动
    
    result = PowerFlowResult()
    
    for iteration in range(max_iter):
        # Calculate power injections / 计算注入功率
        p_calc = np.zeros(n)
        q_calc = np.zeros(n)
        
        for i in range(n):
            for j in range(n):
                p_calc[i] += v_mag[i] * v_mag[j] * abs(ybus[i,j]) * np.cos(v_ang[i] - v_ang[j] - np.angle(ybus[i,j]))
                q_calc[i] += v_mag[i] * v_mag[j] * abs(ybus[i,j]) * np.sin(v_ang[i] - v_ang[j] - np.angle(ybus[i,j]))
        
        # Power mismatches / 功率不平衡
        dp = p_spec - p_calc
        dq = q_spec - q_calc
        
        # Build mismatch vector / 构建不平衡向量
        # For PQ buses: ΔP and ΔQ
        # For PV buses: ΔP only (Q is unknown, V is specified)
        mismatches = []
        for i in pq_idx:
            mismatches.append(dp[i])
        for i in pq_idx:
            mismatches.append(dq[i])
        for i in pv_idx:
            mismatches.append(dp[i])
        
        mismatches = np.array(mismatches)
        
        # Check convergence / 检查收敛
        if np.max(np.abs(mismatches)) < tol:
            result.converged = True
            result.iterations = iteration
            break
        
        # Build Jacobian matrix / 构建雅可比矩阵
        # (Simplified — full implementation would compute partial derivatives)
        n_pq = len(pq_idx)
        n_pv = len(pv_idx)
        n_eq = 2 * n_pq + n_pv
        
        J = np.zeros((n_eq, n_eq))
        # J11: dP/dθ / ∂P/∂θ
        for i_idx, i in enumerate(pq_idx + pv_idx):
            for j_idx, j in enumerate(pq_idx + pv_idx):
                if i == j:
                    J[i_idx, j_idx] = -q_calc[i] - v_mag[i]**2 * ybus[i,i].imag
                else:
                    J[i_idx, j_idx] = v_mag[i] * v_mag[j] * abs(ybus[i,j]) * np.sin(v_ang[i] - v_ang[j] - np.angle(ybus[i,j]))
        
        # J22: dQ/dV * V / ∂Q/∂V * V (for PQ buses)
        for i_idx, i in enumerate(pq_idx):
            for j_idx, j in enumerate(pq_idx):
                if i == j:
                    J[n_pq + n_pv + i_idx, n_pq + n_pv + j_idx] = q_calc[i] - v_mag[i]**2 * ybus[i,i].imag
                else:
                    J[n_pq + n_pv + i_idx, n_pq + n_pv + j_idx] = -v_mag[i] * v_mag[j] * abs(ybus[i,j]) * np.cos(v_ang[i] - v_ang[j] - np.angle(ybus[i,j]))
        
        # Solve corrections / 求解修正量
        try:
            dx = np.linalg.solve(J, mismatches)
        except np.linalg.LinAlgError:
            print("Jacobian is singular — solution diverged / 雅可比矩阵奇异 — 解发散")
            break
        
        # Update voltages / 更新电压
        # Update angles for all non-slack buses
        idx = 0
        for i in pq_idx + pv_idx:
            v_ang[i] += dx[idx]
            idx += 1
        # Update magnitudes for PQ buses
        for i in pq_idx:
            v_mag[i] += v_mag[i] * dx[idx]
            idx += 1
    
    result.voltage_mag = v_mag
    result.voltage_angle = np.degrees(v_ang)
    result.p_injected = p_calc
    result.q_injected = q_calc
    
    # Calculate line losses / 计算线路损耗
    total_loss = 0
    for line in line_data:
        f = line["from"] - 1
        t = line["to"] - 1
        y = 1.0 / complex(line["r"], line["x"])
        i_f = ybus[f,f] * v_mag[f] * np.exp(1j*v_ang[f]) + ybus[f,t] * v_mag[t] * np.exp(1j*v_ang[t])
        s_f = v_mag[f] * np.exp(1j*v_ang[f]) * np.conj(i_f)
        i_t = ybus[t,f] * v_mag[f] * np.exp(1j*v_ang[f]) + ybus[t,t] * v_mag[t] * np.exp(1j*v_ang[t])
        s_t = v_mag[t] * np.exp(1j*v_ang[t]) * np.conj(i_t)
        loss = s_f + s_t
        total_loss += loss.real
    result.losses = total_loss
    
    return result
