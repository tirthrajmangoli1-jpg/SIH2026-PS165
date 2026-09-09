#!/usr/bin/env bash
# OIL SIF-Sentinel Launcher Script
# Smart India Hackathon: PS 165 - Fatality Precursors in OIL's Safety Reports

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="/Users/tirthsmac/.gemini/antigravity/scratch/venv"
NODE_BIN="/Users/tirthsmac/.gemini/antigravity/scratch/tools/node-v20.18.0-darwin-arm64/bin"

export PATH="$NODE_BIN:$PATH"
PORT="${PORT:-8000}"

echo "=========================================================="
echo "    OIL SIF-SENTINEL: FATALITY PRECURSOR RADAR (PS 165)    "
echo "        Oil India Limited - Operations Safety Radar        "
echo "=========================================================="

echo "[1/3] Checking environment & dependencies..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Python virtual environment not found at $VENV_DIR"
    exit 1
fi

echo "[2/3] Building latest React frontend bundle..."
cd "$SCRIPT_DIR/frontend"
npm run build

echo "[3/3] Freeing existing processes on port $PORT (if any)..."
lsof -ti :"$PORT" 2>/dev/null | xargs kill -9 2>/dev/null || true

echo "----------------------------------------------------------"
echo "✓ Web Application:   http://localhost:$PORT"
echo "✓ OpenAPI / Docs:    http://localhost:$PORT/docs"
echo "✓ API Health:        http://localhost:$PORT/api/health"
echo "----------------------------------------------------------"

cd "$SCRIPT_DIR/backend"
"$VENV_DIR/bin/uvicorn" app.main:app --host 0.0.0.0 --port "$PORT"
