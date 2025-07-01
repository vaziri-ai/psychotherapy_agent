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
