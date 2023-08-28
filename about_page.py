import os

import streamlit as st




def show_about_content():

    about_project_title = '<p style="font-family:monospace; font-size: 2rem;">Citation</p>'
    
    st.markdown(about_project_title, unsafe_allow_html=True)
    st.markdown('<p style="font-family:monospace; font-size: 1rem;">If you use SUMOnet  in your work, please do cite us:</p>', unsafe_allow_html=True)
    cite = '''
<p style="font-family:monospace; font-size: 1rem;">
    Dilekoglu, B., Tastan, O.: Sumonet: Deep sequential prediction of sumoylation sites. bioRxiv (2023). https://doi.org/10.1101/2023.08.25.554749, <a href="https://www.biorxiv.org/content/early/2023/08/25/2023.08.25.554749" style="color: inherit; text-decoration: inherit;">https://www.biorxiv.org/content/early/2023/08/25/2023.08.25.554749</a>
</p>
'''
    st.markdown(cite, unsafe_allow_html=True)
    st.markdown("***")
    contact = '<p style="font-family:monospace; font-size: 2rem;">Contact</p>'
    st.markdown(contact, unsafe_allow_html=True)
    berke_contact = '<p style="font-family:monospace; font-size: 1rem;"><b>Berke Dilekoglu</b> berkedilekoglu@sabanciuniv.edu</p>'
    st.markdown(berke_contact, unsafe_allow_html=True)
    oznur_contact = '<p style="font-family:monospace; font-size: 1rem;"><b>Oznur Tastan</b> otastan@sabanciuniv.edu</p>'
    st.markdown(oznur_contact, unsafe_allow_html=True)
    
