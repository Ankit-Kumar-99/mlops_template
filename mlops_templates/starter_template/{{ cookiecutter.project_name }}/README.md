# Sales Forecast MLOps Framework

## Overview

This project implements an MLOps framework for sales forecasting using Azure Databricks. It includes modules for data ingestion, model training, tuning, and prediction. This README provides detailed instructions for new users on how to utilize this MLOps framework for their development needs.

## Project Structure

```
{{ cookiecutter.project_name }}/
├── src/
│   ├── evaluation/
│   ├── feature_engineering/
│   │   └── features_main.py
│   ├── ingestion/
│   │   ├── ingest.py
│   │   ├── preprocessing.py
│   ├── prediction/
│   │   └── predictions.py
│   ├── training/
│   │   └── train.py
│   ├── tuning/
│   │   └── tune.py
│   ├── utils/
│   │   ├── helper.py
│   ├── set_vars.py (notebook)
│   ├── __init__.py
│── tests/
│   │── main_test.py
├── .gitignore
├── config.yml
├── databricks.yml
├── README.md
├── requirements.txt
├── run.py
└── resources/
    └── {{ cookiecutter.project_name }}.yml


```

## Configuration Files

### `config.yml`
Contains project-specific configurations such as input file paths and model-related configurations.

### `databricks.yml`
Specifies workspace configurations for different environments (dev, tst, prod) and the default development mode.

## Entry Point

### `run.py`
Serves as the entry point for the MLOps pipeline. It dynamically imports modules based on user input using `argparse`.

## Modules and Scripts

### Ingestion

#### Overview
The `ingestion` folder is responsible for handling the data ingestion process within the MLOps framework. This includes reading data from various sources and performing initial data preprocessing.

#### Structure
- **`ingest.py`**: Contains functions to read data from files.
- **`preprocessing.py`**: The main script for running the ingestion and preprocessing steps, including reading configuration settings.

### Feature Engineering

#### Overview
The `features_main.py` script is responsible for performing feature engineering as part of the MLOps framework. Feature engineering involves creating and selecting the most relevant features to improve model performance.

#### Structure
- **`features_main.py`**: The main script for performing feature engineering. It reads the configuration settings and applies the necessary transformations and feature creations based on the configuration.

### Predictions

#### Overview
The `predictions` folder is responsible for loading and executing the production model to make predictions. This includes reading configuration settings to determine which model to load and using it for prediction tasks.

#### Structure
- **`predictions.py`**: The main script for loading the production model and making predictions.

### Testing

#### Overview
The `testing` folder is designed to write and manage test cases related to models, data processing, and other components of the MLOps framework. This ensures that the code is robust, reliable, and meets the expected performance and accuracy standards.

#### Structure
- **`main_test.py`**: A sample script demonstrating how to initialize a test environment and run basic test functions.

#### Writing Test Cases
The DS team can add their test scripts in this folder. These test scripts can include, but are not limited to:
- Model accuracy tests
- Data validation tests
- Integration tests for data pipelines
- Performance benchmarks

### Training

#### Overview
The `training` folder is dedicated to scripts and functions related to training machine learning models. This folder includes the necessary configurations and execution scripts to train models as part of the MLOps pipeline.

#### Structure
- **`train.py`**: The main script to execute the training process.

### Tuning

#### Overview
The `tuning` folder contains scripts for tuning machine learning models. This process involves optimizing hyperparameters to improve model performance.

#### Structure
- **`tune.py`**: The main script to execute the tuning process.

### Utils Folder

This folder contains utility scripts and functions used in various parts of the project.

#### Structure
- **`helper.py`**: Provides utility functions for managing project configuration and reading the configuration to make it available throughout the project.


## High-Level Templatized Version of the MLOps Framework

### Resources Folder for MLOps Workflow Definitions

#### Overview
The `resources` folder in this project contains configuration files and definitions for managing MLOps workflows. This `README.md` provides guidance on how Data Scientists (DS) can utilize the `{{ cookiecutter.project_name }}.yml` file to define and manage their workflow definitions effectively.

#### Workflow Definition with {{ cookiecutter.project_name }}.yml
The `{{ cookiecutter.project_name }}.yml` file in this folder defines a Databricks workflow specifically tailored for the sales forecast project. It organizes tasks sequentially, managing data ingestion, model training, prediction, etc.

#### Usage Guidelines
1. **Workflow Customization**: Data Scientists can customize the workflow by modifying the `{{ cookiecutter.project_name }}.yml` file or creating a new workflow. They can adjust task dependencies, Python file paths, function names, per project requirements.
2. **Integration with Azure Databricks**: Ensure that the paths and cluster IDs specified in the `{{ cookiecutter.project_name }}.yml` file match the actual Azure Databricks environment setup (`dev`, `tst`, `prod`). Modify these configurations as necessary for different environments.


# Sales Forecast MLOps Framework

## Overview

Welcome to the Sales Forecast MLOps Framework, designed to streamline the process of sales forecasting using Azure Databricks. This framework integrates various components such as data ingestion, model training, hyperparameter tuning, batch prediction, and monitoring data drifts. Here’s a guide on how to effectively use and contribute to this project.

## Prerequisites

Before getting started, ensure you have the following prerequisites:
- Azure Databricks environment set up.
- Required Python libraries installed (see `requirements.txt`).

## Initial Setup

### Clone the Repository

```sh
git clone <repository-url>
cd {{ cookiecutter.project_name }}
```

### Install Dependencies
``` &copy
pip install -r requirements.txt
```

### Configure Databricks CLI
Make sure the Databricks CLI is configured to interact with your Databricks workspace:

```sh
databricks configure --token
```
## Running the Pipeline

### Manually
1. Set Environment Variables: Configure environment variables for your Databricks workspace.

2. Execute the Run Script
```sh
python run.py <function_name>
```

Replace `<function_name>` with the desired function to execute (e.g., {{ cookiecutter.project_name }}.src.preprocess.main_ingestions).

### Using Databricks
1. `Upload to Databricks`: Upload necessary files to your Databricks workspace.

2. `Run Notebooks`: Execute notebooks and scripts defined in your Databricks workflow.

## Branch Management

### Create a New Branch
```sh
git checkout -b <branch-name>
```
### Commit Changes
```sh
git add .
git commit -m "Your commit message"
```
### Push to Remote
```sh 
git push origin <branch-name>
```
## Contributing

Feedback and Improvements: Provide feedback or suggest improvements to workflow definitions ({{ cookiecutter.project_name }}.yml) and related scripts (run.py, notebooks).
Pull Requests: To contribute changes, fork the repository, make modifications, and submit a pull request for review.






