"""
Real-Time Market Research & Competitive Intelligence Platform
Streamlit Frontend Dashboard
"""
import os
import sys
import time
import json
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Market Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:5000/api")

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-dark:    #0a0e1a;
        --bg-card:    #111827;
        --bg-hover:   #1a2235;
        --accent:     #6366f1;
        --accent2:    #22d3ee;
        --positive:   #10b981;
        --negative:   #ef4444;
        --neutral:    #f59e0b;
        --text:       #e2e8f0;
        --muted:      #64748b;
        --border:     #1e293b;
    }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
        background-color: var(--bg-dark) !important;
        color: var(--text) !important;
    }

    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
        border-left: 4px solid var(--accent);
        transition: all 0.2s ease;
    }
    .metric-card:hover { background: var(--bg-hover); }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent2);
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-label {
        font-size: 0.8rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .article-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .article-title  { font-weight: 600; font-size: 0.95rem; color: var(--text); }
    .article-meta   { font-size: 0.78rem; color: var(--muted); margin-top: 4px; }

    .badge-positive { background: rgba(16,185,129,.15); color: var(--positive); border-radius:6px; padding:3px 10px; font-size:.75rem; font-weight:600; }
    .badge-negative { background: rgba(239,68,68,.15);  color: var(--negative); border-radius:6px; padding:3px 10px; font-size:.75rem; font-weight:600; }
    .badge-neutral  { background: rgba(245,158,11,.15); color: var(--neutral);  border-radius:6px; padding:3px 10px; font-size:.75rem; font-weight:600; }

    .insight-box {
        background: linear-gradient(135deg, rgba(99,102,241,.1), rgba(34,211,238,.05));
        border: 1px solid rgba(99,102,241,.3);
        border-radius: 12px;
        padding: 20px 24px;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    div[data-testid="stSidebar"] {
        background: #080c18 !important;
        border-right: 1px solid var(--border);
    }

    .stButton > button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    h1, h2, h3 { color: var(--text) !important; }

    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--accent2);
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border);
    }
    .stTextInput > div > input, .stSelectbox > div, .stTextArea textarea {
        background: var(--bg-card) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── API helpers ──────────────────────────────────────────────────────────────

def api_get(path: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error ({path}): {e}")
        return None


def api_post(path: str, body: dict):
    try:
        r = requests.post(f"{API_BASE}{path}", json=body, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error ({path}): {e}")
        return None


# ─── Sidebar Navigation ───────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <div style='font-size:1.6rem; font-weight:700; color:#6366f1;'>📡 MarketIQ</div>
        <div style='font-size:0.75rem; color:#64748b; margin-top:4px;'>Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "News Feed", "Sentiment Analyser", "Competitor Intel", "Market Trends", "AI Insights"],
        icons=["grid-3x3-gap", "newspaper", "emoji-smile", "bullseye", "graph-up-arrow", "lightning-charge"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container":         {"padding": "0 8px", "background-color": "transparent"},
            "icon":              {"color": "#6366f1", "font-size": "14px"},
            "nav-link":          {"font-size": "13px", "color": "#94a3b8", "padding": "10px 16px"},
            "nav-link-selected": {"background-color": "rgba(99,102,241,.15)", "color": "#e2e8f0", "font-weight": "600"},
        },
    )

    st.markdown("---")
    st.markdown("<div style='font-size:.7rem; color:#475569; padding:0 8px;'>API Status</div>", unsafe_allow_html=True)
    health = api_get("/health")
    if health and health.get("status") == "ok":
        st.success("API Online ✓")
        mongo_ok = health.get("mongodb", False)
        st.markdown(f"<div style='font-size:.72rem; color:#{'10b981' if mongo_ok else 'ef4444'}; padding:0 8px;'>MongoDB: {'Connected' if mongo_ok else 'Offline (using mock)'}</div>", unsafe_allow_html=True)
    else:
        st.error("API Offline ✗")
        st.caption("Start: `python backend/app.py`")


# ─── Pages ────────────────────────────────────────────────────────────────────

def sentiment_badge(s: str) -> str:
    return f"<span class='badge-{s}'>{s.upper()}</span>"


# ════════════════════════════════════════════
# 1. DASHBOARD
# ════════════════════════════════════════════
if selected == "Dashboard":
    st.markdown("## 📊 Market Intelligence Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y  %H:%M:%S')}")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    articles_data = api_get("/news/articles", {"limit": 100})
    articles      = articles_data["articles"] if articles_data else []
    n_articles    = len(articles)
    n_pos         = sum(1 for a in articles if a.get("sentiment") == "positive")
    n_neg         = sum(1 for a in articles if a.get("sentiment") == "negative")
    n_neu         = n_articles - n_pos - n_neg

    with c1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-label'>Total Articles</div>
            <div class='metric-value'>{n_articles}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card' style='border-left-color:#10b981;'>
            <div class='metric-label'>Positive Signals</div>
            <div class='metric-value' style='color:#10b981;'>{n_pos}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card' style='border-left-color:#ef4444;'>
            <div class='metric-label'>Negative Signals</div>
            <div class='metric-value' style='color:#ef4444;'>{n_neg}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        pct_pos = round(n_pos / n_articles * 100) if n_articles else 0
        st.markdown(f"""<div class='metric-card' style='border-left-color:#22d3ee;'>
            <div class='metric-label'>Positive Rate</div>
            <div class='metric-value' style='color:#22d3ee;'>{pct_pos}%</div>
        </div>""", unsafe_allow_html=True)

    # Charts row
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Positive", "Negative", "Neutral"],
            values=[n_pos, n_neg, n_neu],
            hole=.55,
            marker_colors=["#10b981", "#ef4444", "#f59e0b"],
        )])
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=10, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-header'>Articles by Source</div>", unsafe_allow_html=True)
        if articles:
            df_src = pd.DataFrame(articles)
            src_counts = df_src["source"].value_counts().head(8).reset_index()
            src_counts.columns = ["source", "count"]
            fig_bar = px.bar(
                src_counts, x="count", y="source", orientation="h",
                color="count", color_continuous_scale=["#1e293b", "#6366f1"],
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", coloraxis_showscale=False,
                xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                margin=dict(t=10, b=10, l=10, r=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # Recent articles
    st.markdown("<div class='section-header'>Recent Articles</div>", unsafe_allow_html=True)
    for a in articles[:6]:
        badge = sentiment_badge(a.get("sentiment", "neutral"))
        kws   = ", ".join(a.get("keywords", [])[:4])
        st.markdown(f"""<div class='article-card'>
            <div class='article-title'>{a.get('title','—')}</div>
            <div class='article-meta'>
                {badge}&nbsp;&nbsp;
                <b>{a.get('source','')}</b> · {a.get('published_at','')[:10]}
                &nbsp;|&nbsp; 🏷 {kws}
            </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 2. NEWS FEED
# ════════════════════════════════════════════
elif selected == "News Feed":
    st.markdown("## 📰 News Feed & Sentiment")

    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
    with col1: query = st.text_input("Search query", value="artificial intelligence market")
    with col2: source = st.selectbox("Source", ["newsapi", "rss", "mock"])
    with col3: limit  = st.slider("Limit", 5, 50, 15)
    with col4: method = st.selectbox("NLP Engine", ["ensemble", "vader", "textblob"])

    if st.button("🔍 Fetch & Analyse"):
        with st.spinner("Fetching and analysing articles…"):
            result = api_post("/news/fetch", {
                "query": query, "source": source,
                "limit": limit, "sentiment_method": method,
            })
        if result:
            st.success(f"✓ {result['count']} articles fetched and enriched")
            articles = result["articles"]

            # Sentiment breakdown bar
            df = pd.DataFrame(articles)
            sent_counts = df["sentiment"].value_counts().reset_index()
            sent_counts.columns = ["sentiment", "count"]
            color_map = {"positive": "#10b981", "negative": "#ef4444", "neutral": "#f59e0b"}
            fig = px.bar(sent_counts, x="sentiment", y="count",
                         color="sentiment", color_discrete_map=color_map)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", showlegend=False,
                xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
                margin=dict(t=10, b=10, l=10, r=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Article cards
            for a in articles:
                badge   = sentiment_badge(a.get("sentiment", "neutral"))
                score   = a.get("sentiment_score", 0)
                kws     = ", ".join(a.get("keywords", [])[:5])
                content = a.get("content", "")[:200]
                st.markdown(f"""<div class='article-card'>
                    <div class='article-title'><a href="{a.get('url','#')}" target="_blank" style='color:#e2e8f0;text-decoration:none;'>{a.get('title','—')}</a></div>
                    <div style='margin:6px 0; font-size:.88rem; color:#94a3b8;'>{content}…</div>
                    <div class='article-meta'>
                        {badge}&nbsp; Score: <b style='font-family:monospace;'>{score:+.3f}</b>
                        &nbsp;·&nbsp; <b>{a.get('source','')}</b>
                        &nbsp;·&nbsp; {a.get('published_at','')[:10]}
                        &nbsp;|&nbsp; 🏷 {kws}
                    </div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 3. SENTIMENT ANALYSER
# ════════════════════════════════════════════
elif selected == "Sentiment Analyser":
    st.markdown("## 🎭 Sentiment Analyser")

    text   = st.text_area("Enter text to analyse:", height=160,
                           placeholder="Paste a news headline, tweet, review, or any text…")
    method = st.selectbox("Analysis engine", ["ensemble", "vader", "textblob", "huggingface"])

    if st.button("Analyse Sentiment") and text:
        with st.spinner("Analysing…"):
            result = api_post("/sentiment/analyse", {"text": text, "method": method})

        if result:
            label = result.get("label", "neutral")
            score = result.get("score", 0)
            kws   = result.get("keywords", [])

            colour = {"positive": "#10b981", "negative": "#ef4444", "neutral": "#f59e0b"}[label]
            icon   = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}[label]

            st.markdown(f"""<div style='background:rgba(99,102,241,.08); border:1px solid rgba(99,102,241,.25);
                border-radius:12px; padding:24px 28px; margin:12px 0;'>
                <div style='font-size:2.4rem; font-weight:700; color:{colour};'>{icon} {label.upper()}</div>
                <div style='font-family:monospace; font-size:1.1rem; margin-top:8px; color:#94a3b8;'>
                    Score: <span style='color:{colour};'>{score:+.4f}</span>
                </div>
            </div>""", unsafe_allow_html=True)

            # Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [-1, 1], "tickcolor": "#64748b"},
                    "bar":  {"color": colour},
                    "steps": [
                        {"range": [-1, -0.05], "color": "rgba(239,68,68,.2)"},
                        {"range": [-0.05, 0.05], "color": "rgba(245,158,11,.2)"},
                        {"range": [0.05, 1],  "color": "rgba(16,185,129,.2)"},
                    ],
                },
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
                margin=dict(t=20, b=20, l=40, r=40), height=220,
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            if kws:
                st.markdown("<div class='section-header'>Extracted Keywords</div>", unsafe_allow_html=True)
                kw_html = " ".join(
                    f"<span style='background:rgba(99,102,241,.15); border:1px solid rgba(99,102,241,.3); "
                    f"border-radius:6px; padding:4px 10px; margin:3px; display:inline-block; "
                    f"font-size:.82rem; color:#a5b4fc;'>{kw}</span>"
                    for kw in kws
                )
                st.markdown(kw_html, unsafe_allow_html=True)

            details = result.get("details", {})
            if details:
                with st.expander("📋 Detailed Engine Output"):
                    st.json(details)


# ════════════════════════════════════════════
# 4. COMPETITOR INTELLIGENCE
# ════════════════════════════════════════════
elif selected == "Competitor Intel":
    st.markdown("## 🎯 Competitive Intelligence")

    data        = api_get("/competitors")
    competitors = data["competitors"] if data else []

    if competitors:
        df = pd.DataFrame(competitors)

        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("<div class='section-header'>Market Share</div>", unsafe_allow_html=True)
            if "market_share" in df.columns:
                fig_mkt = px.pie(df, values="market_share", names="name", hole=.4,
                                 color_discrete_sequence=px.colors.sequential.Plasma_r)
                fig_mkt.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
                    margin=dict(t=10, b=10, l=10, r=10), showlegend=True,
                )
                st.plotly_chart(fig_mkt, use_container_width=True)

        with col_b:
            st.markdown("<div class='section-header'>Employee Count vs Market Share</div>", unsafe_allow_html=True)
            if "employees" in df.columns and "market_share" in df.columns:
                fig_sc = px.scatter(df, x="employees", y="market_share", text="name", size="market_share",
                                    color="market_share", color_continuous_scale="Plasma")
                fig_sc.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0", coloraxis_showscale=False,
                    xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
                    margin=dict(t=10, b=10, l=10, r=10),
                )
                st.plotly_chart(fig_sc, use_container_width=True)

        # Competitor table
        st.markdown("<div class='section-header'>Competitor Directory</div>", unsafe_allow_html=True)
        display_cols = [c for c in ["name", "industry", "market_share", "employees", "founded"] if c in df.columns]
        st.dataframe(
            df[display_cols].style.background_gradient(subset=["market_share"] if "market_share" in display_cols else [], cmap="Blues"),
            use_container_width=True, hide_index=True,
        )

        # Individual news monitoring
        st.markdown("<div class='section-header'>Monitor Competitor News</div>", unsafe_allow_html=True)
        names = [c.get("name", "") for c in competitors]
        chosen = st.selectbox("Select competitor", names)
        if st.button(f"📡 Fetch news for {chosen}"):
            with st.spinner(f"Fetching news for {chosen}…"):
                news_data = api_get(f"/competitors/{chosen}/news")
            if news_data:
                for a in news_data.get("articles", []):
                    badge = sentiment_badge(a.get("sentiment", "neutral"))
                    st.markdown(f"""<div class='article-card'>
                        <div class='article-title'>{a.get('title','—')}</div>
                        <div class='article-meta'>{badge} · {a.get('source','')} · {a.get('published_at','')[:10]}</div>
                    </div>""", unsafe_allow_html=True)

    # Add competitor form
    with st.expander("➕ Add New Competitor"):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("Company name")
            new_industry = st.text_input("Industry")
        with c2:
            new_website = st.text_input("Website URL")
            new_mkt = st.number_input("Market share %", 0.0, 100.0, 5.0)
        if st.button("Save Competitor") and new_name:
            res = api_post("/competitors/add", {
                "name": new_name, "industry": new_industry,
                "website": new_website, "market_share": new_mkt,
            })
            if res:
                st.success(f"✓ {new_name} saved!")
                st.rerun()


# ════════════════════════════════════════════
# 5. MARKET TRENDS
# ════════════════════════════════════════════
elif selected == "Market Trends":
    st.markdown("## 📈 Market Trend Analysis")

    trends_data = api_get("/trends")
    articles_data = api_get("/news/articles", {"limit": 100})
    articles = articles_data["articles"] if articles_data else []

    if trends_data:
        trends = trends_data.get("trends", [])
        df_trends = pd.DataFrame(trends)

        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.markdown("<div class='section-header'>Top Keywords / Trends</div>", unsafe_allow_html=True)
            if not df_trends.empty:
                fig_trend = px.bar(
                    df_trends.head(15), x="frequency", y="keyword", orientation="h",
                    color="frequency", color_continuous_scale=["#1e2d4d", "#6366f1", "#22d3ee"],
                )
                fig_trend.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0", coloraxis_showscale=False,
                    xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                    margin=dict(t=10, b=10, l=10, r=10), height=420,
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        with col2:
            st.markdown("<div class='section-header'>Sentiment Over Time</div>", unsafe_allow_html=True)
            if articles:
                df_a = pd.DataFrame(articles)
                df_a["date"] = pd.to_datetime(df_a["published_at"], errors="coerce").dt.date
                df_a_grp = df_a.groupby(["date","sentiment"]).size().reset_index(name="count")
                if not df_a_grp.empty:
                    fig_time = px.area(
                        df_a_grp, x="date", y="count", color="sentiment",
                        color_discrete_map={"positive": "#10b981", "negative": "#ef4444", "neutral": "#f59e0b"},
                    )
                    fig_time.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#e2e8f0", showlegend=True,
                        xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
                        margin=dict(t=10, b=10, l=10, r=10), height=420,
                    )
                    st.plotly_chart(fig_time, use_container_width=True)

        # Sentiment score distribution
        if articles:
            st.markdown("<div class='section-header'>Sentiment Score Distribution</div>", unsafe_allow_html=True)
            df_a = pd.DataFrame(articles)
            if "sentiment_score" in df_a.columns:
                fig_hist = px.histogram(
                    df_a, x="sentiment_score", nbins=30, color_discrete_sequence=["#6366f1"],
                )
                fig_hist.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
                    margin=dict(t=10, b=10, l=10, r=10),
                )
                st.plotly_chart(fig_hist, use_container_width=True)


# ════════════════════════════════════════════
# 6. AI INSIGHTS
# ════════════════════════════════════════════
elif selected == "AI Insights":
    st.markdown("## ⚡ AI-Generated Market Insights")

    if st.button("🤖 Generate Strategic Insights", use_container_width=True):
        with st.spinner("AI is analysing market signals…"):
            result = api_get("/insights")
        if result:
            insights = result.get("insights", "No insights generated.")
            based_on = result.get("based_on", 0)
            st.markdown(f"<div class='insight-box'>{insights.replace(chr(10),'<br>')}</div>",
                        unsafe_allow_html=True)
            st.caption(f"Generated from {based_on} articles  ·  {datetime.now().strftime('%H:%M:%S')}")

    st.markdown("---")
    st.markdown("### 📝 Summarise Custom Text")
    custom_text = st.text_area("Paste an article or report:", height=200,
                               placeholder="Paste any market-related text here for AI summarisation…")
    if st.button("Summarise") and custom_text:
        with st.spinner("Summarising…"):
            res = api_post("/summarise", {"text": custom_text})
        if res:
            st.markdown(f"<div class='insight-box'>{res.get('summary','')}</div>",
                        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Sentiment Stats Overview")
    stats = api_get("/sentiment/stats")
    if stats:
        breakdown = stats.get("breakdown", [])
        if breakdown:
            df_stats = pd.DataFrame(breakdown).rename(columns={"_id": "sentiment"})
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(df_stats, x="sentiment", y="count",
                             color="sentiment",
                             color_discrete_map={"positive":"#10b981","negative":"#ef4444","neutral":"#f59e0b"})
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color="#e2e8f0", showlegend=False,
                                  margin=dict(t=10,b=10,l=10,r=10))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.dataframe(df_stats, use_container_width=True, hide_index=True)
