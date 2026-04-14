import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Global FX Intelligence", layout="wide")

st.title("🌍 Global Currency Intelligence Engine")
st.write("Type like: **100 PKR to euro / 50 dollars to yen / 200 canada to rupees**")

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

    except Exception as e:
        st.error(str(e))


# ---------------- AVAILABLE CURRENCIES ----------------
st.subheader("🌐 Supported Currencies")

st.write(model.get_currency_list())


# ---------------- EXPENSIVENESS CHART ----------------
st.subheader("📊 Country Expensiveness Index")

data = model.get_expensiveness_data()

df = pd.DataFrame({
    "Currency": list(data.keys()),
    "Expensiveness": list(data.values())
})

fig = px.bar(
    df,
    x="Currency",
    y="Expensiveness",
    title="Which currencies represent higher cost of living power"
)

st.plotly_chart(fig, use_container_width=True)
