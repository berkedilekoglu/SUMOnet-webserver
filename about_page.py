import streamlit as st


def show_about_content():

    about_project_title = '<p style="font-family:monospace; font-size: 2rem;">About Project</p>'
    st.markdown(about_project_title, unsafe_allow_html=True)
    st.markdown("***")
    about_us_title = '<p style="font-family:monospace; font-size: 2rem;">About Us</p>'
    st.markdown(about_us_title, unsafe_allow_html=True)
    