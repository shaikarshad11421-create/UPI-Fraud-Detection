from flask import Flask, render_template, request, session, redirect
import os
import folium

# 🔐 auth system
from auth import auth

# 🗄️ database
from db import init_db, insert_transaction, get_all_transactions

app = Flask(__name__)
app.secret_key = "secret123"

# register auth routes
app.register_blueprint(auth)

# initialize database
init_db()


# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template("index.html")


# ---------------- FRAUD LOGIC ----------------
def predict_fraud(data):
    amount, hour, velocity, new_user, location = data

    score = 0
    reasons = []

    # 💰 amount rule
    if amount > 50000:
        score += 40
        reasons.append("High amount")

    # 🌙 time rule
    if hour < 6 or hour > 22:
        score += 25
        reasons.append("Odd time")

    # ⚡ velocity rule
    if velocity > 5:
        score += 25
        reasons.append("High velocity")

    # 👤 new user rule
    if new_user == 1:
        score += 20
        reasons.append("New user")

    # 📍 location rule
    if location in ["unknown", "", None]:
        score += 10
        reasons.append("Unknown location")

    prediction = 1 if score > 50 else 0

    return prediction, score, reasons


# ---------------- PREDICT ----------------
@app.route('/predict', methods=['GET'])
def predict():

    try:
        amount = float(request.args.get('amount', 0))
        hour = int(request.args.get('hour', 0))
        velocity = float(request.args.get('velocity', 0))
        new_user = int(request.args.get('new_user', 0))
        location = request.args.get('location', 'unknown')

        prediction, score, reasons = predict_fraud(
            [amount, hour, velocity, new_user, location]
        )

        insert_transaction(
            (amount, hour, velocity, new_user, location, prediction, score)
        )

        return render_template(
            "result.html",
            prediction=prediction,
            score=score,
            reasons=reasons,
            location=location
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    rows = get_all_transactions()

    fraud_count = len([r for r in rows if r[6] == 1])
    safe_count = len([r for r in rows if r[6] == 0])

    return render_template(
        "dashboard.html",
        rows=rows,
        fraud_count=fraud_count,
        safe_count=safe_count
    )


# ---------------- HEATMAP (NEW FEATURE 🔥) ----------------
@app.route('/heatmap')
def heatmap():

    if 'user' not in session:
        return redirect('/login')

    rows = get_all_transactions()

    # 🌆 city coordinates
    city_coords = {
        "Hyderabad": [17.3850, 78.4867],
        "Bangalore": [12.9716, 77.5946],
        "Chennai": [13.0827, 80.2707],
        "Mumbai": [19.0760, 72.8777],
        "Delhi": [28.7041, 77.1025],
        "Kolkata": [22.5726, 88.3639]
    }

    fraud_map = {}

    # count fraud per city
    for r in rows:
        location = r[4]   # location column
        prediction = r[6] # fraud

        if prediction == 1:
            fraud_map[location] = fraud_map.get(location, 0) + 1

    # 🗺️ create map (India center)
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

    for city, count in fraud_map.items():
        if city in city_coords:
            lat, lon = city_coords[city]

            folium.Circle(
                location=[lat, lon],
                radius=count * 20000,
                color="red",
                fill=True,
                fill_opacity=0.6,
                popup=f"{city}: {count} frauds"
            ).add_to(m)

    # save map
    m.save("static/map.html")

    return render_template("map.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)