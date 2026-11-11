#!/bin/bash
set -e

echo "Running Black formatting check..."
black --check src/ tests/ || (echo "Black failed. Run 'black src/ tests/' to fix." && exit 1)

echo "Running Flake8 linting..."
flake8 src/ tests/

echo "Running MyPy type checking..."
mypy src/ tests/

echo "Running Bandit security analysis..."
bandit -r src/ -lll

echo "Running Pytest suite..."
pytest tests/ -v

echo "All checks passed successfully."
