def score_gad7(responses):
    total = sum(responses)
    if total >= 10:
        level = "شدید"
        recommendation = "سطح اضطراب شما بالاست. توصیه می‌شود با روانپزشک صحبت کنید."
    elif total >= 6:
        level = "متوسط"
        recommendation = "مقداری اضطراب دارید. مشاوره با روان‌درمانگر می‌تواند مفید باشد."
    else:
        level = "خفیف"
        recommendation = "سطح اضطراب پایین است. مراقبت‌های خودیاری پیشنهاد می‌شود."
    return total, level, recommendation


def score_adhd(responses):
    total = sum(responses)
    if total >= 9:
        level = "شدید"
        recommendation = "نشانه‌های قابل توجهی از ADHD وجود دارد. لطفاً با روانپزشک مشورت کنید."
    elif total >= 6:
        level = "متوسط"
        recommendation = "ممکن است نشانه‌هایی از ADHD وجود داشته باشد. توصیه می‌شود با روان‌درمانگر صحبت کنید."
    else:
        level = "خفیف"
        recommendation = "علائم ADHD در سطح خفیف هستند یا قابل‌توجه نیستند."
    return total, level, recommendation
