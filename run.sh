#!/usr/bin/env bash
# ==============================================================================
# ResolveFlow AI: One-Click Startup Script for CA-3 PoC
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

export STREAMLIT_CONFIG_DIR="$DIR/.streamlit"

echo "===================================================================="
echo "Starting ResolveFlow AI: Multi-Agent Customer Support PoC"
echo "===================================================================="

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv..."
    /opt/homebrew/bin/python3.12 -m venv .venv || python3 -m venv .venv
    echo "Installing required dependencies..."
    .venv/bin/pip install -r requirements.txt
fi

# Run test suite to verify health
echo "Running automated verification tests..."
.venv/bin/python -m unittest tests/test_pipeline.py

# Ensure PowerPoint is generated
if [ ! -f "ResolveFlow_AI_Presentation.pptx" ]; then
    echo "Programmatically generating PowerPoint slide deck..."
    .venv/bin/python scripts/generate_presentation.py
fi

echo "Launching Streamlit Interactive Dashboard on http://localhost:8501 ..."
.venv/bin/streamlit run app.py
