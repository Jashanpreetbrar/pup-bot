from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("cutoffs.csv")

# ✅ Home route (for browser testing)
@app.route("/")
def home():
    return "PUP WhatsApp Bot is Running ✅"

# 🎯 Eligibility logic
def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]

    if row.empty:
        return "❌ Invalid category. Use: general, sc, bc, rural"

    cutoff = int(row['avg_cutoff'].values[0])

    if rank <= cutoff:
        return f"✅ Eligible for CSE (Cutoff ~ {cutoff})"
    else:
        return f"⚠️ Lower chances (Cutoff ~ {cutoff})"

# 📱 WhatsApp webhook
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()

    try:
        parts = incoming_msg.split()
        rank = int(parts[0])
        category = parts[1]

        result = check_eligibility(rank, category)
        resp.message(result)

    except:
        resp.message(
            "🎓 PUP CSE Bot\n\n"
            "Send message like:\n"
            "720000 general\n\n"
            "Categories: general, sc, bc, rural"
        )

    return str(resp)

# 🚀 Run app
if __name__ == "__main__":
    app.run()
