from Conditions import Anxiety

def process_user_input(user_input, step, chat_history):
    """Analyze user input and route to correct condition logic."""
    if step == "start":
        return Anxiety.start_screening(chat_history)
    
    if "اضطراب" in user_input or any(word in user_input for word in ["بی‌قراری", "تپش قلب", "دل‌درد"]):
        return Anxiety.handle_input(user_input, chat_history)

    elif "تمرکز" in user_input or "حواس‌پرتی" in user_input:
        return ADHD.handle_input(user_input, chat_history)

    elif "وسواس" in user_input or "شستن دست" in user_input:
        return OCD.handle_input(user_input, chat_history)

    return None, step
