import streamlit as st
import pandas as pd
import plotly.express as px
import model

st.set_page_config(page_title="Global Currency Intelligence V3.5", layout="wide")

st.title("🌍 Global Currency Intelligence System V3.5")

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

            for i in res["insight"]:
                st.info(i)

# ---------------- EXPLORER ----------------
with tab2:
    st.subheader("🌍 World Currency Map")

    df = pd.DataFrame(model.get_country_strength_map().items(), columns=["Country", "Strength"])

    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Strength"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🌍 FLAG CARDS (IMAGE BASED)
    st.subheader("🌍 Currency Explorer")

    country_codes = {
        "Pakistan":"pk","Japan":"jp","United States":"us","United Kingdom":"gb",
        "China":"cn","India":"in","Germany":"de","France":"fr","Italy":"it",
        "Canada":"ca","Switzerland":"ch","Australia":"au","Sweden":"se",
        "South Korea":"kr","Singapore":"sg","Malaysia":"my","Saudi Arabia":"sa",
        "Qatar":"qa","UAE":"ae","Turkey":"tr","Iraq":"iq","Jordan":"jo",
        "Hungary":"hu","Poland":"pl","Romania":"ro","Maldives":"mv","Iran":"ir"
    }

    cols = st.columns(3)

    for i, (code, info) in enumerate(model.CURRENCY_INFO.items()):
        country = info["country"]
        cc = country_codes.get(country, "us")

        with cols[i % 3]:
            st.markdown(f"""
            <div style="padding:14px;border-radius:14px;background:#0f172a;color:white;margin-bottom:10px;">
            
            <img src="https://flagcdn.com/w80/{cc}.png" width="40"><br>
            <b>{country}</b><br>
            💱 {code}<br>
            {info['name']}

            </div>
            """, unsafe_allow_html=True)
