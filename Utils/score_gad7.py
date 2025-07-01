def score_gad7(responses):
    """
    پاسخ‌ها باید لیستی از ۷ عدد صحیح بین ۰ تا ۳ باشند، که نشان‌دهندهٔ شدت هر نشانه هستند.
    """
    if len(responses) != 7:
        raise ValueError("تعداد پاسخ‌ها باید دقیقاً ۷ باشد.")
    
    total = sum(responses)
    
    if total >= 15:
        level = "شدید"
        recommendation = "لطفاً در اسرع وقت با روانپزشک یا روانشناس حرفه‌ای مشورت کنید."
    elif total >= 10:
        level = "متوسط"
        recommendation = "توصیه می‌شود با یک روان‌درمانگر صحبت کنید یا از خدمات مشاوره‌ای بهره ببرید."
    elif total >= 5:
        level = "خفیف"
        recommendation = "می‌توانید از تکنیک‌های خودیاری مانند تمرین تنفس، مدیتیشن و مدیریت استرس استفاده کنید."
    else:
        level = "حداقل"
        recommendation = "نیازی به اقدام خاصی نیست، اما مراقبت از سلامت روان همیشه مفید است."
    
    return total, level, recommendation
