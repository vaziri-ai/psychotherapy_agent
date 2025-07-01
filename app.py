import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
import urllib.parse
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
def ask_gpt4(prompt, chat_history):
    messages = [{"role": "system", "content": "تو یک دستیار روانشناختی مهربان و فارسی‌زبان هستی. به کاربر کمک می‌کنی احساساتش را بیان کند، اگر لازم باشد پیشنهاد می‌کنی تست روانشناسی بدهد، و پاسخ‌ها را با همدلی می‌پذیری."}]
    for msg in chat_history:
        messages.append(msg)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=messages,
    )
    reply = response.choices[0].message["content"]
    return reply

st.markdown("احساست رو بنویس:")

user_input = st.text_input("")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    gpt_reply = ask_gpt4(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_reply})

    st.markdown(f"🤖 روان‌یار: {gpt_reply}")

    # Simple check to trigger test manually
    if any(word in gpt_reply for word in ["تست اضطراب", "تست روانشناسی", "آیا می‌خواهی تست بدهی؟"]):
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
