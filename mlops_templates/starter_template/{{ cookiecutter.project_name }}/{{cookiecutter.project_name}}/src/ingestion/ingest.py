import pandas as pd
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.getOrCreate()

def read_data(file_name):
    """
    Reads a CSV file and returns it as a pandas DataFrame.

    This function reads a CSV file from the specified path and returns the data
    as a pandas DataFrame. It uses the pandas `read_csv` function with a comma
    as the default separator.

    Args:
        file_name (str): Path to the CSV file.
    
    Returns:
        pandas.DataFrame: The loaded data.
    
    Usage:
    Call this function with the path to your CSV file to load the data into a pandas DataFrame.
    You can then manipulate, analyze, or process the data as needed using pandas.

    
    Note:
    Ensure that the specified file path is correct and that the CSV file exists
    at that location. The function expects the file to have a comma as the delimiter.
    """
    data = pd.read_csv(file_name, sep=',')
    return data
