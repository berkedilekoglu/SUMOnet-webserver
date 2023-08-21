import requests as r
from Bio import SeqIO
from io import StringIO



def extract_subseq_with_k_position(sequence:str,position:int) -> str:

    """
    Take protein sequence and 'K' position as an input and find 21-mer which includes 'K' at the middle. Use padding with 'X'.
    
    Parameters:
        sequence (str): Amino acid sequence of the protein.
        position (int): Position of the 'K'. It is not array index. Position is index + 1.
        
    Returns:
        str: 21-mer which includes 'K' at the middle
    """

    half_mer_len = 10

    i = position - 1

    if sequence[i] == 'K':

        left_side = sequence[max(0,i-half_mer_len):i]
        right_side = sequence[i+1:i+1+half_mer_len]

        if len(left_side) < 10:

            left_side = 'X' * (10-len(left_side)) + left_side

        if len(right_side) < 10:

            right_side = right_side + 'X' * (10-len(right_side))


        subseq = left_side + 'K' + right_side

        return subseq
    
    else:
        #Todo:
        #Giving an error might be better
        #User should be noticed for that situation!
        return None
    
def find_mers_with_K(sequence:str) -> list: 

    """
    Take protein sequence as an input and find each 21-mer which includes 'K' at the middle. Use padding with 'X'.
    
    Parameters:
        sequence (str): Amino acid sequence of the protein.
        
    Returns:
        list: List of 21-mers which includes 'K' at the middle
    """

    mers = []
    for i in range(len(sequence)):

        if sequence[i] == 'K':
            position = i+1
            subseq = extract_subseq_with_k_position(sequence,position)

            
            mers.append(subseq)

    return mers


def retrive_protein_sequence_with_uniprotid(uniprot_id:str) -> str :

    """
    Fetches the protein sequence for a given UniProt ID.
    
    Parameters:
        uniprot_id (str): The UniProt ID of the protein.
        
    Returns:
        str: The protein sequence if successful, None otherwise.
    """

    baseUrl="http://www.uniprot.org/uniprot/"
    currentUrl=baseUrl+uniprot_id+".fasta"
    response = r.post(currentUrl)
    cData=''.join(response.text)

    Seq=StringIO(cData)

    protein_sequence = list(SeqIO.parse(Seq,'fasta'))[0].seq

    return str(protein_sequence)

