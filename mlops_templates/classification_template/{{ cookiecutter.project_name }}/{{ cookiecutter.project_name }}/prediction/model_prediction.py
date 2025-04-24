import os
import mlflow
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
import pandas as pd
import numpy as np
from {{ cookiecutter.project_name }}.utils.helpers import get_root_dir, read_config, get_current_mlflow_run_id, get_storage_output_path, load_mlflow_model
import joblib
from sklearn.metrics import accuracy_score


def make_prediction(model, input_data):
    """
    Make predictions using the provided model and input data.


    Args:
        model (sklearn.base.BaseEstimator): The trained scikit-learn model.
        input_data (pd.DataFrame or np.ndarray): The input features for prediction.


    Returns:
        np.ndarray: The predicted labels.
    """
    return model.predict(input_data)


def main_prediction(config=None):
    """
    Handle the prediction process by loading a model and making predictions on the input data.


    This function:
    1. Reads the configuration file or uses default settings if none are provided.
    2. Retrieves the path where output data will be stored.
    3. Checks for the current MLflow run ID to determine if logging is required.
    4. Loads the model either from MLflow (if run ID is available) or from a local file.
    5. Reads the input data from the specified path.
    6. Separates features and target column from the input data.
    7. Makes predictions using the loaded model.
    8. Saves the predictions to a specified output path.
    9. Prints the predictions and calculates the accuracy.
    10. Logs the accuracy metric to MLflow if a run ID is available.


    Args:
        config (dict, optional): Configuration dictionary with settings for prediction. If None, default configuration is used.
    """
    # If no configuration is provided, read the default configuration
    if config is None:
        config = read_config()
   
    # Get the path where output data will be stored
    output_storage_path = get_storage_output_path()
   
    # Get the current MLflow run ID for logging purposes
    mlflow_run_id = get_current_mlflow_run_id()


    # Load the model from MLflow if a run ID is available; otherwise, load from a local file
    if mlflow_run_id:
        model = load_mlflow_model("{{  cookiecutter.project_name }}")
    else:
        model = joblib.load(f"/{output_storage_path}/{config['output_data']['model']}")
   
    # Read the current data from the specified path in the configuration
    data = read_data(f"/{output_storage_path}/{config['output_data']['test_data']}")
   
    # Separate the features and target column based on the configuration
    target_column = config['target_column']
    X_test, y_test = data.drop(target_column, axis=1), data[target_column]
   
    # Make predictions using the loaded model
    predictions = make_prediction(model, X_test)
    
    # Convert predictions to a DataFrame for easier handling and saving
    predictions = pd.DataFrame(predictions, columns=['Prediction'])
   
    # Save the predictions to a CSV file at the specified output path
    predictions.to_csv(f"{output_storage_path}/{config['output_data']['result_data']}", index=False)
   
    # Print the predictions
    print(predictions)
   
    # Calculate and print the accuracy of the predictions
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")
   
    # If a run ID is available, log the accuracy metric using MLflow
    if mlflow_run_id:
        with mlflow.start_run(run_id=mlflow_run_id):
            mlflow.log_metric("accuracy", accuracy)


# Entry point for the script
if __name__ == "__main__":
    main_prediction()
