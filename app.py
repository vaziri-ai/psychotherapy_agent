import streamlit as st
from openai import OpenAI
import json

# Load Persian GAD-7 test
with open("Tests/gad7.json", "r", encoding="utf-8") as f:
    gad7 = json.load(f)

# --- Setup OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="روان‌یار با GPT-4", layout="centered")
st.title("🧠 روان‌یار - همراه روانی شما با GPT-4")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to ask GPT-4 a question
def ask_gpt(prompt, chat_history):
    messages = [{"role": "system", "content": "تو یک دستیار روانشناختی مهربان و فارسی‌زبان هستی. سعی کن فقط در حد ۵ جمله یا ۲ پاراگراف پاسخ بدهی، مگر اینکه کاربر صریحاً درخواست توضیح بیشتر کند."}]
    for msg in chat_history:
        messages.append(msg)
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
    )
    return response.choices[0].message.content

# Show chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"👤 تو: {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 روان‌یار: {msg['content']}")

# Divider
st.markdown("---")

# Input box at bottom
user_input = st.text_input("✍️ پیامت رو بنویس:", key="chat_input")

# Only trigger once per message
if user_input and "just_sent" not in st.session_state:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    gpt_reply = ask_gpt(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_reply})

    # Save GPT reply to session for later use
    st.session_state.last_gpt_reply = gpt_reply
    st.session_state.just_sent = True
    st.rerun()


# Reset the just_sent flag after rerun
if "just_sent" in st.session_state:
    del st.session_state["just_sent"]

# ✅ NEW: Check GPT reply for test suggestion
if "last_gpt_reply" in st.session_state:
    if any(word in st.session_state.last_gpt_reply for word in ["تست اضطراب", "تست روانشناسی", "آیا می‌خواهی تست بدهی؟"]):
        st.markdown("### تست اضطراب GAD-7")

        responses = []
        with st.form("test_form"):
            for idx, q in enumerate(gad7["questions"]):
                answer = st.selectbox(q, list(gad7["options"].values()), key=f"q{idx}")
                responses.append(
                    int([k for k, v in gad7["options"].items() if v == answer][0])
                )
            submitted = st.form_submit_button("ثبت پاسخ‌ها")

        if submitted:
            total, level, recommendation = score_gad7(responses)
            st.success(f"نمرهٔ کلی شما: {total} از ۲۱")
            st.info(f"سطح اضطراب: {level}")
            st.warning(recommendation)
