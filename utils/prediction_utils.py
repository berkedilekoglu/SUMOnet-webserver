import pandas as pd

def create_dataframe(protein_id, peptide_seq, k_position, predicted_probs, predicted_labels):

    data_dict = {'protein_id':protein_id,
                 'peptide_seq':peptide_seq,
                 'lysine_position':k_position,
                 'nonsumoylation_class_probs':predicted_probs[:,0],
                 'sumoylation_class_probs':predicted_probs[:,1],
                 'predicted_labels':predicted_labels}

    return pd.DataFrame(data_dict)

def prediction_outputs(protein_id, peptide_seq, k_position, predicted_probs):

    
    predicted_labels = predicted_probs.argmax(-1)
    return create_dataframe(protein_id, peptide_seq, k_position, predicted_probs, predicted_labels)
