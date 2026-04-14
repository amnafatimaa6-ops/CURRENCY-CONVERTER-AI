import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Elite FX Dashboard V3.1", layout="wide")

st.title("🌍 Global Currency Intelligence System V3.1")

tab1, tab2 = st.tabs(["💱 Converter", "📊 Global Map"])

# ---------------- CONVERTER ----------------
with tab1:
    st.subheader("💱 Smart Converter")

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

            st.subheader("🧠 Insights")

            for i in res["insight"]:
                st.info(i)

# ---------------- MAP + CARDS ----------------
with tab2:
    st.subheader("🌍 World Currency Strength Map")

    data = model.get_country_strength_map()

    df = pd.DataFrame({
        "Country": list(data.keys()),
        "Strength": list(data.values())
    })

    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Strength",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌍 Country Cards")

    cols = st.columns(4)

    for i, row in df.iterrows():
        with cols[i % 4]:
            st.markdown(f"""
            ### 🌍 {row['Country']}
            💰 Strength: **{row['Strength']}/10**
            """)
