"""
Data Collection Module
- News API
- RSS feeds
- Web scraping (BeautifulSoup)
- Competitor monitoring
"""
import os
import time
import hashlib
import requests
import feedparser
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from loguru import logger

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
except ImportError:
    BS4_OK = False

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# ─── News API ─────────────────────────────────────────────────────────────────

def fetch_newsapi(query: str, page_size: int = 30) -> List[Dict[str, Any]]:
    if not NEWS_API_KEY:
        logger.warning("NEWS_API_KEY not set – using mock data")
        return _mock_articles(query, page_size)
    url = "https://newsapi.org/v2/everything"
    params = {
        "q":        query,
        "pageSize": min(page_size, 100),
        "sortBy":   "publishedAt",
        "language": "en",
        "apiKey":   NEWS_API_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        articles = []
        for item in data.get("articles", []):
            articles.append({
                "title":        item.get("title", ""),
                "content":      item.get("description", "") or item.get("content", ""),
                "source":       item.get("source", {}).get("name", "Unknown"),
                "url":          item.get("url", ""),
                "published_at": item.get("publishedAt", datetime.utcnow().isoformat()),
                "image_url":    item.get("urlToImage", ""),
                "query":        query,
            })
        return articles
    except Exception as e:
        logger.error(f"NewsAPI error: {e}")
        return _mock_articles(query, page_size)


# ─── RSS feed collector ───────────────────────────────────────────────────────

RSS_FEEDS = {
    "Technology":   "https://feeds.feedburner.com/TechCrunch",
    "Finance":      "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "Business":     "https://feeds.bbci.co.uk/news/business/rss.xml",
    "AI/ML":        "https://medium.com/feed/tag/artificial-intelligence",
    "Startup":      "https://www.entrepreneur.com/latest.rss",
    "Marketing":    "https://feeds.feedblitz.com/marketingland/all",
}


def fetch_rss(category: str = "Technology", limit: int = 20) -> List[Dict[str, Any]]:
    url = RSS_FEEDS.get(category)
    if not url:
        return []
    try:
        feed     = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:limit]:
            published = entry.get("published", datetime.utcnow().isoformat())
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(published).isoformat()
            except Exception:
                dt = datetime.utcnow().isoformat()
            articles.append({
                "title":        entry.get("title", ""),
                "content":      entry.get("summary", ""),
                "source":       feed.feed.get("title", category),
                "url":          entry.get("link", ""),
                "published_at": dt,
                "image_url":    "",
                "query":        category,
            })
        return articles
    except Exception as e:
        logger.error(f"RSS fetch error ({category}): {e}")
        return []


# ─── Web scraper ──────────────────────────────────────────────────────────────

def scrape_competitor_page(url: str) -> Dict[str, Any]:
    if not BS4_OK:
        return {"error": "beautifulsoup4 not installed"}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MarketIntelBot/1.0)"}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup  = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string.strip() if soup.title else url
        # grab visible text paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40]
        content    = " ".join(paragraphs[:15])
        meta_desc  = ""
        meta_tag   = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_desc = meta_tag.get("content", "")
        return {
            "url":         url,
            "title":       title,
            "description": meta_desc,
            "content":     content[:2000],
            "scraped_at":  datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Scrape error ({url}): {e}")
        return {"url": url, "error": str(e)}


# ─── Mock data (when APIs not configured) ────────────────────────────────────

def _mock_articles(query: str, n: int = 10) -> List[Dict[str, Any]]:
    """Realistic-looking mock articles for demo / offline mode."""
    templates = [
        ("{query} Market Sees Record Growth in Q2 2025",
         "Industry analysts report unprecedented expansion in the {query} sector, with revenues surging 34% year-over-year driven by enterprise adoption and innovation."),
        ("Top Competitors Ramp Up {query} Investment",
         "Leading players in the {query} space are doubling R&D budgets, signalling fierce competition ahead. Analysts expect consolidation within 12 months."),
        ("{query} Faces Regulatory Scrutiny",
         "Regulators are examining business practices within the {query} industry. Compliance costs could rise significantly for market participants."),
        ("AI Transforms {query} Operations",
         "Companies leveraging AI in {query} are seeing 25–40% efficiency gains, disrupting traditional business models and creating new competitive dynamics."),
        ("Startup Disrupts Traditional {query} Value Chain",
         "A well-funded startup has raised $120M to challenge incumbents in the {query} market with a platform-first approach and aggressive pricing."),
        ("{query} Consumers Shift Preferences Post-Pandemic",
         "New research reveals dramatic shifts in {query} consumer behaviour, with digital-first approaches now preferred by over 70% of buyers surveyed."),
        ("Global Supply Chain Impacts {query} Sector",
         "Ongoing supply chain pressures continue to affect {query} companies, with lead times doubling and costs rising across the board."),
        ("{query} ESG Initiatives Gain Momentum",
         "Sustainability targets are reshaping the {query} landscape as investors demand transparency and accountability from market leaders."),
    ]
    articles = []
    for i, (title_tpl, content_tpl) in enumerate(templates[:n]):
        articles.append({
            "title":       title_tpl.format(query=query),
            "content":     content_tpl.format(query=query),
            "source":      ["Reuters", "Bloomberg", "TechCrunch", "Forbes", "WSJ"][i % 5],
            "url":         f"https://example.com/article-{hashlib.md5((title_tpl+query).encode()).hexdigest()[:8]}",
            "published_at": datetime.utcnow().isoformat(),
            "image_url":   "",
            "query":       query,
        })
    return articles


# ─── Competitor intelligence ──────────────────────────────────────────────────

SAMPLE_COMPETITORS = [
    {"name": "TechCorp Alpha",  "website": "https://techcorp-alpha.example.com",  "industry": "SaaS",       "market_share": 23.4, "founded": 2015, "employees": 1200},
    {"name": "DataVision Pro",  "website": "https://datavision-pro.example.com",  "industry": "Analytics",  "market_share": 18.7, "founded": 2017, "employees":  850},
    {"name": "InnovateMind",    "website": "https://innovatemind.example.com",    "industry": "AI/ML",      "market_share": 15.2, "founded": 2019, "employees":  430},
    {"name": "QuantumLeap Inc", "website": "https://quantumleap.example.com",     "industry": "Enterprise", "market_share": 12.8, "founded": 2012, "employees": 3400},
    {"name": "NexGen Systems",  "website": "https://nexgen-sys.example.com",      "industry": "Cloud",      "market_share": 10.1, "founded": 2016, "employees":  620},
    {"name": "PulseMetrics",    "website": "https://pulsemetrics.example.com",    "industry": "BI",         "market_share":  8.9, "founded": 2018, "employees":  310},
]


def get_competitor_data() -> List[Dict[str, Any]]:
    return SAMPLE_COMPETITORS


def monitor_competitor_news(competitor_name: str, limit: int = 10) -> List[Dict]:
    return fetch_newsapi(f'"{competitor_name}"', page_size=limit) or _mock_articles(competitor_name, limit)
