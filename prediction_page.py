import streamlit as st
import time

from model import SUMOnet
from utils import *
from encodings_sumo import *

sequences = None
# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = ">O00566\nMAPQVWRRRTLERCLTEVGKATGRPECFLTIQEGLASKFT"

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

@st.cache_resource()
def load_models():

    return SUMOnet()

def show_predict_page():

    st.title("""SUMOnet: Deep Sequential Prediction of SUMOylation Sites""")
    st.markdown('<p style="font-family:monospace">Important Note: Streamlit reruns the whole script each time a widget is updated. So please be carefull about refreshing page.</p>',unsafe_allow_html=True)

    st.markdown("***")
    col1, col2 = st.columns(2,gap='medium')

    with col1:
        protein_seqence_input_title = '<p style="font-size: 2rem;font-family:monospace">Protein Sequence 🧬</p>'
        st.markdown(protein_seqence_input_title,unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">You can enter protein sequence in fasta format. Multiple sequences are also okay.</p>',unsafe_allow_html=True)
        
        sequences = st.text_area(label="Protein Sequence👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder)
        
        st.markdown("***")
        uniprotid_input_title = '<p style="font-size: 2rem;font-family:monospace">Uniprot Id #️⃣</p>'
        st.markdown(uniprotid_input_title,unsafe_allow_html=True)

        st.markdown('<p style="font-family:monospace">You can enter uniprotid and specific Lysine position.</p>',unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">If Lysine position is given, prediction will be made for only that Lysine residue.</p>',unsafe_allow_html=True)
        st.markdown('<p style="font-family:monospace">If Lysine position is not given, prediction will be made for all Lysine residues in protein sequence.</p>',unsafe_allow_html=True)


        uniprot_id = st.text_input(label = "Uniprot Id👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder="O00566")
        
        lysine_position = st.text_input(label = "Lysine Position👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder="20")
        

        st.markdown("***")
        fasta_file_title = '<p style="font-size: 2rem;font-family:monospace">Fasta File 📜</p>'

        st.markdown(fasta_file_title,unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a file in fasta format")



    with col2:

        st.markdown('<p style="font-size: 2rem;font-family:monospace">Prediction Results </p>',unsafe_allow_html=True)
        

        ## To do predictionları df olarak al
        ## ProtId, 21-mer, predicted_label, predicted_probs
        #with st.spinner('Wait for it...'):
        #        time.sleep(5)
        #st.success('Your Results Are Ready For Download!')

        if sequences:
            with st.spinner('Data is processing...'):
                sequence_list = sequences.split()
                X_ = get_encoded_X_vector_from_data(sequence_list)
            with st.spinner('Model is loading...'):
                my_model = load_models()
            with st.spinner('Predictions are calculating...'):
                preds = my_model.predict(X_)
            st.write(str(preds))
        #csv = convert_df(df)

        #st.download_button(
        #"Press to Download",
        #csv,
        #"file.csv",
        #"text/csv",
        #key='download-csv'
        #)

 