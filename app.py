import streamlit as st
import random

st.title("🔥 YouTube Growth Tool")

title = st.text_input("Enter Video Title")
topic = st.text_input("Enter Topic")
keywords = st.text_input("Enter Keywords (comma separated)")


def generate_description(title, topic, keywords):
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    hashtags = " ".join([f"#{k.replace(' ', '')}" for k in kw_list])

    intros = [
        "Okay so this one got kinda crazy 💀",
        "Not gonna lie… I didn’t expect THIS to happen 😂",
        "Bro this went completely out of control 😭",
        "I was just chilling and then this happened 💀",
        f"This might be one of my weirdest {topic} moments 😂"
    ]

    middles = [
        f"I was playing around with {topic} and somehow ended up with these moments.",
        "This started normal but quickly turned into chaos 💀",
        "Some of these clips actually surprised me ngl.",
        "I didn’t plan this at all… it just happened 😂",
        "Things escalated way faster than expected."
    ]

    endings = [
        "If you enjoyed, drop a like and maybe subscribe 🙌",
        "Like + subscribe if you want more of this 🔥",
        "Support the channel if you liked this one ❤️",
        "Let me know if I should make more like this 👇",
        "Comment what I should try next!"
    ]

    return f"""
{title}

{random.choice(intros)}

{random.choice(middles)}

Watch till the end, it actually gets better 😳

{random.choice(endings)}

keywords (ignore lol):
{", ".join(kw_list)}

{hashtags}
"""


if st.button("Generate 🚀"):
    if title and topic and keywords:
        st.subheader("📄 Description")
        st.code(generate_description(title, topic, keywords))
    else:
        st.warning("Fill all fields")

# ---------------------------
# ---------------------------
# PRO TITLE GENERATOR
# ---------------------------
import random

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

        # Ensure length ~40–70 chars
        if len(title) < 40:
            title += f" | {topic}"
        elif len(title) > 75:
            title = title[:72] + "..."

        titles.append(title)

    return titles


# BUTTON
if st.button("Generate Titles 🔥"):
    if topic and keywords:
        st.subheader("🎯 High CTR Titles")

        titles = generate_titles(topic, keywords)

        for t in titles:
            st.write(f"• {t}")

    else:
        st.warning("Enter topic + keywords")
# ---------------------------
# CTR ANALYZER
# ---------------------------
def analyze_ctr(title, keywords):
    score = 0
    feedback = []

    # Length check
    if 40 <= len(title) <= 70:
        score += 30
    else:
        feedback.append("Title length not optimal (40-70 recommended)")

    # Power words
    power_words = ["crazy", "insane", "shocking", "unexpected", "wtf"]
    if any(word.lower() in title.lower() for word in power_words):
        score += 20
    else:
        feedback.append("Try adding power words (crazy, insane, etc.)")

    # Emotion
    if any(e in title for e in ["😳", "🔥", "💀", "😂"]):
        score += 20
    else:
        feedback.append("Add emotion (emoji or expressive words)")

    # Keywords
    if keywords.split(",")[0].strip().lower() in title.lower():
        score += 30
    else:
        feedback.append("Main keyword missing in title")

    return score, feedback


st.subheader("📊 CTR Score Checker")

if st.button("Check CTR 🚀"):
    if title and keywords:
        score, feedback = analyze_ctr(title, keywords)

        st.write(f"### 🎯 CTR Score: {score}/100")

        if score > 75:
            st.success("🔥 High click potential!")
        elif score > 50:
            st.warning("👍 Decent, can improve")
        else:
            st.error("⚠️ Low CTR, needs improvement")

        if feedback:
            st.write("### सुधार (Improvements):")
            for f in feedback:
                st.write(f"• {f}")
    else:
        st.warning("Enter title + keywords")

from pytrends.request import TrendReq

# ---------------------------
# REAL TREND FINDER (GOOGLE TRENDS)
# ---------------------------
def get_real_trends(topic):
    pytrends = TrendReq(hl='en-IN', tz=330)

    # Build query
    pytrends.build_payload([topic], timeframe='now 7-d', geo='IN')

    # Get related queries
    related = pytrends.related_queries()

    trends = []

    if topic in related:
        if related[topic]['rising'] is not None:
            trends += related[topic]['rising']['query'].tolist()

        if related[topic]['top'] is not None:
            trends += related[topic]['top']['query'].tolist()

    return trends[:10]  # top 10 trends


# BUTTON
if st.button("Find REAL Trends 🔥"):
    if topic:
        st.subheader("📈 Real Trending Searches")

        try:
            trends = get_real_trends(topic)

            if trends:
                for t in trends:
                    st.write(f"• {t}")
            else:
                st.warning("No trends found, try another topic")

        except Exception as e:
            st.error("Error fetching trends (check internet)")
    else:
        st.warning("Enter topic first")