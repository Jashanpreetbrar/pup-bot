import streamlit as st
import pandas as pd

st.set_page_config(page_title="PUP Chatbot", layout="wide")

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

st.markdown("<h2 style='text-align:center;'>🎓 Punjabi University, Patiala CSE Admission Assistant</h2>", unsafe_allow_html=True)

df = pd.read_csv("cutoffs.csv")
df['category'] = df['category'].str.lower()

if "messages" not in st.session_state:
    st.session_state.messages = []

def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]
    if row.empty:
        return "❌ Invalid category"

    cutoff = int(row['avg_cutoff'].values[0])

    if rank <= cutoff:
        return f"✅ Eligible for admission (Cutoff ~ {cutoff})"
    else:
        return f"⚠️ Lower chances of admission (Cutoff ~ {cutoff})"

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input("Whats your JEE rank and Category (Format: 0000 Category)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        rank, category = user_input.split()
        rank = int(rank)
        reply = check_eligibility(rank, category)
    except:
        reply = "❌Wrong Format: (Only 0000 Category is acceptable)"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Show Data"):
        st.dataframe(df, use_container_width=True)

with col2:
    st.link_button("🌐 Official Site", "https://www.punjabiuniversity.ac.in/")

with col3:
    try:
        with open("brochure.pdf", "rb") as file:
            st.download_button("📄 Brochure", file, file_name="PUP_CSE.pdf")
    except:
        st.write("📄 Brochure not available")
