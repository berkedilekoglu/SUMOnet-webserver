import requests as r
import re
from Bio import SeqIO
from io import StringIO
from typing import List, Tuple
from loguru import logger



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
    k_positions = []
    for i in range(len(sequence)):

        if sequence[i] == 'K':
            position = i+1
            subseq = extract_subseq_with_k_position(sequence,position)

            
            mers.append(subseq)
            k_positions.append(position)

    return mers, k_positions


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

    try:
        response = r.post(currentUrl)
        cData=''.join(response.text)

        Seq=StringIO(cData)

        protein_sequence = list(SeqIO.parse(Seq,'fasta'))[0].seq

        return str(protein_sequence)
    
    except:

        return None

def protein_sequence_input(sequence_fasta_list:List[str]) -> Tuple[List[str], List[str]]:

    protein_ids, protein_seqs,k_positions = [], [], []

    for index, item in enumerate(sequence_fasta_list):

        if index % 2 == 0:

            protein_id = item

        else:

            mers, k_position = find_mers_with_K(item)
            
            protein_seqs += mers
            k_positions += k_position
            protein_ids += [protein_id] * len(mers)
            

    return protein_ids, protein_seqs, k_positions

def uniprot_id_input(protein_sequence,uniprot_id,lysine_position=None):

    protein_ids, protein_seqs, k_positions = [], [], []

    if lysine_position == None:

        protein_seqs, k_positions = find_mers_with_K(protein_sequence)
        protein_ids+=[uniprot_id] * len(protein_seqs)

    else:

        subseq = extract_subseq_with_k_position(protein_sequence,lysine_position)   
        
        protein_ids.append(uniprot_id)
        protein_seqs.append(subseq)
        k_positions.append(lysine_position)

    return protein_ids, protein_seqs, k_positions

def fasta_file_input(readed_file):

    print(readed_file.read().decode("utf-8"))
    content_list = readed_file.read().decode("utf-8").splitlines()        

    return protein_sequence_input(content_list)

def extract_protein_id(header):
    # Define the regex pattern to match the identifier between the vertical bars
    identifier_pattern = r'\|([^|]+)\|'

    # Search for the identifier using the regex pattern
    match = re.search(identifier_pattern, header)

    if match:
        identifier = match.group(1)
        return identifier
    else:
        logger.warning(f"Identifier not found in the header: {header}")
        return header
        

def fasta_to_list(entire_text:str):

    lines = entire_text.split('\n')
    
    sequence_lines = []
    sequences = []
    for line in lines:

        if line.startswith('>'):

                if len(sequence_lines) > 0:

                    sequence = ''.join(sequence_lines)
                    sequences.append(sequence)

                    sequence_lines = []

                header = extract_protein_id(line)
                sequences.append(header)

        else:

            sequence_lines.append(line)
    
    #For the last seq
    sequence = ''.join(sequence_lines)
    sequences.append(sequence)

    return sequences

    