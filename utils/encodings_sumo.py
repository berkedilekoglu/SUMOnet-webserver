import joblib
import numpy as np
import pandas as pd
import epitopepredict as ep
import os

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))



def get_min_max_scaler_path():

        return os.path.join(script_dir, "minmax_scaler", "minmax_scaler.gz")

def minmax(X):

        minmax_scaler = joblib.load(get_min_max_scaler_path())
        return minmax_scaler.transform(X)

def reshape(X):

    return X.reshape(len(X),21,X.shape[1]//21)

def blosum_helper(seq):
    #encode a peptide into blosum features
    blosum = ep.blosum62
    x = pd.DataFrame([blosum[i] for i in seq]).reset_index(drop=True)

    e = x.values.flatten()    

    return e

def bl_encoder(data):
    
    bl_data = list(map(blosum_helper,data))
        
    bl_data = np.asarray(bl_data,dtype='float32')

    return bl_data     

def preprocess(data):
        
        
        data = minmax(data)
        return reshape(data)

def get_encoded_X_vector_from_data(X):

        """
        This function is used to get encoded representation of given vectors.

        Args:

            X: List that contains samples.

        Output:

            self.X: Encoded samples
        """


        X = bl_encoder(X)

        return preprocess(X)
