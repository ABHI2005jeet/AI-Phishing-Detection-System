def hybrid_score(ml, rule, url):

    final = (ml * 0.6) + (rule * 0.25) + (url * 0.15)

    if final < 35:
        category = "Safe"
    elif final < 65:
        category = "Suspicious"
    else:
        category = "Phishing"

    return round(min(final, 100), 2), category