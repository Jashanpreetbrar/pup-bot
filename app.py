import streamlit as st
import pandas as pd

st.set_page_config(page_title="PUP Chatbot", layout="wide")

# 🌙 Custom CSS for ChatGPT-like UI
st.markdown("""
<style>
body {
    background-color: #343541;
    color: white;
}

.chat-container {
    max-width: 700px;
    margin: auto;
}

.user-msg {
    background-color: #0b93f6;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
}

.bot-msg {
    background-color: #444654;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: left;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 style='text-align:center;'>🎓 PUP CSE Admission Assistant</h2>", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("cutoffs.csv")
df['category'] = df['category'].str.lower()

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎯 Eligibility logic
def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]
    if row.empty:
        return "❌ Invalid category"

    cutoff = int(row['avg_cutoff'].values[0])

    if rank <= cutoff:
        return f"✅ Eligible (Cutoff ~ {cutoff})"
    else:
        return f"⚠️ Lower chances (Cutoff ~ {cutoff})"

# Chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Chat input (bottom)
user_input = st.chat_input("Type: 720000 general")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        rank, category = user_input.split()
        rank = int(rank)
        reply = check_eligibility(rank, category)
    except:
        reply = "❌ Format: 720000 general"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# 📊 + 🌐 + 📄 Section
st.divider()

col1, col2, col3 = st.columns(3)

# Show data
with col1:
    if st.button("📊 Show Data"):
        st.dataframe(df, use_container_width=True)

# Official website
with col2:
    st.link_button("🌐 Official Site", "https://www.punjabiuniversity.ac.in/")

# Brochure
with col3:
    try:
        with open("brochure.pdf", "rb") as file:
            st.download_button("📄 Brochure", file, file_name="PUP_CSE.pdf")
    except:
        st.write("📄 Brochure not available")
