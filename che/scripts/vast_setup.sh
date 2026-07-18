#!/usr/bin/env bash
# One-shot setup + gate run on a fresh vast.ai CUDA box (run from repo root):
#   bash che/scripts/vast_setup.sh
# Prereq: the repo is on the box (git clone or rsync; exclude .venv/.git).
set -euo pipefail

command -v uv >/dev/null 2>&1 || {
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
}

uv sync --extra cuda
uv run python -c "import jax; print('devices:', jax.devices())"
uv run python -m che.bench.throughput --out che/bench/results/gate_report.md
echo "=== gate report ==="
cat che/bench/results/gate_report.md
