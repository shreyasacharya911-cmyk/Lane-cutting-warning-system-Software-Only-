# Lane Cut Assist (LCA) System

## Disclaimer
> **Lane Cut Assist is a warning-only system. It does not control braking, steering, or throttle. The rider is solely responsible for the lane-change decision.**

## Overview
Lane Cut Assist (LCA) is a modular ADAS warning system for a two-wheeler (scooter) platform. Designed for an embedded Linux target (such as NVIDIA Jetson), it monitors the blind spot using side radar frames when the rider activates the turn indicator and triggers visual (HMI) and audible (buzzer) alerts when an approaching vehicle poses a lane-cut risk.

## Project Structure
```text
├── config/          # System and logging YAML configurations
├── docs/            # Architecture, requirements, and test plan
├── scripts/         # Build, deployment, and static analysis scripts
├── src/             # Core LCA pipeline modules and main entry point
├── tests/           # Unit and integration test suites
├── pyproject.toml   # Project, pytest, mypy, black, and pyright config
└── requirements.txt # Python dependencies
```

## Installation
```bash
pip install -r requirements.txt
```

## Running
From the project root directory:
```bash
python src/main.py
```
Or run as a module:
```bash
python -m src.main
```

## Testing & QA
Run the unit and integration test suite:
```bash
pytest tests/ -v
```

Run the full Linux/CI static analysis and test suite:
```bash
./scripts/run_static_analysis.sh
```

## Documentation
- [System Architecture](docs/architecture.md)
- [Requirements](docs/requirements.md)
- [Test Plan](docs/test_plan.md)
