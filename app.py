import streamlit as st
from streamlit_option_menu import option_menu

from prediction_page import show_predict_page

st.set_page_config(layout="wide")
# 2. horizontal menu
page = option_menu('SUMOnet', ["About", "Predictions"], 
    icons=['house', 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
if page == "About":
    st.title("ABOUT US")
    
elif page == "Predictions":
    show_predict_page()
    


