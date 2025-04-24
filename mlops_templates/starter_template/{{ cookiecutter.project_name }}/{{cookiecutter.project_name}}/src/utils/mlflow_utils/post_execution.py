# Databricks notebook source
import os
import yaml
import json
import mlflow 
import time
from datetime import datetime

# COMMAND ----------

run_id = dbutils.jobs.taskValues.get(taskKey='pre_execution', key='run_id', default='None', debugValue='None')

json_job_config = dbutils.jobs.taskValues.get(taskKey='pre_execution', key='config', default={}, debugValue=0)
config= json.loads(json_job_config)
log_to_mlflow=dbutils.widgets.get('log_artifacts_to_mlflow')
if log_to_mlflow=='true':
    with mlflow.start_run(run_id=run_id):
        mlflow.log_artifacts(f"/{config['output_storage_path']}", artifact_path="datasets")

file_path = config['output_storage_path'].split('/', 1)[1]
try:
    details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    details_json = json.loads(details)
    current_run_id = details_json['tags']['jobRunId' ]
    file_path=f"{file_path}/{current_run_id}"
    dbutils.fs.rm(file_path,True)
except:
    print("workflow run files store")

# COMMAND ----------

