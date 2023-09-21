import streamlit as st
import time
import pandas as pd

from sumonet.model.architecture import SUMOnet
from sumonet.utils.data_pipe import Data
from sumonet.utils.encodings import Encoding
from utils.prediction_utils import prediction_outputs
from loguru import logger
sequences = None

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def load_models():

    my_model = SUMOnet()
    my_model.load_weights()
    return my_model

def make_prediction(protein_ids, protein_seqs, k_positions):
    encoder = Encoding()
    X_train = encoder.encode_data(protein_seqs)
    with st.spinner('Predictions are calculated...'):
        my_model = load_models()
        predicted_probs = my_model.predict(X_train)
        df = prediction_outputs(protein_ids, protein_seqs, k_positions, predicted_probs)
        df = df.sort_values(by='sumoylation_class_probs', ascending=False)
    st.markdown('<p style="font-size: 2rem;font-family:monospace">Prediction Results </p>',unsafe_allow_html=True)
    st.table(df.head())
    csv = convert_df(df)
    st.download_button(
    "Press to Download Full Predictions",
    csv,
    "sumoylation_predictions.csv",
    "text/csv",
    key='download-csv'
    )

def show_fasta_file_page_content():

    data_processes = Data()
    st.title("""SUMOnet: Deep Sequential Prediction of SUMOylation Sites""")
    st.markdown('<p style="font-family:monospace">Important Note: Streamlit reruns the whole script each time a widget is updated. So please be carefull about refreshing page.</p>',unsafe_allow_html=True)

    st.markdown("***")
    col1, col2 = st.columns(2,gap='medium')
    
    
    # Initialize session_state variable
    if "sequences_input" not in st.session_state:
        st.session_state.sequences_input = ""

    # Initialize session_state variable
    if "uniprot_id_input" not in st.session_state:
        st.session_state.uniprot_id_input = ""

    # Initialize session_state variable
    if "uniprot_lysine_position_input" not in st.session_state:
        st.session_state.uniprot_lysine_position_input = ""
   

    with col1:
        
        fasta_file_title = '<p style="font-size: 2rem;font-family:monospace">Upload a Fasta File</p>'

        st.markdown(fasta_file_title,unsafe_allow_html=True)
        try:
            uploaded_file = st.file_uploader("Choose a file in fasta format")
        except Exception as e:
            st.error('Something goes wrong. Please re-upload the data!', icon="🚨")
            logger.error("Error occurred while uploading fasta file: {error_message}", error_message=str(e))
        prediction_button_for_fasta = st.button('Predict!',key='fasta')

    with col2:

        if uploaded_file:

            if prediction_button_for_fasta:
                    
                    try:
                        with st.spinner('Data is processing...'):
                            protein_ids, protein_seqs, k_positions = data_processes.fasta_file_input(uploaded_file)
                        make_prediction(protein_ids, protein_seqs, k_positions)
                        logger.success(f"Fasta file sequence predicted with protein id: {protein_ids}, protein_seqs: {protein_seqs} and k positions: {k_positions}")
                    except Exception as e:
                        st.error('Error occurred while processing text in fasta file! Please check text format in file, it should be in fasta format!', icon="🚨")
                        logger.error("Error occurred while processing text in fasta file: {error_message}", error_message=str(e))
                
            else:
                st.error('For new prediction please click predict button!', icon="🚨")