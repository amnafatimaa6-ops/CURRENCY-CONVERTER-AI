import streamlit as st
import model

st.set_page_config(page_title="AI Finance Assistant", layout="centered")

st.title("💬 AI Global Finance Assistant")
st.write("Ask anything like: *Is 1000 PKR good in Europe? / 50 dollars to yen / 200 canada to rupees*")

query = st.text_input("Talk to AI 💬")

if st.button("Ask"):
    res = model.ai_engine(query)

    if res["type"] == "error":
        st.error(res["message"])
    else:
        st.success("AI Response")

        st.markdown("### 💱 Result")
        st.write(f"{res['amount']} {res['from']} → {res['result']} {res['to']}")

        st.markdown("### 🧠 AI Explanation")

        for line in res["explanation"]:
            st.info(line)
