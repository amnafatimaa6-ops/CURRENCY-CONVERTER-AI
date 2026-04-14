import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Elite Currency Intelligence", layout="wide")

st.title("🌍 Scholarship Elite Currency Intelligence System V3")

st.markdown("Compare currencies, purchasing power, and global financial strength.")

# ---------------- TAB SYSTEM ----------------
tab1, tab2 = st.tabs(["💱 Converter", "📊 Global Insights"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("💱 Smart Converter + Intelligence")

    query = st.text_input("Enter query (e.g. 100 PKR to USD)")

    if st.button("Analyze"):
        res = model.convert(query)

        if "error" in res:
            st.error(res["error"])
        else:
            col1, col2, col3 = st.columns(3)

            col1.metric("From", f"{res['amount']} {res['from']}")
            col2.metric("To", f"{res['result']} {res['to']}")
            col3.metric("Rate", res["rate"])

            st.markdown("### 🧠 Intelligence Layer")

            for line in res["insight"]:
                st.info(line)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("📊 Currency Strength Comparison")

    df = pd.DataFrame(model.get_strength_data().items(), columns=["Currency", "Strength"])
    df = df.sort_values("Strength")

    fig = px.bar(
        df,
        x="Strength",
        y="Currency",
        orientation="h",
        title="Global Currency Power Index"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🌍 Insight")

    st.info("Higher strength = stronger economy = higher purchasing power")
    st.info("Switzerland, USD, GBP are top-tier global currencies")
