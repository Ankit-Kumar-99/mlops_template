import os
from sklearn.preprocessing import StandardScaler
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
import pandas as pd
from {{ cookiecutter.project_name }}.utils.helpers import get_root_dir, read_config, get_storage_output_path, get_current_mlflow_run_id
from {{ cookiecutter.project_name }}.utils.datadrift import detect_drift
from pyspark.dbutils import DBUtils
from sklearn.model_selection import train_test_split
import mlflow
import json


def drop_duplicate_data(dataframe: pd.DataFrame):
    """
    Check for and drop duplicate data in a DataFrame.

    This function identifies and removes duplicate rows in the given DataFrame. It prints
    the number of rows dropped due to duplication.

    Args:
        dataframe (pd.DataFrame): The input DataFrame to be checked for duplicates.

    Returns:
        pd.DataFrame: The DataFrame after removing duplicate rows.

    Example:
        data = drop_duplicate_data(dataframe)
        print(data)
    """
    orignal_row = dataframe.shape[0]
    dataframe.drop_duplicates(inplace=True)
    current_row = dataframe.shape[0]

    if current_row == orignal_row:
        print("No duplicates data found. Number of rows: {}".format(current_row))
    else:
        print("Duplicates data found and number of rows dropped: {}".format(orignal_row - current_row))

    return dataframe

def handle_missing_values(dataframe):
    """
    Handle misisng values in the DataFrame.

    For simplicity, this function fills misisng values with the mean of the respective values.

    Args:
        dataframe (pd.DataFrame): The input DataFrame with potential missing values.

    Returns:
        pd.DataFrame: The DataFrame after filling missing values.
    """
    dataframe.fillna(dataframe.mean(), inplace=True)
    return dataframe

def scale_features(dataframe: pd.DataFrame, feature_columns: list):
    """
    Scale feature columns in the DataFrame using StandardScaler.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        feature_columns (list): List of feature columns to be scaled.

    Returns:
        pd.DataFrame: The DataFrame with scaled features.
    """
    scaler = StandardScaler()
    dataframe[feature_columns] = scaler.fit_transform(dataframe[feature_columns])
    return dataframe

def preprocess(data, config=None):
    """
    Preprocess classification data.

    This function reads the classification data from the specified file path in the configuration,
    removes duplicates, handles missing values, and scale the features.

    Args:
        config (dict): The configuration dictionary containing file paths and feature details.

    Example:
        preprocess(config)
    """
    # Check if the config is None
    if config is None:
        # If config is None, read the configuration
        config = read_config()

    # Remove duplicate entries from the data
    data = drop_duplicate_data(data)

    # Handle any missing values in the data
    data = handle_missing_values(data)

    # Get the feature columns from the configuration
    feature_columns = config.get('feature_columns')

    # Scale the features in the data based on the feature columns
    data = scale_features(data, feature_columns)

    # Return the processed data
    return data


def main_drift_detection(config=None):
    # If no configuration is provided, read the default configuration
    if config is None:
        config = read_config()
    
    # Get the path where output data will be stored
    output_storage_path = get_storage_output_path()
    
    # Read the reference data and current data from the specified path in the configuration
    train_data = read_data(f"{output_storage_path}/{config['output_data']['train_data']}")
    test_data = read_data(f"{output_storage_path}/{config['output_data']['test_data']}")
    
    # Detect drift between the reference data and the current data
    drift_results = detect_drift(train_data, test_data)
    print(json.dumps(drift_results, indent=2))
    
    # Save the drift report to a CSV file at the specified path
    with open("drift_result.json",'w') as f:
        json.dump(drift_results,f,indent=2) 
    
    # Get the current run ID for logging purposes
    mlflow_run_id = get_current_mlflow_run_id()

    # If a run ID is available, log the artifacts using MLflow
    if mlflow_run_id:
        with mlflow.start_run(run_id=mlflow_run_id):
            mlflow.log_artifacts(f"drift_results.json", artifact_path="report")


def main_ingestion(config=None):
    """
    Main ingestion function to preprocess and save data.

    This function reads the configuration, loads the data, removes duplicates, preprocesses the
    time series data for the dashboard, and saves the preprocessed data to MLflow and CSV files.

    Args:
        config (dict, optional): The configuration dictionary. If not provided, it will be read from 'config.yml'.

    Example:
        main_ingestion()
    """

    # reading input data
    data = read_data(f"/Volumes/{config['mlops_catalog']}/{config['mlops_b_schema']}/{config['mlops_b_volume']}/{config['input_file_path']}")

    data = preprocess(data)

    # save preprocessed data 
    storage_output_path=get_storage_output_path()
    data.to_csv(f"{storage_output_path}/{config['output_data']['preprocessed']}") 

    # Splitting data for datadrift    
    train_data, test_data = train_test_split(data, test_size=0.5, random_state=42)
    train_data.to_csv(f"{storage_output_path}/{config['output_data']['train_data']}")
    test_data.to_csv(f"{storage_output_path}/{config['output_data']['test_data']}")
    print(f"current and reference dataset saved at /{storage_output_path}/{config['output_data']}")
    
if __name__ == "__main__":
    config = read_config()
    main_ingestion(config)
