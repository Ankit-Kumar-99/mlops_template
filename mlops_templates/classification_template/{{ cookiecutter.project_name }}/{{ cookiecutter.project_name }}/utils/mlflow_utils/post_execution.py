# Databricks notebook source

import os
import yaml
import json
import mlflow 
import time
from datetime import datetime

# COMMAND ----------

# Retrieve the mlflow run ID from the previous task
mlflow_run_id = dbutils.jobs.taskValues.get(taskKey='pre_execution', key='mlflow_run_id', default='None', debugValue='None')

# Retrieve the job configuration in JSON format from the previous task
json_job_config = dbutils.jobs.taskValues.get(taskKey='pre_execution', key='config', default={}, debugValue=0)
config = json.loads(json_job_config)

# Check if artifacts should be logged to mlflow
log_to_mlflow = dbutils.widgets.get('log_artifacts_to_mlflow')
if log_to_mlflow == 'true':
    # Start an mlflow run and log artifacts
    with mlflow.start_run(run_id=mlflow_run_id):
        mlflow.log_artifacts(f"/{config['output_storage_path']}", artifact_path="datasets")

# Extract the file path from the configuration
file_path = config['output_storage_path'].split('/', 1)[1]
try:
    # Get the current job run details
    details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    details_json = json.loads(details)
    current_job_run_id = details_json['tags']['jobRunId']
    
    # Update the file path with the current job run ID
    file_path = f"{file_path}/{current_job_run_id}"
    
    # Remove the file path if it exists
    dbutils.fs.rm(file_path, True)
except:
    # Print a message if an exception occurs
    print("workflow run files store")

# COMMAND ----------

