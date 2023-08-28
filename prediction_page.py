import streamlit as st
import time
import pandas as pd

from sumonet.model.architecture import SUMOnet
from sumonet.utils.data_pipe import Data
from sumonet.utils.encodings import Encoding
from utils.prediction_utils import prediction_outputs

sequences = None
# Store the initial value of widgets in session state

    

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
    with st.spinner('Model is loading...'):
        my_model = load_models()
    with st.spinner('Predictions are calculating...'):
        predicted_probs = my_model.predict(X_train)
        df = prediction_outputs(protein_ids, protein_seqs, k_positions, predicted_probs)
    st.table(df.head())
    csv = convert_df(df)
    st.download_button(
    "Press to Download Full Predictions",
    csv,
    "sumoylation_predictions.csv",
    "text/csv",
    key='download-csv'
    )

def show_predict_page():
    data_processes = Data()
    st.title("""SUMOnet: Deep Sequential Prediction of SUMOylation Sites""")
    st.markdown('<p style="font-family:monospace">Important Note: Streamlit reruns the whole script each time a widget is updated. So please be carefull about refreshing page.</p>',unsafe_allow_html=True)

    st.markdown("***")
    col1, col2 = st.columns(2,gap='medium')

    with col1:
        protein_seqence_input_title = '<p style="font-size: 2rem;font-family:monospace">Protein Sequence</p>'
        st.markdown(protein_seqence_input_title,unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">You can enter protein sequence in fasta format. Multiple sequences are also okay.</p>',unsafe_allow_html=True)
        
        sequences = st.text_area(label="Protein Sequence👇",
            label_visibility= 'visible',
            disabled= False,
            placeholder=">O00566\nMAPQVWRRRTLERCLTEVGKATGRPECFLTIQEGLASKFT")
        
        prediction_button_for_protein_sequence= st.button('Predict!',key='prot_sequence')
        
        st.markdown("***")
        uniprotid_input_title = '<p style="font-size: 2rem;font-family:monospace">Uniprot Id #️⃣</p>'
        st.markdown(uniprotid_input_title,unsafe_allow_html=True)

        st.markdown('<p style="font-family:monospace">You can enter uniprotid and specific Lysine position.</p>',unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">If Lysine position is given, prediction will be made for only that Lysine residue.</p>',unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">If Lysine position is not given, prediction will be made for all Lysine residues in protein sequence.</p>',unsafe_allow_html=True)


        uniprot_id = st.text_input(label = "Uniprot Id👇",
            label_visibility= 'visible',
            disabled= False,
            placeholder="O00566")
        
        lysine_position = st.text_input(label = "Lysine Position👇",
            label_visibility= 'visible',
            disabled= False,
            placeholder="20")
        prediction_button_id_and_position = st.button('Predict!',key='uniprot')

        st.markdown("***")
        fasta_file_title = '<p style="font-size: 2rem;font-family:monospace">Fasta File 📜</p>'

        st.markdown(fasta_file_title,unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a file in fasta format")
        prediction_button_for_fasta = st.button('Predict!',key='fasta')



    with col2:

        st.markdown('<p style="font-size: 2rem;font-family:monospace">Prediction Results </p>',unsafe_allow_html=True)
        

        ## To do predictionları df olarak al
        ## ProtId, 21-mer, predicted_label, predicted_probs
        #with st.spinner('Wait for it...'):
        #        time.sleep(5)
        #st.success('Your Results Are Ready For Download!')

        if sequences:
            if prediction_button_for_protein_sequence:
                with st.spinner('Data is processing...'):
                    
                    protein_ids, protein_seqs, k_positions = data_processes.protein_sequence_input(sequences.split())
                make_prediction(protein_ids, protein_seqs, k_positions)
            else:
                st.error('For new prediction please click predict button!', icon="🚨")


        
        if uniprot_id:
            if prediction_button_id_and_position:
                protein_seq = data_processes.retrive_protein_sequence_with_uniprotid(uniprot_id)
            
                if protein_seq == None:
                    st.error('Enter a valid Uniprot Id', icon="🚨")

                else:
                    with st.spinner('Data is processing...'):
                        if lysine_position:
                            lysine_position = int(lysine_position)
                            protein_ids, protein_seqs, k_positions = data_processes.uniprot_id_input(protein_seq,uniprot_id,lysine_position)
                           

                        else:
                            protein_ids, protein_seqs, k_positions = data_processes.uniprot_id_input(protein_seq,uniprot_id)

                    make_prediction(protein_ids, protein_seqs, k_positions)
            else:
                st.error('For new prediction please click predict button!', icon="🚨")
                

        else:
            if lysine_position and prediction_button_id_and_position:
                st.error('Please enter Uniprot Id', icon="🚨")

        if uploaded_file:

            if prediction_button_for_fasta:
                with st.spinner('Data is processing...'):
                    protein_ids, protein_seqs, k_positions = data_processes.fasta_file_input(uploaded_file)

                make_prediction(protein_ids, protein_seqs, k_positions)
            else:
                st.error('For new prediction please click predict button!', icon="🚨")
        

 