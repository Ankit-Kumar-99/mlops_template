# MLflow Utils Folder

This folder contains utility scripts and functions related to MLflow and Databricks operations for managing experiments, runs, and integrations.

## Scripts Overview

### mlflow.py

- **Functionality**: Handles MLflow experiment creation, run management, and logging.
- **Usage**:
  - Creates or sets up MLflow experiments based on configuration.
  - Initiates and logs MLflow runs, sets tags and system metrics.
  - Manages experiment IDs and run IDs within MLflow.


### webhook_manager.py

- **Functionality**: Manages Databricks Registry webhooks for triggering jobs based on model events.
- **Usage**:
  - Creates various types of webhooks (e.g., model version created, transitioned stage, etc.) to trigger specified jobs in response to Databricks Model Registry events.

## Dependencies

- `mlflow`: Version 2.9.2
- `databricks_registry_webhooks`: Required for managing Databricks Model Registry webhooks.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install databricks_registry_webhooks mlflow==2.2.2
