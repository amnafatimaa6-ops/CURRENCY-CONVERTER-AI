import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Global FX Intelligence", layout="wide")

st.title("🌍 Global Currency Intelligence Engine")
st.markdown("Type like: **10 pkr to usd / 50 yen to euro / 100 canada to rupees**")

# ---------------- CONVERTER ----------------
st.subheader("💱 Smart Converter")

user_input = st.text_input("Enter your query")

if st.button("Convert 🚀"):
    try:
        res = model.convert_text(user_input)

        st.success("Conversion Successful")

        col1, col2, col3 = st.columns(3)

        col1.metric("From", f"{res['amount']} {res['from']}")
        col2.metric("To", f"{res['result']} {res['to']}")
        col3.metric("Rate", res["rate"])

        st.markdown("### 🌍 Currency Details")

        full_map = model.get_currency_full_list()

        st.write(full_map.get(res["from"], "Unknown"))
        st.write(full_map.get(res["to"], "Unknown"))

    except Exception as e:
        st.error(str(e))
        st.info("Try: 10 pkr to usd | 50 yen to euro | 100 canada to rupees")


# ---------------- SUPPORTED CURRENCIES ----------------
st.subheader("🌐 Supported Currencies (Full Names)")

currency_map = model.get_currency_full_list()

for code, full in currency_map.items():
    st.write(f"💱 **{code} → {full}**")


# ---------------- EXPENSIVENESS CHART ----------------
st.subheader("📊 Cost of Living Index")

data = model.get_expensiveness_data()

df = pd.DataFrame({
    "Currency": list(data.keys()),
    "Index": list(data.values())
})

df = df.sort_values("Index", ascending=True)

fig = px.bar(
    df,
    x="Index",
    y="Currency",
    orientation="h",
    title="Cheapest → Most Expensive Currencies"
)

st.plotly_chart(fig, use_container_width=True)
