import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Currency Engine", layout="wide")

st.title("🌍 Global Currency Intelligence Engine")

st.markdown("Type: **100 PKR to USD / 50 yen to euro / 10 canada to rupees**")

# ---------------- CONVERTER ----------------
st.subheader("💱 Smart Converter")

user_input = st.text_input("Enter your query")

if st.button("Convert"):
    try:
        res = model.convert_text(user_input)

        st.success("Conversion Successful")

        col1, col2, col3 = st.columns(3)

        col1.metric("From", f"{res['amount']} {res['from']}")
        col2.metric("To", f"{res['result']} {res['to']}")
        col3.metric("Rate", res["rate"])

        st.markdown("### 🌍 Currency Details")

        full = model.get_currency_full_list()

        st.write(full.get(res["from"], "Unknown"))
        st.write(full.get(res["to"], "Unknown"))

    except Exception as e:
        st.error(str(e))


# ---------------- FULL LIST ----------------
st.subheader("🌐 Supported Currencies")

for code, info in model.get_currency_full_list().items():
    st.write(f"💱 **{code} → {info}**")


# ---------------- EXPENSIVENESS ----------------
st.subheader("📊 Expensiveness Index (Cheapest → Costliest)")

data = model.get_expensiveness_data()

df = pd.DataFrame({
    "Currency": list(data.keys()),
    "Index": list(data.values())
}).sort_values("Index")

fig = px.bar(
    df,
    x="Index",
    y="Currency",
    orientation="h",
    title="Global Currency Strength Comparison"
)

st.plotly_chart(fig, use_container_width=True)
