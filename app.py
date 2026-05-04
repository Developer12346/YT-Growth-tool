import random
import streamlit as st

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except Exception:
    PYTRENDS_AVAILABLE = False

st.set_page_config(page_title="YT Growth Tool", layout="wide")

st.title("FireGaming982 YouTube Growth Tool")

topic = st.text_input("Enter Topic (e.g. Roblox, BGMI)")
keywords = st.text_input("Keywords (comma separated)")
user_title = st.text_input("Test Your Title (CTR Checker)")


def get_keyword_list(keywords):
    return [keyword.strip() for keyword in keywords.split(",") if keyword.strip()]


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
        f"{topic} latest update",
        f"{topic} old map",
        f"{topic} new event",
        f"{topic} hidden secrets",
        f"{topic} best moments",
        f"{topic} challenge ideas",
        f"{topic} nostalgia",
    ]


def generate_titles(topic, keywords):
    keyword_list = get_keyword_list(keywords)
    main_keyword = keyword_list[0] if keyword_list else topic

    title_patterns = [
        f"Revisiting {topic}: Does It Still Feel the Same?",
        f"{topic} Then vs Now: What Actually Changed?",
        f"I Played {main_keyword} Like the Old Days Again",
        f"The Forgotten Side of {topic} Nobody Talks About",
        f"Why {topic} Hits Different Now",
        f"Can {topic} Still Give Us That Old Feeling?",
        f"I Went Back to {topic} After Years",
        f"{topic} Nostalgia Is Stronger Than I Expected",
        f"The Part of {topic} Everyone Forgot",
        f"What Made Old {topic} So Special?",
        f"I Tried to Recreate My Old {topic} Memories",
        f"{topic} Feels Different Now... But Why?",
        f"The Most Nostalgic Things in {topic}",
        f"I Found Something in {topic} That Took Me Back",
        f"Old {topic} Players Will Remember This",
    ]

    random.shuffle(title_patterns)
    return title_patterns[:5]


def calculate_ctr(title):
    score = 40
    lower_title = title.lower()

    strong_words = [
        "forgotten", "hidden", "secret", "nostalgia", "old",
        "new", "why", "changed", "special", "remember",
        "different", "rare", "best", "update",
    ]

    if any(word in lower_title for word in strong_words):
        score += 20

    if any(word in lower_title for word in ["you", "i", "why", "how", "can", "what"]):
        score += 10

    if any(char in title for char in ["!", "?", "🔥", "🎮", "😳", "🤯"]):
        score += 10

    if 35 <= len(title) <= 75:
        score += 20

    return min(score, 100)


col1, col2, col3 = st.columns(3)

with col1:
    trend_btn = st.button("Trends")

with col2:
    title_btn = st.button("Titles")

with col3:
    ctr_btn = st.button("CTR")


if trend_btn:
    if topic:
        st.subheader("Trending Ideas")
        for trend in get_trends(topic):
            st.write("•", trend)
    else:
        st.warning("Please enter a topic first.")


if title_btn:
    if topic:
        st.subheader("Title Ideas")
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


st.markdown("---")
st.markdown("🔥 Built by FireGaming982 🎮")
st.markdown("Update 1.1- Bug Fixes with Titles And Trends Apps")
