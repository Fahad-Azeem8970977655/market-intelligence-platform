"""
Flask REST API — Market Intelligence Platform
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

load_dotenv()

from backend.nlp_engine    import analyse_sentiment, analyse_sentiment_ensemble, extract_keywords, generate_market_insights, summarise_text
from backend.data_collector import fetch_newsapi, fetch_rss, get_competitor_data, monitor_competitor_news, _mock_articles
from database.db            import (
    save_article_mongo, get_articles_mongo,
    save_competitor_mongo, get_competitors_mongo,
    get_sentiment_stats_mongo, ping_mongo,
)

app = Flask(__name__)
CORS(app)

# ─── Health ───────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status":   "ok",
        "mongodb":  ping_mongo(),
        "timestamp": datetime.utcnow().isoformat(),
    })


# ─── News & sentiment ─────────────────────────────────────────────────────────

@app.route("/api/news/fetch", methods=["POST"])
def news_fetch():
    body     = request.get_json() or {}
    query    = body.get("query", "technology")
    source   = body.get("source", "newsapi")   # newsapi | rss | mock
    limit    = int(body.get("limit", 20))
    method   = body.get("sentiment_method", "ensemble")  # vader | textblob | huggingface | ensemble

    if source == "rss":
        raw_articles = fetch_rss(query, limit)
    elif source == "mock":
        raw_articles = _mock_articles(query, limit)
    else:
        raw_articles = fetch_newsapi(query, limit)

    enriched = []
    for article in raw_articles:
        text = f"{article.get('title','')} {article.get('content','')}"
        if method == "ensemble":
            sentiment_result = analyse_sentiment_ensemble(text)
        else:
            sentiment_result = analyse_sentiment(text, method)

        article["sentiment"]       = sentiment_result["label"]
        article["sentiment_score"] = sentiment_result["score"]
        article["keywords"]        = extract_keywords(text)
        article["category"]        = query

        save_article_mongo(article)
        enriched.append(article)

    return jsonify({"articles": enriched, "count": len(enriched)})


@app.route("/api/news/articles", methods=["GET"])
def news_articles():
    limit     = int(request.args.get("limit", 50))
    sentiment = request.args.get("sentiment")
    category  = request.args.get("category")
    keyword   = request.args.get("keyword")
    articles  = get_articles_mongo(limit, sentiment, category, keyword)
    if not articles:
        # Return mock data if DB empty
        raw = _mock_articles("market", limit)
        for a in raw:
            text = f"{a.get('title','')} {a.get('content','')}"
            res  = analyse_sentiment_ensemble(text)
            a["sentiment"]       = res["label"]
            a["sentiment_score"] = res["score"]
            a["keywords"]        = extract_keywords(text)
        articles = raw
    return jsonify({"articles": articles, "count": len(articles)})


@app.route("/api/sentiment/analyse", methods=["POST"])
def sentiment_analyse():
    body   = request.get_json() or {}
    text   = body.get("text", "")
    method = body.get("method", "ensemble")
    if not text:
        return jsonify({"error": "text required"}), 400
    if method == "ensemble":
        result = analyse_sentiment_ensemble(text)
    else:
        result = analyse_sentiment(text, method)
    result["keywords"] = extract_keywords(text)
    return jsonify(result)


@app.route("/api/sentiment/stats", methods=["GET"])
def sentiment_stats():
    stats = get_sentiment_stats_mongo()
    if not stats["breakdown"]:
        # mock stats
        stats = {
            "breakdown": [
                {"_id": "positive", "count": 42, "avg_score":  0.61},
                {"_id": "neutral",  "count": 28, "avg_score":  0.02},
                {"_id": "negative", "count": 18, "avg_score": -0.55},
            ]
        }
    return jsonify(stats)


@app.route("/api/summarise", methods=["POST"])
def summarise():
    body = request.get_json() or {}
    text = body.get("text", "")
    if not text:
        return jsonify({"error": "text required"}), 400
    summary = summarise_text(text)
    return jsonify({"summary": summary})


# ─── Competitor Intelligence ──────────────────────────────────────────────────

@app.route("/api/competitors", methods=["GET"])
def competitors_list():
    data = get_competitors_mongo()
    if not data:
        data = get_competitor_data()
        for c in data:
            save_competitor_mongo(c)
    return jsonify({"competitors": data, "count": len(data)})


@app.route("/api/competitors/add", methods=["POST"])
def competitor_add():
    body = request.get_json() or {}
    name = body.get("name")
    if not name:
        return jsonify({"error": "name required"}), 400
    _id = save_competitor_mongo(body)
    return jsonify({"id": _id, "status": "saved"})


@app.route("/api/competitors/<name>/news", methods=["GET"])
def competitor_news(name: str):
    limit    = int(request.args.get("limit", 10))
    articles = monitor_competitor_news(name, limit)
    for a in articles:
        text = f"{a.get('title','')} {a.get('content','')}"
        res  = analyse_sentiment_ensemble(text)
        a["sentiment"]       = res["label"]
        a["sentiment_score"] = res["score"]
    return jsonify({"competitor": name, "articles": articles})


# ─── Market Insights ─────────────────────────────────────────────────────────

@app.route("/api/insights", methods=["GET"])
def market_insights():
    articles = get_articles_mongo(limit=30)
    if not articles:
        articles = _mock_articles("technology", 20)
        for a in articles:
            text = f"{a.get('title','')} {a.get('content','')}"
            res  = analyse_sentiment_ensemble(text)
            a["sentiment"] = res["label"]
    insights = generate_market_insights(articles)
    return jsonify({"insights": insights, "based_on": len(articles)})


# ─── Trend analysis ───────────────────────────────────────────────────────────

@app.route("/api/trends", methods=["GET"])
def trends():
    """Aggregate keyword frequency across stored articles."""
    articles = get_articles_mongo(limit=100)
    if not articles:
        articles = _mock_articles("technology market AI", 30)
    all_keywords: dict = {}
    for a in articles:
        for kw in a.get("keywords", []):
            all_keywords[kw] = all_keywords.get(kw, 0) + 1
    top_trends = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:20]
    return jsonify({
        "trends": [{"keyword": k, "frequency": v} for k, v in top_trends]
    })


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    logger.info(f"Starting Market Intelligence API on port {port}")
    app.run(debug=True, port=port, host="0.0.0.0")
