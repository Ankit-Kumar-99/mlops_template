# Databricks notebook source
import os
import yaml
import json


config_file_name = "config.yml"
root_dir = os.path.abspath(os.path.join(config_file_name,'..','..','..'))
root_dir = root_dir.replace('Some(','/Workspace')
config_path = os.path.join(root_dir,config_file_name)
# Read the configuration file
with open(config_path, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)




details = dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
details_json = json.loads(details)
current_run_id = details_json['tags']['jobRunId' ]
print(f"current run Id is - {current_run_id}")
dbutils.jobs.taskValues.set (key='current_run_id', value=current_run_id)
dbutils.jobs.taskValues.set (key='env', value=config['env'])

# COMMAND ----------

