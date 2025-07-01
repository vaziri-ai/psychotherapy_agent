from Conditions import Anxiety, ADHD, OCD

def process_user_input(user_input, step, chat_history):
    if step == "start":
        reply, new_step = Anxiety.start_screening(chat_history)
        return reply, new_step, None  # always 3 values

    anxiety_keywords = ["اضطراب", "بی‌قراری", "تپش قلب", "دل‌درد", "لرزش"]
    adhd_keywords = ["تمرکز", "پرتی حواس", "فراموشی", "بی‌نظمی", "بی‌توجهی"]
    ocd_keywords = ["وسواس", "شستن دست", "تکرار", "دقت زیاد"]

    if any(word in user_input for word in anxiety_keywords):
        reply, new_step = Anxiety.handle_input(user_input, chat_history)
        return reply, new_step, "gad7"

    elif any(word in user_input for word in adhd_keywords):
        reply, new_step = ADHD.handle_input(user_input, chat_history)
        return reply, new_step, "adhd"

    elif any(word in user_input for word in ocd_keywords):
        reply, new_step = OCD.handle_input(user_input, chat_history)
        return reply, new_step, "ocd"

    # fallback to GPT
    return None, step, None
