#!/usr/bin/env bash
# ═══════════════════════════════════════════════════
#  Market Intelligence Platform — Quick Start Script
# ═══════════════════════════════════════════════════
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ██████████████████████████████████████"
echo "  █  Market Intelligence Platform  █"
echo "  ██████████████████████████████████████"
echo -e "${NC}"

# 1. Create .env if missing
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚙  Creating .env from .env.example …${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓  .env created — edit it to add your API keys${NC}"
fi

# 2. Create virtualenv if missing
if [ ! -d venv ]; then
    echo -e "${YELLOW}⚙  Creating virtual environment …${NC}"
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Install dependencies
echo -e "${YELLOW}⚙  Installing dependencies (this may take a few minutes) …${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓  Dependencies installed${NC}"

# 4. Start Flask API in background
echo -e "${YELLOW}🚀 Starting Flask API on http://localhost:5000 …${NC}"
python backend/app.py &
API_PID=$!
sleep 3

# 5. Check API health
if curl -sf http://localhost:5000/api/health > /dev/null; then
    echo -e "${GREEN}✓  Flask API is running (PID $API_PID)${NC}"
else
    echo -e "${RED}✗  Flask API failed to start — check logs above${NC}"
fi

# 6. Start Streamlit
echo -e "${YELLOW}🚀 Starting Streamlit UI on http://localhost:8501 …${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Dashboard: http://localhost:8501${NC}"
echo -e "${GREEN}  API:       http://localhost:5000/api/health${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
streamlit run frontend/streamlit_app.py \
    --server.port 8501 \
    --server.headless true

# Cleanup on exit
kill $API_PID 2>/dev/null || true
