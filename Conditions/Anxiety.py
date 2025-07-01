from Utils.score_gad7 import score_gad7
import json

with open("Tests/gad7.json", "r", encoding="utf-8") as f:
    gad7 = json.load(f)

def start_screening(chat_history):
    return "حالت چطوره؟ می‌خوای درباره احساست صحبت کنی؟", "symptom_check"

def handle_input(user_input, chat_history):
    if any(word in user_input for word in ["تست", "بله", "حتما", "اره","آره", "باشه","اوکی"]):
        return "بسیار خوب، تست اضطراب را شروع می‌کنیم.", "test_active"
    return "به نظر می‌رسه اضطرابی وجود داره. تمایل داری یک تست کوتاه بدیم؟", "test_offer"
