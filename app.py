import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Global FX Intelligence", layout="wide")

st.title("🌍 Global Currency Intelligence Engine")

# ---------------- INPUT ----------------
st.subheader("💱 Smart Converter")

user_input = st.text_input("Enter query (e.g. 100 PKR to euro)")

if st.button("Convert 🚀"):
    try:
        res = model.convert_text(user_input)

        from_country = model.get_currency_country(res["from"])
        to_country = model.get_currency_country(res["to"])

        st.success("Conversion Successful")

        col1, col2, col3 = st.columns(3)

        col1.metric("From", f"{res['amount']} {res['from']}")
        col2.metric("To", f"{res['result']} {res['to']}")
        col3.metric("Rate", res["rate"])

        # 🌍 NEW SECTION: COUNTRY INFO
        st.markdown("### 🌍 Currency Country Mapping")

        st.write(f"**{res['from']} belongs to → {from_country}**")
        st.write(f"**{res['to']} belongs to → {to_country}**")

    except Exception as e:
        st.error(str(e))


# ---------------- CURRENCY LIST ----------------
st.subheader("🌐 Supported Currencies")

st.write(list(set(model.CURRENCY_MAP.values())))


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
