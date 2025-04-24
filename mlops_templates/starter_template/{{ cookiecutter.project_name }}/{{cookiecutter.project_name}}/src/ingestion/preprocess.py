import pandas as pd
import json
from {{ cookiecutter.project_name }}.src.utils.helpers import read_config
from {{ cookiecutter.project_name }}.src.ingestion.ingest import read_data
from {{ cookiecutter.project_name }}.src.utils.datadrift import detect_drift

def main_ingestions(config=None):
    """
    Main function to perform data ingestion and preprocessing.

    This function serves as the main entry point for performing data ingestion
    and preprocessing for the specified model. It reads the configuration using
    the `read_config` function and prints the model name for which data ingestion
    and preprocessing is being performed. Users can customize this function to
    include specific data ingestion and preprocessing steps as needed.

    Parameters:
    config (dict, optional): A dictionary containing configuration parameters. If not provided,
                             the configuration will be read from the default configuration file
                             using the `read_config` function.

    Usage:
    Call this function to start the data ingestion and preprocessing process. The configuration
    parameters will be read, and you can add your custom data ingestion and preprocessing steps
    within this function.

    
    Note:
    Ensure that the configuration file is correctly set up and the `read_config` function
    is working as expected before calling this function.

    If running as a script, the function will be executed automatically.
 
    """
    config = read_config() if config is None else config
    print(f"Ingestion and preprocessing for ====> {config['model_name']}")

    datasets_time_series = read_data(f"{config['input_data']['file_path']}")
    modified_data = datasets_time_series
    modified_data["date"] = pd.to_datetime(modified_data["date"])
    modified_data.drop(["Unnamed: 0"], inplace=True, axis=1)
    # Create reference and current DataFrames
    reference_df = datasets_time_series.sample(frac=0.5, random_state=1)  # Reference DataFrame (50% of the data)
    current_df = datasets_time_series.sample(frac=0.5, random_state=2)
    # Run drift detection tests
    drift_results = detect_drift(reference_df, current_df)
    # Print drift results in JSON format
    print(json.dumps(drift_results, indent=2))
    with open("drift_result.json",'w') as f:
        json.dump(drift_results,f,indent=2)
   

if __name__ == "__main__":
    main_ingestions()
