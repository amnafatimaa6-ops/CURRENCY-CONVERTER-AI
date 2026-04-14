import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Scholarship FX Dashboard", layout="wide")

st.title("🌍 Global Currency Intelligence Dashboard")
st.markdown("Scholarship Premium V2 — Finance + Data + Intelligence")

# ---------------- INPUT ----------------
st.subheader("💱 Currency Converter")

query = st.text_input("Enter query (e.g. 100 PKR to USD)")

if st.button("Analyze"):
    res = model.convert(query)

    if "error" in res:
        st.error(res["error"])
        st.info("Try: 100 pkr to usd | 50 yen to euro | 10 canada to rupees")
    else:
        st.success("Analysis Complete")

        col1, col2, col3 = st.columns(3)

        col1.metric("From", f"{res['amount']} {res['from']}")
        col2.metric("To", f"{res['result']} {res['to']}")
        col3.metric("Rate", res["rate"])

        st.subheader("🧠 Intelligence Layer")

        for i in res["insight"]:
            st.info(i)

# ---------------- CURRENCY STRENGTH ----------------
st.subheader("📊 Currency Strength Index")

df = pd.DataFrame(model.get_strength_data().items(), columns=["Currency", "Strength"])
df = df.sort_values("Strength")

fig = px.bar(df, x="Strength", y="Currency", orientation="h",
             title="Global Currency Strength Comparison")

st.plotly_chart(fig, use_container_width=True)
