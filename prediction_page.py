import streamlit as st

from loguru import logger
from uniprot_id_prediction_page import show_uniprot_id_content
from protein_sequence_prediction_page import show_protein_sequence_page_content
from fasta_file_prediction_page import show_fasta_file_page_content


def display_page_content(page):

    if page == 'Uniprot Id':

        try:

            show_uniprot_id_content()

        except Exception as e:

            logger.error("Error occurred while showing uniprot id page: {error_message}", error_message=str(e))


    elif page == 'Protein Sequence':

        try:

            show_protein_sequence_page_content()

        except Exception as e:

            logger.error("Error occurred while showing protein sequence page: {error_message}", error_message=str(e))

    elif page == 'Upload Fasta File':

        try:

            show_fasta_file_page_content()

        except Exception as e:

            logger.error("Error occurred while showing fasta file page: {error_message}", error_message=str(e))

def show_predict_page():
         
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Predict With:", ['Uniprot Id', 'Protein Sequence', 'Upload Fasta File'])
    display_page_content(selected_page)
