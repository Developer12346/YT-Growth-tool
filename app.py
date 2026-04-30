import streamlit as st
import random

# SAFE IMPORT (prevents crash)
try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except:
    PYTRENDS_AVAILABLE = False

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="🔥 YT Growth Tool", layout="wide")

st.markdown("""
<style>
body {background-color: #0e1117;}
.card {
    padding:20px;
    border-radius:15px;
    background:#1c1f26;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 YouTube Growth Tool")

# ---------------- INPUT ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

topic = st.text_input("🎮 Enter Topic")
keywords = st.text_input("🔑 Keywords (comma separated)")
user_title = st.text_input("📝 Enter Your Title (for CTR check)")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def get_trends(topic):
    if not PYTRENDS_AVAILABLE:
        return [
            f"{topic} funny moments",
            f"{topic} viral clips",
            f"{topic} insane gameplay",
            f"{topic} trending now 🔥"
        ]
    try:
        pytrends = TrendReq(hl='en-IN', tz=330)
        pytrends.build_payload([topic], timeframe='now 7-d', geo='IN')
        data = pytrends.related_queries()
        trends = []

        if topic in data:
            if data[topic]['rising'] is not None:
                trends += data[topic]['rising']['query'].tolist()
            if data[topic]['top'] is not None:
                trends += data[topic]['top']['query'].tolist()

        return trends[:10]
    except:
        return ["Trend fetch failed"]

def generate_titles(topic, keywords):
    kw = keywords.split(",")[0] if keywords else topic

    formats = [
        "This {kw} Moment Was INSANE 😳",
        "You Won’t Believe This {kw} 🔥",
        "Most CRAZY {kw} Ever 💀",
        "This {kw} Should NOT Happen 😳",
        "1 Minute of {kw} Chaos 😂"
    ]

    return [f.format(kw=kw) for f in formats]

def calculate_ctr(title):
    score = 50

    if any(w in title.lower() for w in ["insane","crazy"]):
        score += 20
    if any(e in title for e in ["😳","🔥","💀","😂"]):
        score += 15
    if 40 <= len(title) <= 70:
        score += 15

    return min(score,100)

# ---------------- BUTTONS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    trend_btn = st.button("📈 Trends")

with col2:
    title_btn = st.button("🎯 Titles")

with col3:
    ctr_btn = st.button("📊 CTR")

# ---------------- OUTPUT ----------------

if trend_btn and topic:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔥 Trending Ideas")
    for t in get_trends(topic):
        st.write("•", t)
    st.markdown('</div>', unsafe_allow_html=True)

if title_btn and topic:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Title Ideas")

    titles = generate_titles(topic, keywords)

    for t in titles:
        st.write("•", t)

    st.markdown('</div>', unsafe_allow_html=True)

if ctr_btn and user_title:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 CTR Score")

    score = calculate_ctr(user_title)

    st.metric("CTR Score", f"{score}/100")

    if score < 60:
        st.error("Low CTR — improve title")
    elif score < 80:
        st.warning("Decent CTR — can improve")
    else:
        st.success("High CTR — good to go")

    st.mast.markdown("""
st.markdown("---")

st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px; padding-top: 10px;'>
    Made by <b>FireGaming982</b>
</div>
""", unsafe_allow_html=True)
