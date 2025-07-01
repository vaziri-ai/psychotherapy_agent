from Conditions import Anxiety, ADHD

def process_user_input(user_input, step, chat_history):
    """Analyze user input and route to correct condition logic."""
    if step == "start":
        return anxiety.start_screening(chat_history)
    
    anxiety_keywords = ["اضطراب", "بی‌قراری", "تپش قلب", "دل‌درد", "لرزش"]
    adhd_keywords = ["تمرکز", "پرتی حواس", "فراموشی", "بی‌نظمی", "بی‌توجهی"]
    ocd_keywords = ["وسواس", "شستن دست", "تکرار", "دقت زیاد"]

    if any(word in user_input for word in anxiety_keywords):
        reply, new_step = anxiety.handle_input(user_input, chat_history)
        return reply, new_step, "gad7"

    elif any(word in user_input for word in adhd_keywords):
        reply, new_step = adhd.handle_input(user_input, chat_history)
        return reply, new_step, "ADHD"

    elif any(word in user_input for word in ocd_keywords):
        reply, new_step = ocd.handle_input(user_input, chat_history)
        return reply, new_step, "OCD"

    # If no match, return None to fallback to GPT
    return None, step, None
