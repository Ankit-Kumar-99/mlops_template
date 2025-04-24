import os
import mlflow
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
import pandas as pd
import numpy as np
from {{ cookiecutter.project_name }}.utils.helpers import read_config, get_storage_output_path
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


def main_batch_prediction(config=None):
    """
    Perform batch prediction using a model stored in MLflow and save the results.


    This function:
    1. Reads the configuration file or uses default settings.
    2. Retrieves the latest version of the model from MLflow.
    3. Loads the model.
    4. Reads the input data.
    5. Separates the features and target column from the input data.
    6. Makes predictions on the input data using the loaded model.
    7. Saves the predictions to a specified output path.
    8. Calculates and prints the accuracy of the predictions.


    Args:
        config (dict, optional): Configuration dictionary with settings for prediction. If None, default configuration is used.
    """
    # If no configuration is provided, read the default configuration
    if config is None:
        config = read_config()
   
    # Get the path where output data will be stored
    output_storage_path = get_storage_output_path()
   
    # Define the model name
    model_name = "{{ cookiecutter.project_name }}"
   
    # Initialize the MLflow client
    client = mlflow.tracking.MlflowClient()
   
    # Get the latest version of the model
    model_version = client.get_latest_versions(model_name)[0].version
   
    # Construct the model URI
    model_uri = f"models:/{model_name}/{model_version}"
   
    # Load the model from MLflow
    model = mlflow.sklearn.load_model(model_uri)
   
    # Read the current data from the specified path
    data = read_data("/dbfs/tmp/mlops_classification_framework/input/test_data.csv")
   
    # Separate the features and target column based on configuration
    target_column = config['target_column']
    X_test, y_test = data.drop(target_column, axis=1), data[target_column]
   
    # Make predictions using the loaded model
    predictions = make_prediction(model, X_test)
   
    # Convert predictions to a DataFrame for easier handling and saving
    predictions = pd.DataFrame(predictions, columns=['Prediction'])
   
    # Save the predictions to a CSV file at the specified output path
    predictions.to_csv(f"/{output_storage_path}/{config['output_data']['batch_result_data']}", index=False)
   
    # Print the predictions
    print(predictions)
   
    # Calculate and print the accuracy of the predictions
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")


# Entry point for the script
if __name__ == "__main__":
    main_batch_prediction()





