# app.py

import streamlit as st
from model import convert_text

st.set_page_config(
    page_title="Global Currency AI",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Global Currency Intelligence Engine")
st.write("Type naturally like: **45 PKR to lira**, **100 yen in rupees**, **50 dollars to euro**")

user_input = st.text_input("Enter your query:")

if st.button("Convert 🚀"):
    try:
        result = convert_text(user_input)

        st.success("Conversion Complete")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("From", result["input"])
        with col2:
            st.metric("To", result["output"])

        st.divider()

        st.write("📊 Exchange Path")
        st.code(result["path"])

        st.write("📉 Rate Used")
        st.code(result["rate"])

    except Exception as e:
        st.error(f"System Error: {str(e)}")
        st.info("Try: '45 PKR to lira' or '100 yen to dollars'")
