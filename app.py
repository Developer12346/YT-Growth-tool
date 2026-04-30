import streamlit as st
import random
from pytrends.request import TrendReq

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="🔥 FireGaming Growth Tool",
    page_icon="🔥",
    layout="wide"
)

# ---------------------------
# CUSTOM UI STYLE
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
.stButton>button {
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #1c1f26;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("<h1>🔥 FireGaming Growth Tool</h1>", unsafe_allow_html=True)
st.caption("Create viral YouTube content using data + AI 🚀")

# ---------------------------
# INPUT SECTION
# ---------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

topic = st.text_input("🎮 Enter Topic")
keywords = st.text_input("🔑 Enter Keywords (comma separated)")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FUNCTIONS
# ---------------------------

# 🔥 Trend Finder (Real)
def get_real_trends(topic):
    pytrends = TrendReq(hl='en-IN', tz=330)
    try:
        pytrends.build_payload([topic], timeframe='now 7-d', geo='IN')
        related = pytrends.related_queries()

        trends = []

        if topic in related:
            data = related[topic]

            if data.get('rising') is not None:
                trends += data['rising']['query'].tolist()

            if data.get('top') is not None:
                trends += data['top']['query'].tolist()

        trends = list(dict.fromkeys(trends))
        return trends[:10]

    except:
        return []


# 🎯 Title Generator
def generate_titles(topic, keywords):
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    main_kw = kw_list[0] if kw_list else topic

    power_words = ["Insane", "Crazy", "Unbelievable", "Unexpected", "Wild"]
    emotions = ["😳", "🔥", "💀", "😂"]

    formats = [
        "This {kw} Moment Was {power} {emoji}",
        "You Won’t Believe This {kw} Clip {emoji}",
        "This {kw} Should NOT Happen {emoji}",
        "I Tried {kw} and It Got {power} {emoji}",
        "Most {power} {kw} Moment Ever {emoji}",
        "{power} Things Happened in {kw} {emoji}",
        "This {kw} Edit Went Too Far {emoji}",
        "1 Minute of {power} {kw} Chaos {emoji}"
    ]

    titles = []

    for _ in range(5):
        fmt = random.choice(formats)
        title = fmt.format(
            kw=main_kw,
            power=random.choice(power_words),
            emoji=random.choice(emotions)
        )

        if len(title) < 40:
            title += f" | {topic}"
        elif len(title) > 75:
            title = title[:72] + "..."

        titles.append(title)

    return titles


# 📊 CTR Checker
def calculate_ctr(title):
    score = 50

    if any(word in title.lower() for word in ["insane", "crazy", "unbelievable"]):
        score += 15

    if any(e in title for e in ["😳", "🔥", "💀", "😂"]):
        score += 10

    if 40 <= len(title) <= 70:
        score += 15

    return min(score, 100)


# ---------------------------
# BUTTONS
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    trend_btn = st.button("📈 Find Trends")

with col2:
    title_btn = st.button("🎯 Generate Titles")

with col3:
    ctr_btn = st.button("📊 Check CTR")

# ---------------------------
# OUTPUT SECTIONS
# ---------------------------

# 📈 Trends
if trend_btn and topic:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔥 Trending Ideas")

    trends = get_real_trends(topic)

    if trends:
        for t in trends:
            st.write(f"• {t}")
    else:
        st.warning("No trends found, try broader topic")

    st.markdown('</div>', unsafe_allow_html=True)


# 🎯 Titles
if title_btn and topic and keywords:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 High CTR Titles")

    titles = generate_titles(topic, keywords)

    for t in titles:
        st.write(f"• {t}")

    st.markdown('</div>', unsafe_allow_html=True)


# 📊 CTR
if ctr_btn and topic:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 CTR Score")

    sample_title = topic
    score = calculate_ctr(sample_title)

    st.metric("CTR Score", f"{score}/100")

    if score < 60:
        st.warning("Low CTR — improve title")
    else:
        st.success("Good CTR — ready to post")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("Built by FireGaming982 🚀")