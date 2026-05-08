# 📡 Real-Time Market Research & Competitive Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?logo=huggingface&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2-teal?logo=chainlink&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple)

> A full-stack, production-grade AI platform for automated news monitoring, multi-engine NLP sentiment analysis, competitor tracking, keyword trend detection, and LangChain-powered strategic insight generation — wrapped in an interactive Streamlit dashboard.

---

## 📸 Dashboard Preview

```
┌─────────────────────────────────────────────────────────┐
│  📡 MarketIQ  |  Dashboard  News  Sentiment  Insights   │
├───────────────┬───────────────┬───────────────┬─────────┤
│ Total Articles│Positive Signal│Negative Signal│Pos Rate │
│     100       │      62       │      18       │  62%    │
├───────────────┴───────────────┴───────────────┴─────────┤
│  Sentiment Pie Chart   │   Articles by Source Bar Chart  │
├────────────────────────┴─────────────────────────────────┤
│  Recent Articles Feed with Sentiment Badges + Keywords   │
└──────────────────────────────────────────────────────────┘
```

> 📷 Add real screenshots to `/screenshots` folder after running the app.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND  (Streamlit)                   │
│                                                         │
│  📊 Dashboard  📰 News Feed  🎭 Sentiment Analyser      │
│  🎯 Competitor Intel  📈 Trends  ⚡ AI Insights          │
└──────────────────────┬──────────────────────────────────┘
                       │  HTTP REST API
┌──────────────────────▼──────────────────────────────────┐
│                  BACKEND  (Flask)                        │
│                                                         │
│  /api/news  │  /api/sentiment  │  /api/competitors       │
│  /api/trends  │  /api/insights  │  /api/health           │
└──────┬───────────────┬──────────────────┬───────────────┘
       │               │                  │
┌──────▼──────┐ ┌──────▼──────┐  ┌───────▼───────────┐
│  NLP Engine │ │Data Collector│  │    Databases       │
│             │ │             │  │                    │
│  · VADER    │ │  · NewsAPI  │  │  · MongoDB         │
│  · TextBlob │ │  · RSS Feeds│  │  · PostgreSQL      │
│  · HuggingF │ │  · BS4 Web  │  │  · Redis (cache)   │
│  · LangChain│ │    Scraper  │  │                    │
└─────────────┘ └─────────────┘  └────────────────────┘
```

---

## ✨ Features

| Module | Description |
|---|---|
| 📰 **Live News Feed** | Aggregates articles from NewsAPI, RSS feeds, and web scraping via BeautifulSoup |
| 🎭 **Ensemble Sentiment Engine** | Combines VADER + TextBlob + HuggingFace Transformers for consensus scoring |
| 🎯 **Competitor Intelligence** | Market share charts, employee metrics, per-competitor news monitoring |
| 📈 **Trend Analysis** | Keyword frequency ranking, sentiment-over-time area chart, score histogram |
| ⚡ **AI Insights Generator** | LangChain + HuggingFace pipeline for strategic recommendations & summarisation |
| 🗃️ **Dual Database** | MongoDB (unstructured articles) + PostgreSQL (structured records) + Redis (cache) |
| 🐳 **Docker Ready** | Full docker-compose setup for one-command deployment |
| 🔌 **REST API** | 11 documented endpoints — easily integrable with Power BI, Tableau, or any frontend |

---

## 🚀 Quick Start

### Option 1 — Automated Script (Recommended)

**Linux / macOS:**
```bash
git clone https://github.com/YOUR_USERNAME/market-intelligence-platform.git
cd market-intelligence-platform
chmod +x start.sh
./start.sh
```

**Windows:**
```bat
git clone https://github.com/YOUR_USERNAME/market-intelligence-platform.git
cd market-intelligence-platform
start.bat
```

---

### Option 2 — Manual Setup

**Step 1: Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/market-intelligence-platform.git
cd market-intelligence-platform
```

**Step 2: Create virtual environment**
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Configure environment**
```bash
cp .env.example .env
# Open .env in any text editor and add your API keys
```

**Step 5: Start Flask API** *(Terminal 1)*
```bash
python backend/app.py
```

**Step 6: Start Streamlit Dashboard** *(Terminal 2)*
```bash
streamlit run frontend/streamlit_app.py
```

Open your browser → **http://localhost:8501** 🎉

---

### Option 3 — Docker Compose

```bash
git clone https://github.com/YOUR_USERNAME/market-intelligence-platform.git
cd market-intelligence-platform
docker-compose up --build
```

---

## 🌐 Access URLs

| Service | URL |
|---|---|
| 📊 Streamlit Dashboard | http://localhost:8501 |
| 🔌 Flask REST API | http://localhost:5000 |
| ❤️ Health Check | http://localhost:5000/api/health |

---

## 🔑 API Keys Configuration

Open `.env` and fill in your keys. The platform runs with **mock data by default** — no keys required to test.

| Variable | Where to Get | Tier |
|---|---|---|
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) | Free (100 req/day) |
| `HUGGINGFACE_API_KEY` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | Free |
| `MONGO_URI` | Local MongoDB or [MongoDB Atlas](https://www.mongodb.com/atlas) | Free tier available |
| `POSTGRES_URI` | Local PostgreSQL or [Supabase](https://supabase.com) | Free tier available |

```env
NEWS_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here
MONGO_URI=mongodb://localhost:27017/
POSTGRES_URI=postgresql://user:password@localhost:5432/market_intel
```

---

## 📁 Project Structure

```
market-intelligence-platform/
│
├── backend/
│   ├── app.py                  # Flask REST API — 11 endpoints
│   ├── nlp_engine.py           # VADER + TextBlob + HuggingFace + LangChain
│   └── data_collector.py       # NewsAPI + RSS + BeautifulSoup scraper
│
├── database/
│   └── db.py                   # MongoDB + PostgreSQL connection & helpers
│
├── frontend/
│   └── streamlit_app.py        # Streamlit 6-page dashboard
│
├── screenshots/                # Add your screenshots here
│
├── docker-compose.yml          # Full stack orchestration
├── Dockerfile.api              # Flask API container
├── Dockerfile.ui               # Streamlit container
├── requirements.txt            # All Python dependencies
├── .env.example                # Environment variable template
├── start.sh                    # Linux/Mac one-click launcher
├── start.bat                   # Windows one-click launcher
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit 1.35 | Interactive dashboard UI |
| **Visualization** | Plotly 5.22 | Charts, gauges, graphs |
| **Backend** | Flask 3.0 + Flask-CORS | REST API server |
| **Sentiment (Fast)** | VaderSentiment | Lexicon-based, real-time |
| **Sentiment (NLP)** | TextBlob | Polarity + subjectivity |
| **Sentiment (Deep)** | HuggingFace Transformers | Deep learning models |
| **AI Orchestration** | LangChain 0.2 | Summarisation + insights |
| **Embeddings** | sentence-transformers | Semantic similarity |
| **Primary DB** | MongoDB 7 | Articles + unstructured data |
| **Secondary DB** | PostgreSQL 16 | Structured records + ORM |
| **Cache** | Redis 7 | Response caching |
| **Scraping** | BeautifulSoup4, feedparser | Web + RSS data collection |
| **News API** | NewsAPI.org | Live news aggregation |
| **DevOps** | Docker + Docker Compose | Containerised deployment |

---

## 📊 API Endpoints Reference

```
GET  /api/health                       System health check
───────────────────────────────────────────────────────────
POST /api/news/fetch                   Fetch & NLP-enrich articles
GET  /api/news/articles                List stored articles (filterable)
───────────────────────────────────────────────────────────
POST /api/sentiment/analyse            Analyse any text (all engines)
GET  /api/sentiment/stats              Sentiment breakdown statistics
───────────────────────────────────────────────────────────
GET  /api/competitors                  List all competitors
POST /api/competitors/add              Add a new competitor
GET  /api/competitors/{name}/news      Monitor competitor news feed
───────────────────────────────────────────────────────────
GET  /api/insights                     AI-generated market insights
GET  /api/trends                       Top keyword trends
POST /api/summarise                    Summarise any article/text
```

### Example Request
```bash
curl -X POST http://localhost:5000/api/sentiment/analyse \
  -H "Content-Type: application/json" \
  -d '{"text": "The market is showing strong bullish signals this quarter", "method": "ensemble"}'
```

### Example Response
```json
{
  "label": "positive",
  "score": 0.724,
  "keywords": ["market", "bullish", "signals", "quarter", "strong"],
  "details": {
    "vader":    {"label": "positive", "score": 0.681},
    "textblob": {"label": "positive", "score": 0.767}
  }
}
```

---

## 📈 Dashboard Pages

### 1. 📊 Dashboard
Real-time KPIs, sentiment pie chart, articles-by-source bar chart, recent article feed with sentiment badges and keyword tags.

### 2. 📰 News Feed
Search any keyword, choose data source (NewsAPI / RSS / Mock), select NLP engine, fetch and display enriched articles with scores and keywords.

### 3. 🎭 Sentiment Analyser
Paste any text — get instant sentiment label, animated gauge (-1 to +1), keyword cloud, and detailed per-engine breakdown.

### 4. 🎯 Competitor Intelligence
Market share pie chart, employee vs market-share scatter, competitor directory table, per-competitor live news monitoring, add-competitor form.

### 5. 📈 Market Trends
Top-20 keyword frequency bar chart, sentiment-over-time area chart, sentiment score distribution histogram.

### 6. ⚡ AI Insights
One-click strategic insight generation from 30+ articles, custom text summarisation, sentiment stats overview.

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 🗺️ Roadmap

- [ ] Scheduled auto-fetch (APScheduler — daily news collection)
- [ ] Export to Excel / PDF reports
- [ ] Email alerting when negative sentiment exceeds threshold
- [ ] User authentication (streamlit-authenticator)
- [ ] Power BI / Tableau connector
- [ ] Multi-language sentiment support

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
- 📧 Email: fahadazeem880@gmail.com

---

## ⭐ Support

If you found this project useful, please consider giving it a **star** ⭐ on GitHub — it helps others discover it!

---

*Built with ❤️ using Python, Flask, Streamlit, and HuggingFace*
