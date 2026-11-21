"""Streamlit entry point: page configuration and sidebar navigation."""

import streamlit as st

st.set_page_config(
    page_title="Rate My Recipe",
    page_icon="🍽️",
    layout="wide",
)

pages = [
    st.Page("home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/1_Explore.py", title="Explore", icon="🔎"),
    st.Page("pages/2_Rankings.py", title="Rankings", icon="🏆"),
    st.Page("pages/3_Analysis.py", title="Analysis", icon="📊"),
    st.Page(
        "pages/4_Recipe_characteristics.py",
        title="Recipe Characteristics",
        icon="🥕"
    ),
]

navigation = st.navigation(pages)
navigation.run()
