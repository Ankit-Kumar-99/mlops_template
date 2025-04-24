import yaml
import os.path

def read_config(config_file='config.yml'):
    """
    Read and return the configuration from a YAML file.

    This function searches for the specified configuration file starting from the
    current working directory and moving up recursively. Once found, it reads the
    YAML file and returns the configuration as a dictionary.

    Args:
        config_file (str): The name of the configuration file to read. Defaults to 'config.yml'.

    Returns:
        dict: The configuration data loaded from the YAML file.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        yaml.YAMLError: If there is an error in parsing the YAML file.

    Example:
        config = read_config('config.yml')
        print(config)
    """
    print(f"config_file - {config_file}")
    config_path = find_file_recursive(config_file)
    print(f"config_path - {config_path}")
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def find_file_recursive(filename, start_directory=os.getcwd()):
    """
    Recursively search for a file starting from a specified directory.

    This function starts searching for the specified file from the given start directory
    and moves up through the directory tree until the file is found or the root directory is reached.

    Args:
        filename (str): The name of the file to search for.
        start_directory (str): The directory to start searching from. Defaults to the current working directory.

    Returns:
        str: The full path of the file if found.
        None: If the file is not found.

    Example:
        file_path = find_file_recursive('config.yml')
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
    Update a specific key-value pair in the YAML configuration file.

    This function searches for the specified configuration file, updates the specified key
    with the new value, and writes the updated configuration back to the file.

    Args:
        key (str): The key to update in the configuration.
        value: The new value for the specified key.
        config_file (str): The name of the configuration file to update. Defaults to 'config.yml'.

    Example:
        update_config('model_name', 'new_model_name')
    """
    config_path = find_file_recursive(config_file)
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
    Retrieve the current MLflow run ID.

    This function attempts to create a Databricks session. If unsuccessful, it falls back to 
    creating a Spark session. It then uses DBUtils to get the MLflow run ID from the task values 
    of a job. If no run ID is found, it returns None.

    Returns:
    str or None: The current MLflow run ID, or None if no run ID is found.
    """
    try:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    except ImportError:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()

    dbutils = DBUtils(spark)
    mlflow_run_id = dbutils.jobs.taskValues.get(taskKey='pre_execution', key='run_id', default='None', debugValue='None')
    if mlflow_run_id == 'None':
        mlflow_run_id = None
    return mlflow_run_id


def read_secret(secret_name):
    """
    Retrieves a secret from a specified secret scope.

    Args:
        secret_name (str): The name of the secret.
        secret_scope (str): The name of the secret scope.

    Returns:
        str: The value of the retrieved secret.

    To create a secret scope backed by Azure Key Vault:
    1. Edit your workspace URL, which looks like this: adb-XXXXX.azuredatabricks.net/?o=YYYYYY.
    2. Append #/secrets/createScope to the URL.
    3. This will take you to a page where you can create a secret scope.
    4. Provide the name of your secret scope, the Azure Key Vault URL, and the resource ID.
    """
    config = read_config()

    # Extract the secret_scope from the config
    secret_scope = config.get('secret_scope', None)
    
    if not secret_scope:
        print("Error: 'secret_scope' not found in config.")
        return None

    try:
        return dbutils.secrets.get(scope=secret_scope, key=secret_name)
    except Exception as e:
        print(f"Error reading secret {secret_name} from scope {secret_scope}: {str(e)}")
        return None

def get_storage_output_path():
    """
    Retrieve the storage output path based on the current job run ID.

    This function reads the configuration, create a Databricks session.
    It then uses DBUtils to get the current job run ID 
    from the notebook context. Based on the job run ID, it constructs the storage output path and 
    creates the necessary directories in the file system.
    
    Behavior:
    Manual Execution: If the code is run manually (outside of a Databricks workflow), the intermediate data is stored in a folder named manual in DBFS (Databricks File System).
    Databricks Workflow Execution: If the code is run within a Databricks workflow, the intermediate data is stored in a folder created with the job ID of that workflow.
    
    Returns:
    str: The storage output path.
    """
    config = read_config()

    try:
        from databricks.connect import DatabricksSession
        spark = DatabricksSession.builder.getOrCreate()
    except ImportError:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()

    dbutils = DBUtils(spark)

    details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    details_json = json.loads(details)
    try:
        current_job_run_id = details_json['tags']['jobRunId']
    except:
        current_job_run_id = None
    
    if current_job_run_id != None:
        storage_output_path = f"{config['output_storage_path']}/{current_job_run_id}"
        file_path = config['output_storage_path'].split('/', 1)[1]
        dbutils.fs.mkdirs(f"{file_path}/{current_job_run_id}")
    else:
        storage_output_path = f"{config['output_storage_path']}/manual"
        file_path = config['output_storage_path'].split('/', 1)[1]
        dbutils.fs.mkdirs(f"{file_path}/manual")

    return storage_output_path