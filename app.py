import streamlit as st

from streamlit_option_menu import option_menu
from prediction_page import show_predict_page
from about_page import show_about_content
from tutorial_page import show_tutorial_page


def main():
    # 2. horizontal menu
    page = option_menu('SUMOnet', [ "Predict", "Tutorial","About"], 
        icons=['gear','bi-book','house'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    if page == "About":
        show_about_content()
        
    elif page == "Predict":
        show_predict_page()

    elif page == "Tutorial":
        show_tutorial_page()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
    


