from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("cutoffs.csv")

def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]
    if row.empty:
        return "Invalid category"

    cutoff = int(row['avg_cutoff'].values[0])

    if rank <= cutoff:
        return f"Eligible for CSE. Avg cutoff: {cutoff}"
    else:
        return f"Lower chance. Avg cutoff: {cutoff}"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body").lower()
    resp = MessagingResponse()

    try:
        rank, category = incoming_msg.split()
        rank = int(rank)

        result = check_eligibility(rank, category)
        resp.message(result)

    except:
        resp.message("Send message like:\n720000 general")

    return str(resp)

if __name__ == "__main__":
    app.run()
