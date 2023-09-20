import streamlit as st
import time
import pandas as pd

from sumonet.model.architecture import SUMOnet
from sumonet.utils.data_pipe import Data
from sumonet.utils.encodings import Encoding
from utils.prediction_utils import prediction_outputs

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
    with st.spinner('Processing...'):
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



def show_predict_page():
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
        
        uniprotid_input_title = '<p style="font-size: 2rem;font-family:monospace">Enter UniprotID</p>'
        st.markdown(uniprotid_input_title,unsafe_allow_html=True)

        st.markdown('<p style="font-family:monospace">Please enter a valid UniprotID and/or a specific Lysine position. If a Lysine position is provided, the model will predict the SUMOylation status of that position. Otherwise, SUMOnet will be provide predictions for all Lysine positions in the sequence.</p>',unsafe_allow_html=True)

        uniprot_id = st.text_input(label = "Uniprot Id👇",
            label_visibility= 'visible',
            disabled= False,
            placeholder="O00566",
            value=st.session_state.uniprot_id_input)

        lysine_position = st.text_input(label = "Lysine Position👇",
            label_visibility= 'visible',
            disabled= False,
            placeholder="20",
            value=st.session_state.uniprot_lysine_position_input)
        
        col5, col6, _, _, _= st.columns(5,gap='small')
        with col5:
            load_sample_button_for_uniprot_id= st.button('Load Sample',key='load_sample_uniprot')
        with col6:
            prediction_button_id_and_position = st.button('Predict!',key='uniprot')
            
        if load_sample_button_for_uniprot_id:
            st.session_state.uniprot_id_input = "O00566"
            st.session_state.uniprot_lysine_position_input = "20"
            st.text('Please refresh page if examples were not loaded.')
            
        st.markdown("***")
        protein_seqence_input_title = '<p style="font-size: 2rem;font-family:monospace">Enter Protein Sequence(s)</p>'
        st.markdown(protein_seqence_input_title,unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">You may enter multiple or a single sequence in fasta format. SUMOnet will scan for all Lysine positions.</p>',unsafe_allow_html=True)

        sequences = st.text_area(label="Protein Sequence👇",
            label_visibility= 'visible',
            disabled= False,
            placeholder=">sp|Q9UER7|DAXX_HUMAN Death domain-associated protein 6 OS=Homo sapiens OX=9606 GN=DAXX PE=1 SV=2\nMATANSIIVLDDDDEDEAAAQPGPSHPLPNAASPGAEAPSSSEPHGARGSSSSGGKKCYK\nLENEKLFEEFLELCKMQTADHPEVVPFLYNRQQRAHSLFLASAEFCNILSRVLSRARSRP\nAKLYVYINELCTVLKAHSAKKKLNLAPAATTSNEPSGNNPPTHLSLDPTNAENTASQSPR\nTRGSRRQIQRLEQLLALYVAEIRRLQEKELDLSELDDPDSAYLQEARLKRKLIRLFGRLC\nELKDCSSLTGRVIEQRIPYRGTRYPEVNRRIERLINKPGPDTFPDYGDVLRAVEKAAARH\nSLGLPRQQLQLMAQDAFRDVGIRLQERRHLDLIYNFGCHLTDDYRPGVDPALSDPVLARR\nLRENRSLAMSRLDEVISKYAMLQDKSEEGERKKRRARLQGTSSHSADTPEASLDSGEGPS\nGMASQGCPSASRAETDDEDDEESDEEEEEEEEEEEEEATDSEEEEDLEQMQEGQEDDEEE\nDEEEEAAAGKDGDKSPMSSLQISNEKNLEPGKQISRSSGEQQNKGRIVSPSLLSEEPLAP\nSSIDAESNGEQPEELTLEEESPVSQLFELEIEALPLDTPSSVETDISSSRKQSEEPFTTV\nLENGAGMVSSTSFNGGVSPHNWGDSGPPCKKSRKEKKQTGSGPLGNSYVERQRSVHEKNG\nKKICTLPSPPSPLASLAPVADSSTRVDSPSHGLVTSSLCIPSPARLSQTPHSQPPRPGTC\nKTSVATQCDPEEIIVLSDSD",
            value=st.session_state.sequences_input  
            )
        
        col3, col4, _, _, _= st.columns(5,gap='small')
        with col3:
            load_sample_button_for_protein_sequence= st.button('Load Sample',key='load_sample_sequence')
        with col4:
            prediction_button_for_protein_sequence= st.button('Predict!',key='prot_sequence')
       
        if load_sample_button_for_protein_sequence:
            st.session_state.sequences_input = ">sp|Q9UER7|DAXX_HUMAN Death domain-associated protein 6 OS=Homo sapiens OX=9606 GN=DAXX PE=1 SV=2\nMATANSIIVLDDDDEDEAAAQPGPSHPLPNAASPGAEAPSSSEPHGARGSSSSGGKKCYK\nLENEKLFEEFLELCKMQTADHPEVVPFLYNRQQRAHSLFLASAEFCNILSRVLSRARSRP\nAKLYVYINELCTVLKAHSAKKKLNLAPAATTSNEPSGNNPPTHLSLDPTNAENTASQSPR\nTRGSRRQIQRLEQLLALYVAEIRRLQEKELDLSELDDPDSAYLQEARLKRKLIRLFGRLC\nELKDCSSLTGRVIEQRIPYRGTRYPEVNRRIERLINKPGPDTFPDYGDVLRAVEKAAARH\nSLGLPRQQLQLMAQDAFRDVGIRLQERRHLDLIYNFGCHLTDDYRPGVDPALSDPVLARR\nLRENRSLAMSRLDEVISKYAMLQDKSEEGERKKRRARLQGTSSHSADTPEASLDSGEGPS\nGMASQGCPSASRAETDDEDDEESDEEEEEEEEEEEEEATDSEEEEDLEQMQEGQEDDEEE\nDEEEEAAAGKDGDKSPMSSLQISNEKNLEPGKQISRSSGEQQNKGRIVSPSLLSEEPLAP\nSSIDAESNGEQPEELTLEEESPVSQLFELEIEALPLDTPSSVETDISSSRKQSEEPFTTV\nLENGAGMVSSTSFNGGVSPHNWGDSGPPCKKSRKEKKQTGSGPLGNSYVERQRSVHEKNG\nKKICTLPSPPSPLASLAPVADSSTRVDSPSHGLVTSSLCIPSPARLSQTPHSQPPRPGTC\nKTSVATQCDPEEIIVLSDSD"
            st.text('Please refresh page if examples were not loaded.')
        
        
        st.markdown("***")
        fasta_file_title = '<p style="font-size: 2rem;font-family:monospace">Upload a Fasta File</p>'

        st.markdown(fasta_file_title,unsafe_allow_html=True)
        try:
            uploaded_file = st.file_uploader("Choose a file in fasta format")
        except:
            st.error('Something goes wrong. Please re-upload the data!', icon="🚨")
        prediction_button_for_fasta = st.button('Predict!',key='fasta')



    with col2:

        if sequences:
            if prediction_button_for_protein_sequence:
                with st.spinner('Data is processing...'):
                    sequence_list = data_processes.fasta_to_list(sequences)
                    protein_ids, protein_seqs, k_positions = data_processes.protein_sequence_input(sequence_list)
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
        

 