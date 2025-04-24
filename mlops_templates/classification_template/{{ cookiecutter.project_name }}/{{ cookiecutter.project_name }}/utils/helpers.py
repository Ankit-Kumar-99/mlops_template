import yaml
import json
import os.path
from pyspark.dbutils import DBUtils
import mlflow

def read_config(config_file='config.yml'):
    """
    Reads and returns the configuration from a YAML file.


    This function reads a YAML configuration file specified by `config_file` and returns its content as a dictionary.
    The default file name is 'config.yml', but you can specify a different file if needed.


    Args:
        config_file (str): The name of the YAML configuration file to read. Default is 'config.yml'.


    Returns:
        dict: A dictionary containing the configuration settings from the YAML file.


    Raises:
        FileNotFoundError: If the specified configuration file does not exist at the determined path.
        yaml.YAMLError: If the YAML file is invalid or cannot be parsed.


    Usage:
        config = read_config('path/to/config.yml')
        print(config)
    """
    print(f"config_file - {config_file}")
    config_path = get_root_dir(config_file)
    print(f"config_path - {config_path}")
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def get_root_dir(filename='config.yml', start_directory=os.getcwd()):
    """
    Recursively searches for a file starting from the current directory and moving up the directory tree.


    This function starts from `start_directory` and looks for the specified file (`filename`). If the file is not found,
    it moves up to the parent directory and continues the search. The search stops when the root directory is reached.


    Args:
        filename (str): The name of the file to search for. Default is 'config.yml'.
        start_directory (str): The directory from which the search begins. Default is the current working directory.


    Returns:
        str: The full path to the file if found. Returns None if the file is not found in the directory tree.


    Usage:
        file_path = get_root_dir('config.yml')
        if file_path:
            print(f"File found: {file_path}")
        else:
            print("File not found")
    """
    from pyspark.dbutils import DBUtils
    try:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    except ImportError:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()

    dbutils = DBUtils(spark)
   
    start_directory = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath()
    start_directory = str(start_directory).replace('Some(','/Workspace')
    current_dir = start_directory

    # Iterate over directories starting from current directory and going up
    while True:
        file_path = os.path.join(current_dir, filename)

        if os.path.isfile(file_path):
            return file_path  # Found the file, return its full path

        # Move up to the parent directory
        parent_dir = os.path.dirname(current_dir)
       
        # Check if reached the root directory (on Unix-like systems '/')
        if parent_dir == current_dir:
            print("file not found")
            return None  # File not found


        # Update current directory to parent directory
        current_dir = parent_dir




def update_config(key: str, value, config_file='config.yml'):
    """
    Updates a specific key-value pair in the configuration file.


    This function reads the configuration file specified by `config_file`, updates the specified key with the new value,
    and writes the updated configuration back to the file.


    Args:
        key (str): The key to update in the configuration file.
        value: The new value to set for the specified key.
        config_file (str): The name of the configuration file to update. Default is 'config.yml'.


    Raises:
        FileNotFoundError: If the configuration file does not exist at the determined path.
        yaml.YAMLError: If the YAML file is invalid or cannot be parsed.
        IOError: If there is an issue writing to the configuration file.


    Usage:
        update_config('new_key', 'new_value', 'path/to/config.yml')
        print("Configuration updated successfully.")
    """
    config_path = get_root_dir(config_file)
    print(config_path)
    print(f'key {key}, value - {value}')
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        print(config)
    config[key] = value


    with open(config_path, "w") as f:
        yaml.dump(config, f)


    print(f"Config file '{config_path}' updated successfully.")




def get_current_mlflow_run_id():
    """
    Retrieves the current MLflow run ID from Databricks task values.


    This function initializes a Spark session, uses Databricks utilities to fetch the MLflow run ID associated with a
    specific task key ('pre_execution'). If the MLflow run ID is not found, it returns None.


    Returns:
        str or None: The MLflow run ID if found, otherwise None.


    Usage:
        mlflow_run_id = get_current_mlflow_run_id()
        if mlflow_run_id:
            print(f"MLflow Run ID: {mlflow_run_id}")
        else:
            print("MLflow Run ID not found")
    """
    try:
        # Try to import and initialize DatabricksSession
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    except ImportError:
        # Fallback to SparkSession if DatabricksSession is not available
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()


    # Initialize DBUtils
    dbutils = DBUtils(spark)


    # Fetch the MLflow run ID from task values
    mlflow_run_id = dbutils.jobs.taskValues.get(
        taskKey='pre_execution',
        key='mlflow_run_id',
        default='None',
        debugValue='None'
    )


    # Return None if the MLflow run ID is not found
    if mlflow_run_id == 'None':
        return None


    return mlflow_run_id




def read_secret(secret_name):
    """
    Retrieves a secret from a specified secret scope.


    This function reads the secret scope from the configuration file and uses Databricks utilities to fetch the value
    of the specified secret from that scope. If the secret scope or secret name is invalid, the function handles errors
    and returns None.


    Args:
        secret_name (str): The name of the secret to retrieve.


    Returns:
        str: The value of the retrieved secret, or None if an error occurs.


    Raises:
        KeyError: If 'secret_scope' is not found in the configuration.
        Exception: If there is an issue reading the secret from Databricks.


    Usage:
        secret_value = read_secret('my_secret')
        if secret_value:
            print(f"Secret Value: {secret_value}")
        else:
            print("Failed to retrieve secret")
    """
    # Store config.yml as a dictionary
    config = read_config()

    try:
        # Try to import and initialize DatabricksSession
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    except ImportError:
        # Fallback to SparkSession if DatabricksSession is not available
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()


    # Initialize DBUtils
    dbutils = DBUtils(spark)


    # Extract the secret_scope from the config
    secret_scope = config.get('secret_scope', None)
   
    # If secret_scope is not found, return None
    if not secret_scope:
        print("Error: 'secret_scope' not found in config.")
        return None


    # Read and return secret value, return None if Error
    try:
        return dbutils.secrets.get(scope=secret_scope, key=secret_name)
    except Exception as e:
        print(f"Error reading secret {secret_name} from scope {secret_scope}: {str(e)}")
        return None




def get_storage_output_path(file_name=None):
    config = read_config()

    try:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    except ImportError:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()

    dbutils = DBUtils(spark)

    # details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    # details_json = json.loads(details)
    
    current_run_id=dbutils.jobs.taskValues.get(taskKey='pre_execution', key='current_job_run_id', default='None', debugValue='None')
    if current_run_id=='None':
        current_run_id=None
    
    storage_output_path = f"/Volumes/{config['mlops_catalog']}/{config['mlops_s_schema']}/{config['mlops_s_volume']}/{config['output_storage_path']}" 
    if current_run_id != None:
        storage_output_path += f"/{current_run_id}"
    else:
        storage_output_path += "/manual"

    return storage_output_path


def load_mlflow_model(model_name):
    """
    Loads a logged model from MLflow.

    This function retrieves the latest version of the model specified by `model_name` from MLflow and loads it using
    MLflow's model loading functions. The model name must correspond to a model registered in MLflow.

    Args:
        model_name (str): The name of the model stored in MLflow.

    Returns:
        object: The loaded model object.

    Raises:
        mlflow.exceptions.MlflowException: If there is an issue retrieving the model or its version.
        KeyError: If the model name does not exist or the version cannot be retrieved.

    Usage:
        model = load_mlflow_model('my_model_name')
        # Use the loaded model for predictions or further processing
    """
    # Retrieve the latest version of the model
    client = mlflow.tracking.MlflowClient()
    latest_version_info = client.get_latest_versions(model_name)[0]
    latest_version = latest_version_info.version

    # Load the latest version of the model logged in MLflow
    model_uri = f"models:/{model_name}/{latest_version}"
    model = mlflow.sklearn.load_model(model_uri)

    # Return the loaded model
    return model


