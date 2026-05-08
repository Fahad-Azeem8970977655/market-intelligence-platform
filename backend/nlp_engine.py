"""
AI / NLP Engine
- VaderSentiment  (fast, lexicon-based)
- TextBlob        (subjectivity + polarity)
- HuggingFace     (deep-learning sentiment)
- LangChain       (summarisation + insights)
"""
import os
import re
from typing import Dict, List, Any, Optional
from loguru import logger

# ─── VaderSentiment ───────────────────────────────────────────────────────────
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _vader = SentimentIntensityAnalyzer()
    VADER_OK = True
except ImportError:
    VADER_OK = False
    logger.warning("vaderSentiment not installed")

# ─── TextBlob ─────────────────────────────────────────────────────────────────
try:
    from textblob import TextBlob
    TEXTBLOB_OK = True
except ImportError:
    TEXTBLOB_OK = False
    logger.warning("textblob not installed")

# ─── HuggingFace pipeline ─────────────────────────────────────────────────────
_hf_sentiment = None

def _load_hf_sentiment():
    global _hf_sentiment
    if _hf_sentiment is None:
        try:
            from transformers import pipeline
            model = os.getenv("SENTIMENT_MODEL", "cardiffnlp/twitter-roberta-base-sentiment-latest")
            _hf_sentiment = pipeline("sentiment-analysis", model=model, truncation=True, max_length=512)
            logger.info(f"HuggingFace model loaded: {model}")
        except Exception as e:
            logger.warning(f"HuggingFace load failed: {e}")
    return _hf_sentiment


# ─── Core sentiment function ──────────────────────────────────────────────────

def analyse_sentiment(text: str, method: str = "vader") -> Dict[str, Any]:
    """
    Returns:
        label  : positive | negative | neutral
        score  : float  -1 … +1
        details: dict with method-specific breakdown
    """
    text = text.strip()
    if not text:
        return {"label": "neutral", "score": 0.0, "details": {}}

    if method == "vader" and VADER_OK:
        scores = _vader.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return {"label": label, "score": compound, "details": scores}

    if method == "textblob" and TEXTBLOB_OK:
        blob  = TextBlob(text)
        score = blob.sentiment.polarity          # -1 … +1
        subj  = blob.sentiment.subjectivity      # 0 … 1
        if score > 0.1:
            label = "positive"
        elif score < -0.1:
            label = "negative"
        else:
            label = "neutral"
        return {"label": label, "score": round(score, 4),
                "details": {"polarity": score, "subjectivity": subj}}

    if method == "huggingface":
        pipe = _load_hf_sentiment()
        if pipe:
            try:
                result = pipe(text[:512])[0]
                raw_label = result["label"].lower()
                if "pos" in raw_label:
                    label = "positive"
                elif "neg" in raw_label:
                    label = "negative"
                else:
                    label = "neutral"
                # normalise score to -1…+1
                score = result["score"] if label == "positive" else -result["score"] if label == "negative" else 0.0
                return {"label": label, "score": round(score, 4), "details": result}
            except Exception as e:
                logger.error(f"HF sentiment error: {e}")

    # fallback → vader
    return analyse_sentiment(text, method="vader")


def analyse_sentiment_ensemble(text: str) -> Dict[str, Any]:
    """Average across all available engines for higher accuracy."""
    results = {}
    if VADER_OK:
        results["vader"]    = analyse_sentiment(text, "vader")
    if TEXTBLOB_OK:
        results["textblob"] = analyse_sentiment(text, "textblob")

    if not results:
        return {"label": "neutral", "score": 0.0, "details": {}}

    avg_score = sum(r["score"] for r in results.values()) / len(results)
    if avg_score >= 0.05:
        label = "positive"
    elif avg_score <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {"label": label, "score": round(avg_score, 4), "details": results}


# ─── Keyword extraction ───────────────────────────────────────────────────────

def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Simple TF-IDF-style keyword extraction without heavy dependencies."""
    STOP_WORDS = {
        "the","a","an","is","are","was","were","be","been","being",
        "have","has","had","do","does","did","will","would","could",
        "should","may","might","shall","can","need","dare","used",
        "in","on","at","to","for","of","and","or","but","if","by",
        "with","as","this","that","these","those","it","its","we","i",
        "you","he","she","they","them","their","our","us","my","your",
        "his","her","not","no","so","up","out","about","from","into",
        "than","more","also","said","new","one","two","after","before",
    }
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    freq: Dict[str, int] = {}
    for w in words:
        if w not in STOP_WORDS:
            freq[w] = freq.get(w, 0) + 1
    sorted_kw = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_kw[:top_n]]


# ─── LangChain summarisation ──────────────────────────────────────────────────

def summarise_text(text: str, max_length: int = 200) -> str:
    """Summarise using LangChain + HuggingFace pipeline."""
    try:
        from langchain_huggingface import HuggingFacePipeline
        from langchain.chains.summarize import load_summarize_chain
        from langchain.docstore.document import Document
        from transformers import pipeline as hf_pipeline

        model_name = os.getenv("SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
        summarizer = hf_pipeline(
            "summarization", model=model_name,
            max_length=max_length, min_length=40, truncation=True
        )
        llm  = HuggingFacePipeline(pipeline=summarizer)
        chain = load_summarize_chain(llm, chain_type="stuff")
        docs  = [Document(page_content=text[:3000])]
        return chain.run(docs)
    except Exception as e:
        logger.warning(f"LangChain summarise failed ({e}), using extractive fallback")
        # Extractive fallback: first 3 sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return " ".join(sentences[:3])


def generate_market_insights(articles: List[Dict]) -> str:
    """Use LangChain to generate strategic insights from a batch of articles."""
    try:
        from langchain.prompts import PromptTemplate
        from langchain_huggingface import HuggingFacePipeline
        from transformers import pipeline as hf_pipeline

        headlines = "\n".join(
            f"- {a.get('title','')}: {a.get('sentiment','neutral')} sentiment"
            for a in articles[:20]
        )
        template = PromptTemplate(
            input_variables=["headlines"],
            template=(
                "You are a senior market analyst. Based on these news headlines and sentiments:\n"
                "{headlines}\n\n"
                "Provide 3 key strategic insights for businesses in this market:"
            ),
        )
        model_name = "google/flan-t5-base"
        gen = hf_pipeline("text2text-generation", model=model_name,
                          max_new_tokens=300, truncation=True)
        llm    = HuggingFacePipeline(pipeline=gen)
        prompt = template.format(headlines=headlines)
        return llm(prompt)
    except Exception as e:
        logger.warning(f"generate_market_insights failed: {e}")
        pos = sum(1 for a in articles if a.get("sentiment") == "positive")
        neg = sum(1 for a in articles if a.get("sentiment") == "negative")
        total = len(articles) or 1
        pct_pos = round(pos / total * 100)
        return (
            f"📊 Analysis of {total} articles:\n"
            f"• {pct_pos}% positive sentiment — market mood is "
            f"{'optimistic' if pct_pos > 60 else 'cautious' if pct_pos > 40 else 'bearish'}.\n"
            f"• {neg} negative signals detected — monitor for risk factors.\n"
            f"• Recommend: track competitor activity and sentiment trends weekly."
        )
