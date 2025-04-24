# Databricks notebook source
dbutils.widgets.text("current_run_id", "manual")

# COMMAND ----------

import os
import yaml
import json
import mlflow 
import time
from datetime import datetime

username=dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
current_job_run_id = dbutils.widgets.get("current_run_id")

working_directory = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
working_directory = str(working_directory)
config_file_name = "config.yml"
working_directory = f"/Workspace/{working_directory}"
try:
    # root_dir = os.path.abspath(os.path.join(working_directory))
    root_dir = os.path.abspath(os.path.join(working_directory,'..','..'))
    # root_dir = root_dir.replace('/databricks/driver/Some(','/Workspace')
    config_path = os.path.join(root_dir,config_file_name)
    print("config_path" , config_path)
    # Read the configuration file
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        
except:
    root_dir = os.path.abspath(os.path.join(config_file_name,'..','..',))
    # root_dir = os.path.abspath(os.path.join(config_file_name))
    root_dir = root_dir.replace('Some(','/Workspace')
    root_dir = root_dir.replace('set_vars)','')
    config_path = os.path.join(root_dir,config_file_name)
    print("config_path" , config_path)
    # Read the configuration file
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)



# details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
# details_json = json.loads(details)
# current_run_id = details_json['tags']['jobRunId' ]
# print(f"current run Id is - {current_run_id}")
base_config = json.dumps(config)
dbutils.jobs.taskValues.set(key='config', value=base_config)
current_job_run_id=dbutils.widgets.get("current_run_id")
dbutils.jobs.taskValues.set (key='mlflow_run_id', value=current_job_run_id)
dbutils.jobs.taskValues.set (key='env', value=config['env'])

# COMMAND ----------

def start_mlflow_run(experiment_name: str):
    # Fetch the experiment details using MLflow API
    try:
        mlflow.create_experiment(experiment_name)
        experiment = mlflow.get_experiment_by_name(experiment_name)
    except:
        experiment = mlflow.get_experiment_by_name(experiment_name)
       
 
    # Ensure experiment exists
    if experiment is None:
        raise ValueError(f"Experiment with name '{experiment_name}' not found. Ensure it has been created during deployment.")
    else:
        experiment_id = experiment.experiment_id
        print(f"Experiment ID: {experiment_id}")
 
    # Set the experiment by ID (optional if needed)
    mlflow.set_experiment(experiment_name=experiment_name)
 
    # Store experiment_id in task values (for later use in other steps)
    dbutils.jobs.taskValues.set(key='experiment_id', value=experiment_id)
 
    # Use the current job run ID as the run name
    run_name = f"{current_job_run_id}"
 
    with mlflow.start_run(run_name=current_job_run_id, log_system_metrics=True) as run:
        mlflow_run_id = run.info.run_id
        dbutils.jobs.taskValues.set(key='mlflow_run_id', value=mlflow_run_id)
        print(f"Run ID: {mlflow_run_id}")
    return mlflow_run_id
 

# COMMAND ----------

experiment_name = f"/Users/{dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()}/mlops_timeseries_framework_ex"
display(experiment_name)
 
 
# Start the MLflow run
mlflow_run_id = start_mlflow_run(experiment_name)
 
# Optionally print the run ID for confirmation
print(f"Run ID: {mlflow_run_id}")

# COMMAND ----------

import json

# Convert the context to a JSON string
details_json_string = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()

# Parse the JSON string to a Python dictionary
details_dict = json.loads(details_json_string)

# Access the 'jobRunId' from the tags
# current_run_id = details_dict['tags']['jobRunId']

# print(current_run_id)

file_path = f"/Volumes/{config['mlops_catalog']}/{config['mlops_s_schema']}/{config['mlops_s_volume']}/{config['output_storage_path']}/{current_job_run_id}"
print(file_path)

# COMMAND ----------

# dbutils.fs.mkdirs(file_path)
!mkdir -pv {file_path}

# COMMAND ----------


