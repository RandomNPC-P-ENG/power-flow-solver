# Power Flow Solver ⚡

Newton-Raphson power flow solver for electrical power system analysis.

## Features
- Newton-Raphson method for non-linear power flow equations
- Fast Decoupled Load Flow (FDBF) option
- PQ, PV, and Slack bus types
- Y-bus admittance matrix formation
- Voltage profile and power loss analysis
- IEEE test systems (14, 30, 57, 118 bus)
- CSV/JSON export of results
- Visualization of voltage profiles

## Algorithm
```
Input: Bus data, Line data
        │
        ▼
Form Y-bus matrix
        │
        ▼
Initialize: V=1.0∠0° (flat start)
        │
        ▼
┌───▶ Calculate ΔP, ΔQ (power mismatch)
│     │
│     ▼
│   Solve [J][Δx] = [ΔS]  (Jacobian)
│     │
│     ▼
│   Update V, δ
│     │
│     ▼
│   Converged? ──No──┘
│     │
│    Yes
│     ▼
│   Output results
```

## Tech Stack
- **Language**: C++17 (templates, operator overloading for matrices)
- **Math**: Custom matrix library or Eigen
- **Testing**: Google Test with IEEE benchmark systems
- **Build**: CMake

## Skills Demonstrated
- Numerical methods (Newton-Raphson, Jacobian)
- Power systems (load flow analysis)
- Linear algebra (matrix operations, sparse solvers)
- C++17 (templates, operator overloading)

Built by Isaac © 2026
