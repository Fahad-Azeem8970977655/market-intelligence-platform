# 📡 Real-Time Market Research & Competitive Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?logo=huggingface)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb)
![License](https://img.shields.io/badge/License-MIT-purple)

A full-stack, production-grade AI platform for automated news monitoring,
multi-engine NLP sentiment analysis, competitor tracking, keyword trend
detection, and LangChain-powered strategic insight generation — all wrapped
in an interactive Streamlit dashboard.

---

## 🖥️ Demo Screenshots

> Add screenshots here after running the app
> `![Dashboard](screenshots/dashboard.png)`

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────┐
│              FRONTEND  (Streamlit)               │
│  Dashboard │ News │ Sentiment │ Competitors │ AI │
└─────────────────────┬───────────────────────────┘
│  REST API
┌─────────────────────▼───────────────────────────┐
│              BACKEND  (Flask)                    │
│  /news  │  /sentiment  │  /competitors           │
│  /trends │  /insights  │  /health                │
└──────┬──────────────┬─────────────┬─────────────┘
│              │             │
┌──────▼─────┐ ┌──────▼────┐ ┌────▼──────────┐
│ NLP Engine │ │  Data      │ │  Databases    │
│ · VADER    │ │  Collector │ │  · MongoDB    │
│ · TextBlob │ │  · NewsAPI │ │  · PostgreSQL │
│ · HuggingF │ │  · RSS     │ │  · Redis      │
│ · LangChain│ │  · Scraper │ └───────────────┘
└────────────┘ └───────────┘

---

## ✨ Features

| Module | What it does |
|---|---|
| 📰 **News Feed** | Fetches & analyses articles from NewsAPI, RSS, web scraping |
| 🎭 **Sentiment Engine** | Ensemble of VADER + TextBlob + HuggingFace Transformers |
| 🎯 **Competitor Intel** | Market share tracking, employee metrics, competitor news monitoring |
| 📈 **Trend Analysis** | Keyword frequency, sentiment-over-time, score distribution |
| ⚡ **AI Insights** | LangChain + HuggingFace strategic insight & summarization |
| 🗃️ **Dual Database** | MongoDB (articles) + PostgreSQL (structured) + Redis (cache) |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/market-intelligence-platform.git
cd market-intelligence-platform
```

### 2. Create virtual environment
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Open .env and add your API keys
```

### 5. Run the platform

**Terminal 1 — Flask API:**
```bash
python backend/app.py
```

**Terminal 2 — Streamlit Dashboard:**
```bash
streamlit run frontend/streamlit_app.py
```

Open → **http://localhost:8501**

---

## 🐳 Docker (One Command)

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Dashboard | http://localhost:8501 |
| Flask API | http://localhost:5000/api/health |

---

## 🔑 API Keys

| Variable | Source | Required? |
|---|---|---|
| `NEWS_API_KEY` | newsapi.org (free) | Optional* |
| `HUGGINGFACE_API_KEY` | huggingface.co (free) | Optional* |
| `MONGO_URI` | Local or Atlas (free) | Optional* |

> *Platform works with built-in mock data if no keys are configured.

---

## 📁 Project Structure
market-intelligence-platform/
├── backend/
│   ├── app.py                 # Flask REST API
│   ├── nlp_engine.py          # VADER + TextBlob + HuggingFace + LangChain
│   └── data_collector.py      # NewsAPI + RSS + scraper
├── database/
│   └── db.py                  # MongoDB + PostgreSQL
├── frontend/
│   └── streamlit_app.py       # Streamlit dashboard
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.ui
├── requirements.txt
├── .env.example
└── README.md

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Plotly |
| Backend | Python 3.11, Flask, Flask-CORS |
| AI / NLP | HuggingFace Transformers, LangChain, VaderSentiment, TextBlob |
| Databases | MongoDB, PostgreSQL, Redis |
| Scraping | BeautifulSoup4, feedparser, NewsAPI |
| DevOps | Docker, Docker Compose |

---

## 📊 API Endpoints
GET  /api/health                      Health check
POST /api/news/fetch                  Fetch & analyse articles
GET  /api/news/articles               List stored articles
POST /api/sentiment/analyse           Analyse any text
GET  /api/sentiment/stats             Sentiment statistics
GET  /api/competitors                 Competitor list
POST /api/competitors/add             Add competitor
GET  /api/competitors/{name}/news     Competitor news feed
GET  /api/insights                    AI market insights
GET  /api/trends                      Keyword trends
POST /api/summarise                   Summarise text

---

## 🤝 Contributing

Pull requests are welcome. For major changes please open an issue first.

---

## 📄 License

[MIT](LICENSE)
