def predict_fraud(amount, location, time_hour):
    # SIMPLE RULE-BASED MODEL (you can replace with ML later)

    if amount > 50000:
        return "🚨 FRAUD DETECTED (High Amount)"
    
    if location == "foreign":
        return "🚨 FRAUD DETECTED (Foreign Location)"

    if time_hour < 6 or time_hour > 22:
        return "⚠ Suspicious Transaction (Odd Time)"

    return "✅ Safe Transaction"