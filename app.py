import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Global Currency Intelligence V3.2", layout="wide")

st.title("🌍 Global Currency Intelligence System V3.2")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💱 Converter", "📊 Global Explorer"])

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

# ---------------- GLOBAL MAP + CARDS + SLIDER ----------------
with tab2:
    st.subheader("🌍 World Currency Map")

    df = pd.DataFrame(model.get_country_strength_map().items(), columns=["Country", "Strength"])

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

    st.subheader("🎚️ Currency Explorer Slider")

    data = model.get_country_currency_slider_data()

    index = st.slider("Select Country", 0, len(data)-1, 0)

    selected = data[index]

    st.success(f"""
🌍 Country: {selected['country']}
💱 Currency: {selected['currency']}
📌 Full Name: {selected['name']}
""")
