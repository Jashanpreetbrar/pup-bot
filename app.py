import streamlit as st
import pandas as pd

st.set_page_config(page_title="PUP CSE Chatbot")

st.title("🎓 PUP CSE Admission Assistant")

# Load dataset (your uploaded CSV)
df = pd.read_csv("Previous Year ranks - Sheet1.csv")

# Normalize category column (important)
df['category'] = df['category'].str.lower()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 🎯 Eligibility logic using avg or latest year
def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]

    if row.empty:
        return "❌ Invalid category"

    # Try avg_cutoff if exists, else use latest year
    if 'avg_cutoff' in df.columns:
        cutoff = int(row['avg_cutoff'].values[0])
    else:
        # fallback: use last column (latest year)
        cutoff = int(row.iloc[0, -1])

    if rank <= cutoff:
        return f"✅ Eligible (Cutoff ~ {cutoff})"
    else:
        return f"⚠️ Lower chances (Cutoff ~ {cutoff})"

# 💬 Chat input
user_input = st.chat_input("Enter: rank category (e.g., 720000 general)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        parts = user_input.split()
        rank = int(parts[0])
        category = parts[1]

        reply = check_eligibility(rank, category)

    except:
        reply = "❌ Format: 720000 general"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# 📊 BUTTON: Show full dataset
st.divider()
if st.button("📊 Show All Previous Year Data"):
    st.subheader("📊 Complete Dataset")
    st.dataframe(df)
