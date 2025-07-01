import streamlit as st
from openai import OpenAI
import json
from Utils.score_gad7 import score_gad7

# Load Persian GAD-7 test
with open("Tests/gad7.json", "r", encoding="utf-8") as f:
    gad7 = json.load(f)

# --- Setup OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="اپلیکیشن هوش مصنوعی روانشناسی دکتر موذنی", layout="centered")
st.title("اپلیکیشن هوش مصنوعی روانشناسی دکتر موذنی")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "step" not in st.session_state:
    st.session_state.step = "start"
if "symptom_check_done" not in st.session_state:
    st.session_state.symptom_check_done = False

# Function to ask GPT-4 with custom system prompt
SYSTEM_PROMPT = (
    "تو یک دستیار روان‌شناسی فارسی‌زبان هستی که مکالمه را به شکل مرحله‌ای هدایت می‌کنی. "
    "در ابتدا از احساس کلی کاربر بپرس، سپس با سؤالات هدفمند علائم را بررسی کن، "
    "در صورت تشخیص نشانه‌های اضطراب یا ADHD، تست مناسب را پیشنهاد بده. "
    "در هر مرحله فقط یک سؤال بپرس. سعی کن فقط در حد ۵ جمله یا ۲ پاراگراف پاسخ بدهی، مگر اینکه کاربر صریحاً درخواست توضیح بیشتر کند."
)

def ask_gpt(prompt, chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in chat_history:
        messages.append(msg)
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
    )
    return response.choices[0].message.content

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f" تو: {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"هوش مصنوعی روانشناسی: {msg['content']}")

# Divider
st.markdown("---")

# Input box
user_input = st.text_input("شکاستت رو بنویس، امروز چه حالی داری؟", key="chat_input")

if st.session_state.get("step") != "test_active":
# Step-based interaction
    if user_input and "just_sent" not in st.session_state:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
    
        if st.session_state.step == "start":
            reply = ask_gpt("کاربر احساس خود را بیان کرده. حالا درباره علائمش سؤال کن.", st.session_state.chat_history)
            st.session_state.step = "symptom_check"
    
        elif st.session_state.step == "symptom_check":
            if any(word in user_input for word in ["دل‌درد", "لرزش", "بی‌قراری", "تپش قلب"]):
                reply = "ممکنه نشونه‌هایی از اضطراب باشه. دوست داری یک تست علمی کوتاه انجام بدیم؟"
                st.session_state.step = "test_offer"
            else:
                reply = ask_gpt("از کاربر درباره علائمش بیشتر بپرس.", st.session_state.chat_history)
    
        elif st.session_state.step == "test_offer":
            if any(word in user_input for word in ["بله", "باشه", "اوکی"]):
                st.session_state.step = "test_active"
                reply = "بسیار خب، تست اضطراب GAD-7 را شروع می‌کنیم."
            else:
                reply = "باشه. اگر نظرت عوض شد، می‌تونی هر زمان بگی تا تست رو انجام بدیم."
    
        else:
            reply = ask_gpt(user_input, st.session_state.chat_history)
    
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.last_gpt_reply = reply
        st.session_state.just_sent = True
        st.rerun()

# Reset flag
if "just_sent" in st.session_state:
    del st.session_state["just_sent"]

# Show test if active
if st.session_state.get("step") == "test_active":
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

        st.session_state.step = "post_test"
