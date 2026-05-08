# 📡 Real-Time Market Research & Competitive Intelligence Platform

A full-stack AI-powered platform for market monitoring, sentiment analysis, competitor tracking, and strategic insights generation.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                  │
│  Dashboard │ News Feed │ Sentiment │ Competitors │ AI   │
└──────────────────────┬──────────────────────────────────┘
                       │  HTTP REST
┌──────────────────────▼──────────────────────────────────┐
│               BACKEND (Flask REST API)                   │
│  /api/news  │  /api/sentiment  │  /api/competitors       │
│  /api/trends │  /api/insights  │  /api/health            │
└──────┬───────────────┬─────────────────┬────────────────┘
       │               │                 │
┌──────▼──────┐ ┌──────▼──────┐ ┌───────▼───────┐
│  NLP Engine │ │Data Collector│ │   Databases   │
│  · VADER    │ │  · NewsAPI  │ │  · MongoDB    │
│  · TextBlob │ │  · RSS feeds│ │  · PostgreSQL │
│  · HuggingF │ │  · Scraper  │ │  · Redis      │
│  · LangChain│ └─────────────┘ └───────────────┘
└─────────────┘
```

---

## 🚀 Quick Start

### Option A — One-command start (recommended)

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bat
start.bat
```

### Option B — Manual setup

```bash
# 1. Clone / extract the project
cd market_intel

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate.bat         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys (see below)

# 5. Start Flask API  (Terminal 1)
python backend/app.py

# 6. Start Streamlit  (Terminal 2)
streamlit run frontend/streamlit_app.py
```

### Option C — Docker Compose

```bash
docker-compose up --build
```

Access:
- **Dashboard** → http://localhost:8501
- **API**        → http://localhost:5000/api/health

---

## 🔑 API Keys (Optional but recommended)

Edit `.env`:

| Variable | Where to get it | Required? |
|---|---|---|
| `NEWS_API_KEY` | https://newsapi.org (free tier: 100 req/day) | Optional* |
| `HUGGINGFACE_API_KEY` | https://huggingface.co/settings/tokens | Optional* |
| `MONGO_URI` | Local MongoDB or MongoDB Atlas | Optional* |

> \* The platform works out-of-the-box with **mock data** if no API keys are configured.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Streamlit-Option-Menu |
| **Backend** | Python 3.11, Flask, Flask-CORS |
| **AI / NLP** | HuggingFace Transformers, TextBlob, VaderSentiment, LangChain |
| **Database** | MongoDB (primary), PostgreSQL (optional) |
| **Cache** | Redis (optional) |
| **Visualization** | Plotly |
| **Scraping** | BeautifulSoup4, feedparser, requests |

---

## 📊 Features

### Dashboard
- Real-time KPIs: total articles, positive/negative signals, positive rate
- Sentiment distribution pie chart
- Articles by source bar chart
- Recent article feed with sentiment badges

### News Feed
- Search by keyword across NewsAPI, RSS feeds, or mock data
- Multi-engine NLP: VADER, TextBlob, HuggingFace, or Ensemble
- Per-article sentiment score, keywords extraction
- Save all results to MongoDB automatically

### Sentiment Analyser
- Paste any text for instant analysis
- Animated gauge (-1 to +1)
- Keyword extraction
- Engine-specific detailed breakdown

### Competitor Intelligence
- Market share pie chart
- Employee vs market share scatter plot
- Competitor directory table
- Per-competitor news monitoring with sentiment
- Add new competitors via UI

### Market Trends
- Top keyword frequency bar chart
- Sentiment over time area chart
- Sentiment score histogram

### AI Insights
- LangChain + HuggingFace strategic insight generation
- Extractive fallback when models unavailable
- Custom text summarisation

---

## 🛠️ API Reference

```
GET  /api/health                     Health check
POST /api/news/fetch                 Fetch & analyse articles
GET  /api/news/articles              List stored articles
POST /api/sentiment/analyse          Analyse text sentiment
GET  /api/sentiment/stats            Sentiment statistics
GET  /api/competitors                List competitors
POST /api/competitors/add            Add competitor
GET  /api/competitors/{name}/news    Competitor news
GET  /api/insights                   AI market insights
GET  /api/trends                     Keyword trends
POST /api/summarise                  Summarise text
```

---

## 🗂️ Project Structure

```
market_intel/
├── backend/
│   ├── app.py              Flask REST API
│   ├── nlp_engine.py       VADER + TextBlob + HF + LangChain
│   └── data_collector.py   NewsAPI + RSS + Scraper
├── database/
│   └── db.py               MongoDB + PostgreSQL helpers
├── frontend/
│   └── streamlit_app.py    Streamlit dashboard
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.ui
├── requirements.txt
├── .env.example
├── start.sh                Linux/Mac launcher
└── start.bat               Windows launcher
```

---

## ❓ Troubleshooting

**API Offline in sidebar:**
Make sure Flask is running: `python backend/app.py`

**MongoDB not connected:**
Platform auto-falls back to mock data. Install MongoDB locally or use Atlas.

**HuggingFace model slow:**
First run downloads models (~500MB). Use `vader` or `textblob` engine for instant results.

**Port already in use:**
Change `FLASK_PORT=5001` in `.env` and update `API_BASE_URL=http://localhost:5001/api`.
