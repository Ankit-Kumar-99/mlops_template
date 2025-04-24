import os
import mlflow
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from {{ cookiecutter.project_name }}.utils.helpers import get_root_dir, read_config, get_current_mlflow_run_id, get_storage_output_path
import joblib


def train_model(X_train, y_train, best_params=None):
    """
    Train a Logistic Regression model on the provided training data.


    If `best_params` is provided, the model is initialized with those parameters.
    Otherwise, the model is initialized with default parameters.


    Parameters:
    ----------
    X_train : pd.DataFrame
        Feature data for training the model.
    y_train : pd.Series
        Target values corresponding to the training data.
    best_params : dict, optional
        Dictionary containing hyperparameters for initializing the Logistic Regression model. 
        The dictionary must include "C" (float) and "solver" (str). If None, default parameters are used.


    Returns:
    -------
    model : LogisticRegression
        The trained Logistic Regression model.
    """
    # Initialize the Logistic Regression model with provided parameters or defaults
    if best_params is not None:
        model = LogisticRegression(
            C=float(best_params["C"]),  # Regularization parameter
            solver=best_params["solver"],  # Optimization algorithm
            random_state=42  # Seed for reproducibility
        )
    else:
        # Use default parameters for the Logistic Regression model
        model = LogisticRegression(random_state=42)
   
    # Fit the model to the training data
    model.fit(X_train, y_train)
    return model


def save_model(model, config):
    """
    Save the trained model either to MLflow or locally based on the presence of an MLflow run ID.


    If an MLflow run ID is available, the model is logged and registered with MLflow. 
    If no run ID is found, the model is saved locally using `joblib`.


    Parameters:
    ----------
    model : LogisticRegression
        The trained Logistic Regression model to be saved.
    config : dict
        Configuration dictionary that includes paths for saving the model.
        Must contain the key 'output_data' with a subkey 'model' specifying the local file path.
    """
    # Retrieve the output storage path from configuration
    output_storage_path = get_storage_output_path()
   
    # Get the current MLflow run ID for logging purposes
    mlflow_run_id = get_current_mlflow_run_id()
   
    # Description for the model
    description = "This is a logistic regression model for diabetes classification."


    if mlflow_run_id:
        # If an MLflow run ID is present, log and register the model with MLflow
        with mlflow.start_run(run_id=mlflow_run_id):
            mlflow.sklearn.log_model(model, "{{  cookiecutter.project_name }}")  # Log model to MLflow
            model_name = "{{  cookiecutter.project_name }}"  # Define the model name for MLflow registry
            model_uri = f"runs:/{mlflow_run_id}/{{  cookiecutter.project_name }}"  # Model URI for registration
            mlflow.register_model(model_uri, model_name)  # Register the model in the MLflow model registry
            mlflow.set_tag("model_description", description)  # Add a description tag to the model
    else:
        # If no MLflow run ID is found, save the model locally
        model_path = f"{output_storage_path}/{config['output_data']['model']}"
        joblib.dump(model, model_path)  # Save the model using joblib


def main_training(config=None):
    """
    Main function to orchestrate the training of a Logistic Regression model.


    This function reads the configuration, processes the data, trains the model, and saves it.
    If an MLflow run ID is available, it uses the parameters from MLflow; otherwise, it uses default parameters.


    Parameters:
    ----------
    config : dict, optional
        Configuration dictionary. If None, default configuration is read from a configuration file.


    Returns:
    -------
    None
    """
    # If no configuration is provided, read the default configuration
    if config is None:
        config = read_config()


    # Retrieve the output storage path from configuration
    output_storage_path = get_storage_output_path()
   
    # Read the reference data from the specified path in the configuration
    data = read_data(f"{output_storage_path}/{config['output_data']['train_data']}")
   
    # Separate the features and target column from the data
    target_column = config['target_column']
    X_train, y_train = data.drop(target_column, axis=1), data[target_column]
   
    # Get the current MLflow run ID for logging purposes
    mlflow_run_id = get_current_mlflow_run_id()
    if mlflow_run_id:
        # If an MLflow run ID is present, use it to fetch hyperparameters and train the model
        with mlflow.start_run(run_id=mlflow_run_id):
            best_params = mlflow.active_run().data.params  # Fetch best parameters from MLflow
            model = train_model(X_train, y_train, best_params)  # Train model with the best parameters
    else:
        # Train the model with default parameters if no MLflow run ID is available
        model = train_model(X_train, y_train)
   
    # Save the trained model to the appropriate location
    save_model(model, config)


# Entry point for the script
if __name__ == "__main__":
    main_training()
