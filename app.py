# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import json
from process_input import process_user_input

# --- Setup ---
st.set_page_config(page_title="اپلیکیشن هوش مصنوعی روانشناسی دکتر موذنی", layout="centered")
st.title("🧠 اپلیکیشن هوش مصنوعی روانشناسی دکتر موذنی")

# --- OpenAI client ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "تو یک دستیار روان‌شناسی فارسی‌زبان هستی. در پاسخ‌هایت مهربان باش، از مثال ساده استفاده کن و بیش از ۵ جمله یا ۲ پاراگراف ننویس مگر اینکه ازت خواسته بشه."}
    ]
if "step" not in st.session_state:
    st.session_state.step = "start"
if "just_sent" not in st.session_state:
    st.session_state.just_sent = False
if "test_type" not in st.session_state:
    st.session_state.test_type = None

# --- Show Chat History (Skip system) ---
for msg in st.session_state.chat_history[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# --- Input Field ---
user_input = st.chat_input("پیامت رو اینجا بنویس...")

# --- Process Input ---
if user_input and not st.session_state.just_sent:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    reply, new_step, new_test_type = process_user_input(user_input, st.session_state.step, st.session_state.chat_history)

    # Fallback to GPT if no specific reply
    if reply is None:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.chat_history
        )
        reply = response.choices[0].message.content

    st.chat_message("assistant").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Update step and test_type if provided
    if new_step:
        st.session_state.step = new_step
    if new_test_type:
        st.session_state.test_type = new_test_type

    st.session_state.just_sent = True
    st.rerun()

# --- Reset just_sent flag on rerun ---
if st.session_state.just_sent:
    st.session_state.just_sent = False

# --- Render condition-specific tests ---
if st.session_state.step == "test_active":
    if st.session_state.test_type == "gad7":
        from conditions.anxiety import run_test as run_gad7_test
        run_gad7_test()
    elif st.session_state.test_type == "adhd":
        from conditions.adhd import run_test as run_adhd_test
        run_adhd_test()
    elif st.session_state.test_type == "ocd":
        from conditions.ocd import run_test as run_ocd_test
        run_ocd_test()
