import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Global Currency Intelligence V3.4", layout="wide")

st.title("🌍 Global Currency Intelligence System V3.4")

tab1, tab2 = st.tabs(["💱 Converter", "🌍 Explorer"])

# ---------------- CONVERTER ----------------
with tab1:
    st.subheader("💱 Smart Converter")

    query = st.text_input("Enter query (e.g. 100 PKR to USD)")

    if st.button("Convert"):
        res = model.convert(query)

        if "error" in res:
            st.error(res["error"])
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("From", f"{res['amount']} {res['from']}")
            c2.metric("To", f"{res['result']} {res['to']}")
            c3.metric("Rate", res["rate"])

            st.subheader("🧠 Insights")
            for i in res["insight"]:
                st.info(i)

# ---------------- EXPLORER ----------------
with tab2:
    st.subheader("🌍 World Currency Strength Map")

    df = pd.DataFrame(model.get_country_strength_map().items(), columns=["Country", "Strength"])

    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Strength",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🌍 FLAG CARDS (CLEAN VERSION)
    st.subheader("🌍 Currency Explorer")

    flags = {
        "Pakistan":"🇵🇰","India":"🇮🇳","China":"🇨🇳","Japan":"🇯🇵",
        "United States":"🇺🇸","United Kingdom":"🇬🇧","Eurozone":"🇪🇺",
        "Canada":"🇨🇦","Switzerland":"🇨🇭","Australia":"🇦🇺","Sweden":"🇸🇪",
        "South Korea":"🇰🇷","Singapore":"🇸🇬","Malaysia":"🇲🇾",
        "Saudi Arabia":"🇸🇦","Qatar":"🇶🇦","UAE":"🇦🇪","Turkey":"🇹🇷",
        "Iraq":"🇮🇶","Jordan":"🇯🇴","Hungary":"🇭🇺","Poland":"🇵🇱",
        "Romania":"🇷🇴","Maldives":"🇲🇻","Iran":"🇮🇷"
    }

    cols = st.columns(3)

    for i, (code, info) in enumerate(model.CURRENCY_INFO.items()):
        country = info["country"]
        flag = flags.get(country, "🌍")

        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                padding:14px;
                border-radius:14px;
                background:#0f172a;
                color:white;
                margin-bottom:10px;
            ">
            
            <h3>{flag} {country}</h3>
            <p>💱 {code}</p>
            <p>{info['name']}</p>

            </div>
            """, unsafe_allow_html=True)
