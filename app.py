import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Elite FX Dashboard V3", layout="wide")

st.title("🌍 Scholarship Elite Currency Intelligence V3")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💱 Converter", "📊 Global Insights"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("💱 Smart Currency Converter")

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

            st.markdown("### 🧠 Insights")

            for line in res["insight"]:
                st.info(line)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("🌍 Global Currency Strength Map")

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
        color_continuous_scale="Viridis",
        title="Global Currency Strength Index"
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
