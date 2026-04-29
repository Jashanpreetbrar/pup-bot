import streamlit as st
import pandas as pd

st.set_page_config(page_title="PUP CSE Chatbot")

st.title("🎓 PUP CSE Admission Assistant")

df = pd.read_csv("cutoffs.csv")

df['category'] = df['category'].str.lower()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def check_eligibility(rank, category):
    row = df[df['category'] == category.lower()]

    if row.empty:
        return "❌ No Such Category Found."

    if 'avg_cutoff' in df.columns:
        cutoff = int(row['avg_cutoff'].values[0])
    else:
        cutoff = int(row.iloc[0, -1])

    if rank <= cutoff:
        return f"✅ Eligible for Admissions (Cutoff ~ {cutoff})"
    else:
        return f"⚠️ Lower chances of Admissions (Cutoff ~ {cutoff})"

user_input = st.chat_input("Enter: rank category (e.g., 0000 Category)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        parts = user_input.split()
        rank = int(parts[0])
        category = parts[1]

        reply = check_eligibility(rank, category)

    except:
        reply = "❌ Invalid Format (Format should be: 0000 Category)"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.divider()
if st.button("🔗 For More Info"):
    st.markdown(
        "<a href='https://www.punjabiuniversity.ac.in/' target='_blank'>Click here to visit official website</a>",
        unsafe_allow_html=True
    )
if st.button("📊 Previous 3 Year Data"):
    st.subheader("📊 Complete Dataset")
    st.dataframe(df)
