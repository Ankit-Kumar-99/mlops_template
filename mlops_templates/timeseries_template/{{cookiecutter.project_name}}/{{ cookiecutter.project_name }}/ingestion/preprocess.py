import os
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
import pandas as pd
import mlflow
import json
from {{ cookiecutter.project_name }}.utils.helpers import get_root_dir, read_config,get_current_mlflow_run_id,get_storage_output_path
from pyspark.dbutils import DBUtils
from {{ cookiecutter.project_name }}.utils.datadrift import detect_drift


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

def preprocess(config):
    """
    Preprocess time series data for the dashboard.

    This function reads the time series data from the specified file path in the configuration,
    converts the date column to datetime format, and drops the 'Unnamed: 0' column.

    Args:
        config (dict): The configuration dictionary containing file paths.

    Example:
        preprocess_dashboard_data_time(config)
    """
    path = get_root_dir()
    root_dir = os.path.dirname(path)
    datasets_time_series = read_data(f"/Volumes/{config['mlops_catalog']}/{config['mlops_b_schema']}/{config['mlops_b_volume']}/{config['input_file_path']}")
    modified_data = datasets_time_series
    modified_data["date"] = pd.to_datetime(modified_data["date"])
    modified_data.drop(["Unnamed: 0"], inplace=True, axis=1)

def caluate_drift(config=None):
    """
    Calculate and log data drift between reference and current datasets.

    This function reads data from the specified file path in the config, splits the data into 
    reference and current DataFrames, detects drift between these DataFrames, and logs the 
    results. The drift results are saved to a JSON file and logged as an artifact in MLflow.

    Parameters:
    config (dict, optional): Configuration dictionary containing the input data file path.

    Steps:
    1. Read data from the file path specified in the config.
    2. Split the data into reference and current DataFrames (50% each).
    3. Detect drift between the reference and current DataFrames.
    4. Print the drift results in JSON format.
    5. Save the drift results to a JSON file.
    6. Log the drift results JSON file as an artifact in MLflow if a current MLflow run exists.

    Returns:
    None
    """
    # Create reference and current DataFrames
    read_data(f"/Volumes/{config['mlops_catalog']}/{config['mlops_b_schema']}/{config['mlops_b_volume']}/{config['input_file_path']}")
    reference_df = datasets[['sales']].sample(frac=0.5, random_state=1)  # Reference DataFrame (50% of the data)
    current_df = datasets[['sales']].sample(frac=0.5, random_state=2)    # Current DataFrame (50% of the data)
    drift_results = detect_drift(reference_df, current_df)
    print(json.dumps(drift_results, indent=2))
    
    # Saving result
    with open("drift_result.json", 'w') as f:
        json.dump(drift_results, f, indent=2)
    
    # Log results to MLflow 
    mlflow_run_id = get_current_mlflow_run_id()
    if mlflow_run_id is not None:
        with mlflow.start_run(run_id=mlflow_run_id):
            mlflow.log_artifact("drift_result.json", artifact_path="drift_detection")


def main_ingestions(config=None):
    """
    Main ingestion function to preprocess and save data.

    This function reads the configuration, loads the data, removes duplicates, preprocesses the
    time series data for the dashboard, and saves the preprocessed data to MLflow and CSV files.

    Args:
        config (dict, optional): The configuration dictionary. If not provided, it will be read from 'config.yml'.

    Example:
        main_ingestions()
    """
    # reading input data
    datasets = read_data(f"/Volumes/{config['mlops_catalog']}/{config['mlops_b_schema']}/{config['mlops_b_volume']}/{config['input_file_path']}")
    data = drop_duplicate_data(dataframe=datasets)
    preprocess(config)
    # save preprocessed data 
    storage_output_path=get_storage_output_path()
    data.to_csv(f"/{storage_output_path}/{config['output_data']['preprocessed']}")     


if __name__ == "__main__":
    config = read_config()
    main_ingestions(config)

