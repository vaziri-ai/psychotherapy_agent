# -*- coding: utf-8 -*-
import streamlit as st
import json
from Utils.score_ADHD import score_adhd  # Your ADHD scoring function

# Load ADHD test questions from JSON file
with open("Tests/ADHD.json", "r", encoding="utf-8") as f:
    adhd_test = json.load(f)

def handle_input(user_input, chat_history):
    """
    Handle user input in ADHD screening flow.
    Return: reply text, next step
    """
    # If user agrees to take the test
    if any(word in user_input for word in ["تست", "بله", "اوکی", "باشه", "آره"]):
        return "بسیار خوب، تست غربالگری ADHD را شروع می‌کنیم.", "test_active"
    # If user says no or anything else, ask again or provide fallback
    else:
        return "اگر تمایل داشتی، هر زمان بگو تا تست رو شروع کنیم.", "test_offer"

def run_test():
    """
    Render the ADHD screening test form, collect responses, score and show results.
    """
    st.markdown("### تست غربالگری ADHD")
    responses = []

    with st.form("adhd_test_form"):
        for idx, question in enumerate(adhd_test["questions"]):
            answer = st.selectbox(
                question,
                options=list(adhd_test["options"].values()),
                key=f"adhd_q{idx}"
            )
            # Convert selected answer back to integer key for scoring
            responses.append(
                int([k for k, v in adhd_test["options"].items() if v == answer][0])
            )
        submitted = st.form_submit_button("ثبت پاسخ‌ها")

    if submitted:
        total, level, recommendation = score_adhd(responses)
        st.success(f"نمره کلی شما: {total}")
        st.info(f"سطح علائم: {level}")
        st.warning(recommendation)

        st.session_state.step = "post_test"
