import pandas as pd

def read_data(file_name):
    """
    reading pandas dataframe 
    Args:
        file_name: str file name with path 

    Return:
        data: pandas dataframe
    """

    data = pd.read_csv(file_name, sep=',' )
    return data
