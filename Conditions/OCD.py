# -*- coding: utf-8 -*-
import streamlit as st

# For this minimal example, no external test JSON or scoring function included.
# You can expand with JSON and scoring logic later.

def handle_input(user_input, chat_history):
    """
    Handle user input during OCD screening flow.
    Returns a tuple: (reply message, next step).
    """
    # Simple keyword to start test
    if any(word in user_input for word in ["تست", "بله", "اوکی", "باشه", "آره"]):
        return "خوب است، تست اختلال وسواس فکری-عملی را شروع می‌کنیم.", "test_active"
    
    # If user is hesitant or no clear answer
    return "آیا تمایل داری تست وسواس را انجام دهی؟", "test_offer"

def run_test():
    """
    Render a minimal OCD test form.
    For demonstration, use a few sample questions hardcoded here.
    """
    st.markdown("### تست اختلال وسواس فکری-عملی (OCD)")
    responses = []

    with st.form("ocd_test_form"):
        questions = [
            "چند وقت یک‌بار فکرهای مزاحم و تکراری داری؟",
            "چند وقت یک‌بار احساس می‌کنی باید کارها را چند بار چک کنی؟",
            "چند وقت یک‌بار مجبور می‌شوی کارهای خاصی را بارها انجام دهی؟"
        ]
        options = {
            "0": "اصلاً",
            "1": "گاهی اوقات",
            "2": "اغلب",
            "3": "تقریباً همیشه"
        }

        for idx, question in enumerate(questions):
            answer = st.selectbox(question, options.values(), key=f"ocd_q{idx}")
            # Map answer text back to key for scoring
            responses.append(int([k for k, v in options.items() if v == answer][0]))

        submitted = st.form_submit_button("ثبت پاسخ‌ها")

    if submitted:
        total = sum(responses)

        if total >= 7:
            level = "شدید"
            recommendation = "لطفاً با یک روانپزشک متخصص مشورت کنید."
        elif total >= 4:
            level = "متوسط"
            recommendation = "ممکن است وسواس وجود داشته باشد، توصیه می‌شود مشاوره بگیرید."
        else:
            level = "کم"
            recommendation = "نشانه‌های کمی از وسواس مشاهده شده است."

        st.success(f"نمره کل: {total}")
        st.info(f"سطح وسواس: {level}")
        st.warning(recommendation)

        st.session_state.step = "post_test"
