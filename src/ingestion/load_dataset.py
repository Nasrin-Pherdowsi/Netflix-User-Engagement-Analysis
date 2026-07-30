import numpy as np

from src.config import DATASET_PATH

def load_dataset():
    # loads dataset and returns it as a structured numpy array (np.ndarray)

    #np.genfromtxt is used for mixed-type business datasets
    dataset = np.genfromtxt(DATASET_PATH,      #the csv file path
                         delimiter=',',     #delimiter helps NumPy understand where one column ends
                         names=True,        #first row is the column names row
                         dtype=None,        #data type of each col gets detected automaticallly
                         encoding='utf-8')  #standard encoding is followed
    return dataset