import streamlit as st
import pandas as pd
import plotly.express as px
from model import convert_text, get_expensiveness_data

st.set_page_config(page_title="Global FX Intelligence", layout="wide")

st.title("🌍 Global Currency Intelligence Dashboard")

# ---------------- LEFT: CONVERTER ----------------
st.subheader("💱 Smart Converter")

user_input = st.text_input("Enter query (e.g. 100 PKR to euro)")

if st.button("Convert"):
    try:
        res = convert_text(user_input)

        st.success("Conversion Complete")

        col1, col2, col3 = st.columns(3)

        col1.metric("From", f"{res['amount']} {res['from']}")
        col2.metric("To", f"{res['result']} {res['to']}")
        col3.metric("Rate", res["rate"])

    except Exception as e:
        st.error(str(e))


# ---------------- RIGHT: CURRENCY LIST ----------------
st.subheader("🌐 Available Currencies")

currencies = [
    "PKR 🇵🇰", "INR 🇮🇳", "CNY 🇨🇳", "JPY 🇯🇵",
    "USD 🇺🇸", "GBP 🇬🇧", "EUR 🇪🇺",
    "CAD 🇨🇦", "CHF 🇨🇭",
    "SAR 🇸🇦", "QAR 🇶🇦",
    "TRY 🇹🇷", "PLN 🇵🇱",
    "HUF 🇭🇺", "RON 🇷🇴",
    "MVR 🇲🇻", "IRR 🇮🇷"
]

st.write(currencies)


# ---------------- CHART ----------------
st.subheader("📊 Currency Expensiveness Index")

data = get_expensiveness_data()

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
