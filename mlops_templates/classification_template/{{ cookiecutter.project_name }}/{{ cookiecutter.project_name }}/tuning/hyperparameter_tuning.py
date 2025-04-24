import mlflow
import ray
from ray import tune, train
from ray.util.spark import setup_ray_cluster, shutdown_ray_cluster
from ray.tune.schedulers import ASHAScheduler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from {{ cookiecutter.project_name }}.utils.helpers import get_root_dir, read_config, get_current_mlflow_run_id, get_storage_output_path
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
from ray.job_config import JobConfig


def train_and_evaluate(config, X_train, y_train, X_test, y_test):
    """
    Train and evaluate a logistic regression model using the provided hyperparameters.


    Args:
        config (dict): Dictionary containing hyperparameters for the model.
        X_train (pd.DataFrame or np.ndarray): Features used for training the model.
        y_train (pd.Series or np.ndarray): Target labels used for training the model.
        X_test (pd.DataFrame or np.ndarray): Features used for evaluating the model.
        y_test (pd.Series or np.ndarray): Target labels used for evaluating the model.


    Returns:
        dict: A dictionary containing the accuracy of the model on the test data.
    """
    # Initialize the logistic regression model with parameters from the config
    try:
        model = LogisticRegression(
        C=config["C"],
        solver=config["solver"],
        random_state=42
        )
        # Train the model on the training data
        model.fit(X_train, y_train)
        # Predict the target values for the test data
        y_pred = model.predict(X_test)
        # Calculate the accuracy of the predictions
        accuracy = accuracy_score(y_test, y_pred)
        # Report the accuracy to Ray Tune
        train.report({"accuracy": accuracy})
        return {"accuracy": accuracy}
    except Exception as e:
        train.report({"error": str(e)})
        raise e


    



def main_tuning(config=None):
    """
    Main function to handle hyperparameter tuning for a logistic regression model using Ray Tune.


    This function:
    1. Reads the configuration file or uses default settings if none are provided.
    2. Sets up the Ray cluster with specified resources.
    3. Initializes Ray with the dashboard host and port.
    4. Reads the reference and current data from specified paths.
    5. Separates features and target column for training and testing.
    6. Defines the hyperparameter search space for tuning.
    7. Sets up the ASHA scheduler for hyperparameter tuning.
    8. Configures and runs the hyperparameter tuning with Ray Tune.
    9. Prints the best configuration based on accuracy.
    10. Logs the best hyperparameters to MLflow if a run ID is found.
    11. Shuts down the Ray cluster.


    Args:
        config (dict, optional): Configuration dictionary with settings for hyperparameter tuning. If None, default configuration is used.
    """
    # If no configuration is provided, read the default configuration
    if config is None:
        config = read_config()


    root_path = get_root_dir()
    conn_str = setup_ray_cluster(
        num_cpus_per_node=4,
        num_worker_nodes=1,
        autocaling=True,
        
    )

    dashboard_host = conn_str[1].split(":")[0] + ":" + conn_str[1].split(":")[1]
   
    # Initialize Ray with the dashboard host and port
    ray.init(dashboard_host=dashboard_host, dashboard_port=conn_str[1].split(':')[-1],job_config=JobConfig(code_search_path=[root_path]))


    # Get the path where output data will be stored
    output_storage_path = get_storage_output_path()
   
    # Read the reference and current data from the specified paths in the configuration
    train_data = read_data(f"{output_storage_path}/{config['output_data']['train_data']}")
    test_data = read_data(f"{output_storage_path}/{config['output_data']['test_data']}")
   
    # Separate the features and target column for training and testing
    target_column = config['target_column']
    X_train, y_train = train_data.drop(target_column, axis=1), train_data[target_column]
    X_test, y_test = test_data.drop(target_column, axis=1), test_data[target_column]
    print("-----------------------------------------------------------------")
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print("head of X_train: ", X_train.head(5))
    print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    print("head of X_test: ", X_test.head(5))
    print("-----------------------------------------------------------------")


    # Define the hyperparameter search space
    search_space = {
        "C": tune.grid_search(list(map(float, config["hyperparameters"]["C"]))),
        "solver": tune.grid_search(config["hyperparameters"]["solver"])
    }
   


    # Set up the ASHA scheduler for hyperparameter tuning
    scheduler = ASHAScheduler(
        metric="accuracy",
        mode="max",
        max_t=10,
        grace_period=1,
    )

    # Set up the tuner with the search space and scheduler
    tuner = tune.Tuner(
        tune.with_resources(
            tune.with_parameters(train_and_evaluate, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test),
            resources={"cpu": 1, "gpu": 0}
        ),
        param_space=search_space,
        tune_config=tune.TuneConfig(
            scheduler=scheduler,
            num_samples=10,
        ),
    )

    # Run the hyperparameter tuning
    results = tuner.fit()

    # Get the best result based on accuracy
    best_result = results.get_best_result(metric="accuracy", mode="max")
    print(f"Best Config: {best_result.config}")

    # Shut down the Ray cluster
    shutdown_ray_cluster()

    # Get the current run ID for logging purposes
    mlflow_run_id = get_current_mlflow_run_id()
    if mlflow_run_id:
        with mlflow.start_run(run_id=mlflow_run_id):
            mlflow.log_params(best_result.config)

# Entry point for the script
if __name__ == "__main__":
    main_tuning()
