"""
Database Layer - MongoDB + PostgreSQL support
"""
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from loguru import logger

# ─── MongoDB Connection ───────────────────────────────────────────────────────
try:
    from pymongo import MongoClient, DESCENDING
    from pymongo.errors import ConnectionFailure

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB  = os.getenv("MONGO_DB", "market_intelligence")

    _client: Optional[MongoClient] = None

    def get_mongo_client() -> MongoClient:
        global _client
        if _client is None:
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        return _client

    def get_db():
        return get_mongo_client()[MONGO_DB]

    def ping_mongo() -> bool:
        try:
            get_mongo_client().admin.command("ping")
            return True
        except Exception:
            return False

except ImportError:
    logger.warning("pymongo not installed - MongoDB unavailable")
    def get_db(): return None
    def ping_mongo(): return False


# ─── PostgreSQL Connection ────────────────────────────────────────────────────
try:
    from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
    from sqlalchemy.orm import declarative_base, sessionmaker

    POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://user:password@localhost:5432/market_intel")

    Base = declarative_base()

    class Article(Base):
        __tablename__ = "articles"
        id            = Column(Integer, primary_key=True)
        title         = Column(String(500))
        content       = Column(Text)
        source        = Column(String(200))
        url           = Column(String(1000))
        published_at  = Column(DateTime)
        sentiment     = Column(String(20))
        sentiment_score = Column(Float)
        keywords      = Column(JSON)
        category      = Column(String(100))
        created_at    = Column(DateTime, default=datetime.utcnow)

    class Competitor(Base):
        __tablename__ = "competitors"
        id            = Column(Integer, primary_key=True)
        name          = Column(String(200))
        website       = Column(String(500))
        industry      = Column(String(200))
        description   = Column(Text)
        metrics       = Column(JSON)
        last_updated  = Column(DateTime, default=datetime.utcnow)

    class MarketSignal(Base):
        __tablename__ = "market_signals"
        id            = Column(Integer, primary_key=True)
        signal_type   = Column(String(100))
        title         = Column(String(500))
        description   = Column(Text)
        strength      = Column(Float)
        source        = Column(String(200))
        detected_at   = Column(DateTime, default=datetime.utcnow)
        metadata      = Column(JSON)

    def get_pg_engine():
        return create_engine(POSTGRES_URI)

    def get_pg_session():
        engine  = get_pg_engine()
        Session = sessionmaker(bind=engine)
        return Session()

    def init_postgres():
        try:
            engine = get_pg_engine()
            Base.metadata.create_all(engine)
            logger.info("PostgreSQL tables initialised")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL init failed: {e}")
            return False

except ImportError:
    logger.warning("sqlalchemy not installed - PostgreSQL unavailable")
    def init_postgres(): return False


# ─── MongoDB helpers ──────────────────────────────────────────────────────────

def save_article_mongo(article: Dict[str, Any]) -> Optional[str]:
    try:
        db  = get_db()
        col = db["articles"]
        # avoid duplicates
        existing = col.find_one({"url": article.get("url")})
        if existing:
            return str(existing["_id"])
        article["created_at"] = datetime.utcnow()
        result = col.insert_one(article)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"save_article_mongo error: {e}")
        return None


def get_articles_mongo(
    limit: int = 100,
    sentiment: Optional[str] = None,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
) -> List[Dict]:
    try:
        db    = get_db()
        query: Dict[str, Any] = {}
        if sentiment: query["sentiment"] = sentiment
        if category:  query["category"]  = category
        if keyword:   query["$text"]      = {"$search": keyword}
        cursor = db["articles"].find(query).sort("published_at", DESCENDING).limit(limit)
        articles = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            articles.append(doc)
        return articles
    except Exception as e:
        logger.error(f"get_articles_mongo error: {e}")
        return []


def save_competitor_mongo(competitor: Dict[str, Any]) -> Optional[str]:
    try:
        db  = get_db()
        col = db["competitors"]
        existing = col.find_one({"name": competitor.get("name")})
        if existing:
            col.update_one({"_id": existing["_id"]}, {"$set": competitor})
            return str(existing["_id"])
        competitor["created_at"] = datetime.utcnow()
        result = col.insert_one(competitor)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"save_competitor_mongo error: {e}")
        return None


def get_competitors_mongo() -> List[Dict]:
    try:
        db     = get_db()
        cursor = db["competitors"].find({})
        competitors = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            competitors.append(doc)
        return competitors
    except Exception as e:
        logger.error(f"get_competitors_mongo error: {e}")
        return []


def get_sentiment_stats_mongo() -> Dict[str, Any]:
    try:
        db       = get_db()
        pipeline = [
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}, "avg_score": {"$avg": "$sentiment_score"}}},
            {"$sort":  {"count": -1}},
        ]
        results = list(db["articles"].aggregate(pipeline))
        return {"breakdown": results}
    except Exception as e:
        logger.error(f"get_sentiment_stats_mongo error: {e}")
        return {"breakdown": []}
