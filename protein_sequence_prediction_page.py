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

def show_protein_sequence_page_content():
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
            st.text('Please click again if examples were not loaded or refresh page.')


    with col2:

        if sequences:
            if prediction_button_for_protein_sequence:

                try:

                    with st.spinner('Data is processing...'):
                        sequence_list = data_processes.fasta_to_list(sequences)
                        protein_ids, protein_seqs, k_positions = data_processes.protein_sequence_input(sequence_list)
                    make_prediction(protein_ids, protein_seqs, k_positions)

                except Exception as e:

                    logger.error("Error occurred while making prediction : {error_message}", error_message=str(e))
                    st.error(f'Please make sure the input is fasta formatted and try again!', icon="🚨")
                                
            else:
                st.error('For new prediction please click predict button!', icon="🚨")