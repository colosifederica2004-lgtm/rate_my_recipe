import streamlit as st


st.set_page_config(
    page_title="Rate My Recipe",
    page_icon="🍲",
    layout="wide",
)

st.title("Rate My Recipe")

st.write(
    "Explore recipe ratings and discover how different ranking "
    "methods can affect which recipes appear at the top."
)

st.info(
    "The application is under development. "
    "Data analysis and recipe rankings will be added later."
)