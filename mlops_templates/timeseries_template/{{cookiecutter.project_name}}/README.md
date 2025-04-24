# Time series MLOps framework
 
## Overview
 
This project is designed to streamline the development and deployment of time series machine learning models. It includes various modules to facilitate different stages of the machine learning workflow, including data ingestion, preprocessing, model training, and experiment tracking. Each module is tailored to handle specific tasks efficiently, ensuring a cohesive and scalable MLOps framework.

## Project Structure
```
MLOPS/
├── azure-pipelines/
├── {{ cookiecutter.project_name }}/
│   ├── ingestion/
│   │   ├── ingest.py
│   │   ├── preprocessing.py
│   ├── training/
│   │   └── parallel_model_training.py
│   ├── utils/
│   │   ├── helper.py
|   |   ├── update_libs.py
│   |   ├── mlflow_utils/
│   │       └── post_execution.py  
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

````
 
## Modules
 
### Ingestion Module
 
The Ingestion module focuses on reading, preprocessing, and saving data, preparing it for downstream analysis and modeling.
 
#### Structure
 
- **ingest.py**: Contains functions to read data from files into pandas DataFrames.
- **preprocess.py**: Provides functions for preprocessing data, such as removing duplicates and formatting for specific analytic needs.
 
#### Usage
 
Ensure `config.yml` is configured with appropriate data paths.
 
- **Read Data**: Use `read_data` from `ingest.py` to read data from CSV files.
- **Preprocess Data**: Functions in `preprocess.py` handle data cleaning and transformation.
- **Main Ingestion**: Execute `main_ingestions` to run complete ingestion and preprocessing pipelines.
 
### Training Module
 
The Training module focuses on parallelized training and evaluation of time series models (ARIMA and Prophet) using Ray.
 
#### Overview
 
- **Parallelized Training**: Uses Ray for efficient model training across multiple SKUs.
- **Model Evaluation**: Compares ARIMA and Prophet models based on RMSE.
- **Configuration-Based**: Reads dynamic settings from `config.yml`.
- **MLflow Integration**: Logs model metrics to MLflow for tracking and comparison.
- **Result Logging**: Saves evaluation results as CSV and MLflow artifacts.
 
#### Structure
 
- `config.yml`: Configuration file for data paths and model settings.
- `train.py`: Main script for data handling, training, and evaluation using Ray.
 
#### Parallelization with Ray
 
1. **Initialization**: Initialize Ray with desired CPU resources.
   ```python
   ray.init(num_cpus=4)  # Adjust num_cpus based on available resources
2. **Data Handling**:Read and Preprocess Data for Each SKU
 
    ```python
    results_refs = []
    for sku in sku_list:
        train_data, test_data = preprocess_data(data, sku)
        result_ref = main_train_func.remote(train_data, test_data, sku)
        results_refs.append(result_ref)
 
    results = ray.get(results_refs)
 
### Utils Module
 
#### Overview
The Utils module provides utility functions for managing project configurations and dependencies.
 
#### Structure
`update_libs.py:` Updates library requirements in YAML files.
 
`helper.py:` Functions for reading, finding, and updating configuration files.
 
`MLflow Utils Folder`
This folder contains scripts for MLflow and Databricks operations.

`post_execution.py`: The code to perform some tasks related to workflow execution and logging.Checks if artifacts should be logged to MLflow based on the value of log_to_mlflow parameter.

  
#### Usage
**Configuration**: Configure config.yml with appropriate settings.
 
**Run**: Execute scripts (train.py, etc.) for specific tasks.
 
**Monitor**: Track progress and metrics using MLflow UI.
 
 
## Getting Started
 
### Steps to Use This Template
1. **Clone the Repository**: Clone this repository to your local machine or Databricks workspace.
`git clone <repository_url>`
2. **Configure the Project**: Update the config.yml file with your specific settings for data paths, model parameters, and other configurations.
3. **Ingest Data**: Use the ingestion module to read and preprocess your data.
```python
from ingestion.ingest import read_data
data = read_data('path/to/your/data.csv')
```
4. **Train Models**: Execute the training script to start training your time series models.
``` sh
python train.py
```
5. **Track Experiments**: Monitor your experiments and model performance using the MLflow UI.
 
## Databricks Asset Bundles
 
Databricks asset bundles allow you to package and deploy your ML models and workflows seamlessly.
 
1. **Define Assets**: Specify your models, notebooks, and other assets in a structured format.
2. **Bundle Assets**: Create asset bundles using Databricks CLI or the Databricks workspace UI.
3. **Deploy Assets**: Deploy the bundled assets to different environments (dev, test, prod) as defined in your config.yml.
 
By following these steps and utilizing the provided modules, you can efficiently develop, deploy, and monitor time series models using this MLOps framework on Databricks.
 
## Using Databricks Repos and Starting with the Template
 
### Introduction
This guide provides a comprehensive step-by-step approach for using Databricks Repos and starting with the provided time-series project template. The instructions are designed to help new users set up and utilize the template efficiently.
 
### Databricks Repos
Databricks Repos is a version control feature in Databricks that allows you to integrate with Git repositories. It provides an efficient way to manage and synchronize your code, making collaboration easier.
 
## Steps to Use Databricks Repos
### 1. Create a Databricks Repo:
 
- Navigate to your Databricks workspace.
- Go to the "Repos" tab on the sidebar.
- Click on the "Create" button and select "Azure Devops Repo" (or your preferred Git provider).
- Link your Databricks workspace to your Azure Devops Repo - repository by following the authentication steps.
 
### 2. Clone the Repo:
 
- After linking your Azure Devops account, you can clone a repository.
- Click on the "Repos" tab, then "Clone Repo".
- Enter the URL of your Azure Devops repository and click "Clone".
- This action will create a new folder in your Databricks workspace containing the cloned repository.
 
### 3. Sync Changes:
 
- Regularly sync changes between your local repository and Databricks Repo to keep the code up to date.
- You can use the "Fetch", "Pull", and "Push" options in the Databricks Repos UI to synchronize changes.
- Fetch: Fetches updates from the remote repository.
- Pull: Merges changes from the remote repository into your local repo.
- Push: Pushes your local changes to the remote repository.
 
### 4. Run Notebooks:
 
- Once your repository is cloned, you can navigate through the folders to find your notebooks.
- Open any notebook and click "Run All" to execute the cells.

### 5. Run Python Script Files:

- If you make changes to any other file that is imported in your script, it is crucial to clear the state and run all cells again to ensure the latest changes are incorporated.
##### Steps to Run Python Scripts After Changes
- Clear State: In the Databricks workspace, go to the notebook or script you are working on.
Clear the state by selecting "Clear State" from the "Edit" menu. This ensures that all previous variables and imports are reset.
- Run All Cells: After clearing the state, click "Run All" to execute all cells from the beginning.
This step ensures that any changes in the imported files are correctly reflected in the current execution context.

 
 
## Starting with the Template
This template is designed to streamline the development and deployment of time-series machine learning models. Below are the detailed steps to get started:
 
### 1. Clone the Repository:
 
- Clone this repository to your local machine or directly to your Databricks workspace using the steps mentioned above.
- Command line option (if cloning locally):
```sh
    git clone <repository_url>
```
 
 
### 2. Configure the Project:
 
- Update the config.yml file with your specific settings for data paths, model parameters, and other configurations.
- The config.yml file is located in the root directory of the project.
- Example configuration:
``` yaml
environments:
  dev:
    data_path: "/path/to/data"
    model_params:
      param1: value1
      param2: value2
```
### 3. Ingest Data:
 
- Use the ingestion module to read and preprocess your data.
- Example code to read data:
``` python
from ingestion.ingest import read_data
data = read_data('path/to/your/data.csv')
```
### 4. Train Models:
 
- Execute the training script to start training your time-series models.
- Command line option:
```sh
python train.py
```
### 5.Track Experiments:
 
- Monitor your experiments and model performance using the MLflow UI.
- MLflow logs will be generated as the models are trained.
## Adding New Code and Workflow Steps
### 1.Add New Code:
 
- Place your new scripts or modules in the appropriate directory (e.g., ingestion, training, utils).
### 2. Update Workflows:
 
- Modify the workflow scripts (e.g., train.py) to integrate your new code.
- Ensure the new steps are added to the pipeline logic.
### 3. Update config.yml:
 
- If your new code requires additional configurations, update the config.yml file accordingly.
- Example:
```yaml
Copy code
new_feature:
  param1: value1
  param2: value2
```
### 4. Update Task in Resources Folder:
 
- When a new task is introduced, update the corresponding YAML file in the resources folder.
- Add the new task under the appropriate section, ensuring that all necessary configurations and dependencies are specified.
- Example:
```yaml
Copy code
tasks:
  - name: existing_task
    ...
  - name: new_task
    ...
```

## Enhancements and Future Updates

To utilize and improve this template further, consider the following enhancements:

**1. Cookiecutter Integration**: Incorporate Cookiecutter to automate the creation of project scaffolding, ensuring a standardized structure across different projects.
**2.Enhanced Data Validation**: Add robust data validation checks to ensure data quality before processing and model training.


## Conclusion

By following this framework, you can efficiently manage the lifecycle of time series machine learning models, from data ingestion to model training and deployment. The modular structure allows for easy customization and extension, enabling you to adapt the framework to your specific needs. Future updates, such as Cookiecutter integration and advanced monitoring, will further enhance the usability and scalability of this MLOps framework.