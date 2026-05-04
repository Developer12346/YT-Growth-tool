import streamlit as st
import random
import requests

# ---------------- SAFE IMPORT ----------------
try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except:
    PYTRENDS_AVAILABLE = False

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🔥 YT Growth Tool", layout="wide")

st.title("🔥 FireGaming982 YouTube Growth Tool")

# ---------------- UI ----------------
topic = st.text_input("🎮 Enter Topic (e.g. Roblox, BGMI)")
keywords = st.text_input("🔑 Keywords (comma separated)")
user_title = st.text_input("📝 Test Your Title (CTR Checker)")

# ---------------- AI FUNCTION (FREE + SAFE) ----------------
def ai_generate(prompt):
    try:
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

        response = requests.post(
            API_URL,
            json={"inputs": prompt},
            timeout=12
        )

        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", None)

        return None

    except:
        return None

# ---------------- TRENDS ----------------
def get_trends(topic):
    if PYTRENDS_AVAILABLE:
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

            if len(trends) > 0:
                return trends[:10]
        except:
            pass

    # fallback
    return [
        f"{topic} gameplay",
        f"{topic} funny moments",
        f"{topic} update",
        f"{topic} secrets",
        f"{topic} vs pro",
        f"{topic} challenge",
        f"{topic} highlights",
    ]

# ---------------- TITLES ----------------
def generate_titles(topic, keywords):
    prompt = f"Generate 5 viral YouTube gaming titles for topic: {topic} with keywords: {keywords}"

    ai_output = ai_generate(prompt)

    if ai_output:
        return ai_output.split("\n")

    # fallback
    kw = keywords.split(",")[0] if keywords else topic

    return [
        f"{topic} but Everything Went WRONG 😳",
        f"I Tried {topic} and It was INSANE 🔥",
        f"Only 1% Can Do This in {topic} 🤯",
        f"{topic} Moments You Can’t Believe 💀",
        f"This {topic} Trick is BROKEN 😳"
    ]

# ---------------- CTR ----------------
def calculate_ctr(title):
    score = 40

    if any(w in title.lower() for w in ["insane", "crazy", "broken"]):
        score += 20

    if any(e in title for e in ["😳", "🔥", "💀", "🤯"]):
        score += 10

    if 45 <= len(title) <= 70:
        score += 20

    if any(w in title.lower() for w in ["you", "this", "i"]):
        score += 10

    return min(score, 100)

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
    st.subheader("🔥 Trending Ideas")
    for t in get_trends(topic):
        st.write("•", t)

if title_btn and topic:
    st.subheader("🎯 Viral Titles")
    for t in generate_titles(topic, keywords):
        st.write("•", t)

if ctr_btn and user_title:
    st.subheader("📊 CTR Score")
    score = calculate_ctr(user_title)

    st.metric("CTR Score", f"{score}/100")

    if score < 60:
        st.error("Low CTR — weak title")
    elif score < 80:
        st.warning("Decent CTR — improve hook")
    else:
        st.success("High CTR — strong title")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🔥 Built by FireGaming982")
```
