import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="PUP Chatbot", layout="wide")

# 🔹 Load background image
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("background.jpg")

# 🔹 Apply CSS (ChatGPT-style + background)
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.chat-container {{
    max-width: 700px;
    margin: auto;
    background-color: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 12px;
}}

.user-msg {{
    background-color: #0b93f6;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
}}

.bot-msg {{
    background-color: #444654;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: left;
}}

h2 {{
    text-align: center;
    color: white;
}}
</style>
""", unsafe_allow_html=True)

# 🔹 Title
st.markdown("<h2>🎓 PUP CSE Admission Assistant</h2>", unsafe_allow_html=True)

# 🔹 Load dataset
df = pd.read_csv("cutoffs.csv")
df.columns = df.columns.str.strip().str.lower()
df['category'] = df['category'].str.lower()

# 🔹 Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Eligibility logic
def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]

    if row.empty:
        return "❌ Invalid category (general, sc, bc, rural)"

    cutoff = int(row['avg_cutoff'].values[0])

    if rank <= cutoff:
        return f"✅ Eligible (Cutoff ~ {cutoff})"
    else:
        return f"⚠️ Lower chances (Cutoff ~ {cutoff})"

# 🔹 Chat UI
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 🔹 Chat input
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

# 🔹 Bottom section
st.divider()

col1, col2, col3 = st.columns(3)

# 📊 Show Data
with col1:
    if st.button("📊 Show Data"):
        st.dataframe(df, use_container_width=True)

# 🌐 Official Website
with col2:
    st.link_button("🌐 Official Website", "https://www.punjabiuniversity.ac.in/")

# 📄 Brochure Download
with col3:
    try:
        with open("brochure.pdf", "rb") as file:
            st.download_button(
                "📥 Download Brochure",
                file,
                file_name="PUP_CSE_Brochure.pdf"
            )
    except:
        st.write("📄 Brochure not available")
