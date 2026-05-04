import streamlit as st
import requests

# ---------------- SAFE IMPORT ----------------
try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except Exception:
    PYTRENDS_AVAILABLE = False

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="YT Growth Tool", layout="wide")

st.title("FireGaming982 YouTube Growth Tool")

# ---------------- UI ----------------
topic = st.text_input("Enter Topic (e.g. Roblox, BGMI)")
keywords = st.text_input("Keywords (comma separated)")
user_title = st.text_input("Test Your Title (CTR Checker)")

# ---------------- AI FUNCTION ----------------
def ai_generate(prompt):
    try:
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"

        response = requests.post(
            api_url,
            json={"inputs": prompt},
            timeout=12
        )

        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text")

        return None

    except Exception:
        return None

# ---------------- TRENDS ----------------
def get_trends(topic):
    if PYTRENDS_AVAILABLE:
        try:
            pytrends = TrendReq(hl="en-IN", tz=330)
            pytrends.build_payload([topic], timeframe="now 7-d", geo="IN")
            data = pytrends.related_queries()

            trends = []

            if topic in data:
                if data[topic]["rising"] is not None:
                    trends += data[topic]["rising"]["query"].tolist()

                if data[topic]["top"] is not None:
                    trends += data[topic]["top"]["query"].tolist()

            if trends:
                return trends[:10]

        except Exception:
            pass

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
        titles = ai_output.split("\n")
        titles = [title.strip("-• 1234567890. ") for title in titles if title.strip()]

        if titles:
            return titles[:5]

    return [
        f"{topic} but Everything Went WRONG",
        f"I Tried {topic} and It was INSANE",
        f"Only 1% Can Do This in {topic}",
        f"{topic} Moments You Can't Believe",
        f"This {topic} Trick is BROKEN",
    ]

# ---------------- CTR ----------------
def calculate_ctr(title):
    score = 40
    lower_title = title.lower()

    if any(word in lower_title for word in ["insane", "crazy", "broken", "secret", "shocking"]):
        score += 20

    if any(word in lower_title for word in ["you", "this", "i", "only"]):
        score += 10

    if any(char in title for char in ["!", "?", "🔥", "😳", "💀", "🤯"]):
        score += 10

    if 35 <= len(title) <= 75:
        score += 20

    return min(score, 100)

# ---------------- BUTTONS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    trend_btn = st.button("Trends")

with col2:
    title_btn = st.button("Titles")

with col3:
    ctr_btn = st.button("CTR")

# ---------------- OUTPUT ----------------
if trend_btn:
    if topic:
        st.subheader("Trending Ideas")
        for trend in get_trends(topic):
            st.write("•", trend)
    else:
        st.warning("Please enter a topic first.")

if title_btn:
    if topic:
        st.subheader("Viral Titles")
        for title in generate_titles(topic, keywords):
            st.write("•", title)
    else:
        st.warning("Please enter a topic first.")

if ctr_btn:
    if user_title:
        st.subheader("CTR Score")
        score = calculate_ctr(user_title)

        st.metric("CTR Score", f"{score}/100")

        if score < 60:
            st.error("Low CTR - weak title")
        elif score < 80:
            st.warning("Decent CTR - improve hook")
        else:
            st.success("High CTR - strong title")
    else:
        st.warning("Please enter a title to check.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built by FireGaming982")
