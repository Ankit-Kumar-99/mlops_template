# Training Module

## Overview

This module is designed to perform parallelized training and evaluation of time series models (ARIMA and Prophet) for multiple SKUs using Ray. The results of the model evaluation are logged using MLflow. This approach ensures efficient utilization of resources and speeds up the training process.

## Features

- **Parallelized Training**: Utilizes Ray to parallelize the training and evaluation of ARIMA and Prophet models for multiple SKUs.
- **Model Evaluation**: Compares the performance of ARIMA and Prophet models based on Root Mean Squared Error (RMSE).
- **Configuration-Based**: Reads configuration settings from `config.yml` for dynamic and flexible processing.
- **MLflow Integration**: Logs model parameters and performance metrics to MLflow for easy tracking and comparison.
- **Result Logging**: Saves the evaluation results as a CSV file and logs it as an artifact in MLflow.

## File Structure

- `config.yml`: Configuration file containing settings for data paths, ARIMA model parameters, and MLflow run ID.
- `train.py`: Main script that performs data reading, training, and evaluation of models using Ray.

## How Parallelization is Achieved

Parallelization is achieved using Ray, a framework for building and running distributed applications. The following steps outline the process:

1. **Initialization**: Ray is initialized with the desired number of CPUs.
    ```python
    ray.init(num_cpus=1)  # Adjust num_cpus based on your resources
    ```

2. **Data Reading and Preprocessing**: The data is read and preprocessed. The dataset is split into training and testing sets for each SKU.
    ```python
    data = read_data(f"{root_dir}/{config['input_data']['file_path']}")
    data['date'] = pd.to_datetime(data['date'])
    ```

3. **Parallel Model Evaluation**: The `main_train_func` function, decorated with `@ray.remote`, is used to evaluate ARIMA and Prophet models for each SKU in parallel. The function is invoked remotely for each SKU, and the results are collected asynchronously.
    ```python
    results_refs = []
    for sku in sku_list:
        train, test = train_test_split_data(data, target_feature, sku)
        result_ref = main_train_func.remote(train, test, target_feature, sku)
        results_refs.append(result_ref)
    
    results = ray.get(results_refs)
    ```

4. **Result Logging and Saving**: The results are compiled into a DataFrame, saved as a CSV file, and logged as an MLflow artifact.
    ```python
    results_df = pd.DataFrame({
        'SKU': skus,
        'Best Model': best_models,
        'ARIMA RMSE': arima_rmse_list,
        'Prophet RMSE': prophet_rmse_list
    })

    results_csv_path = "/tmp/results.csv"
    results_df.to_csv(results_csv_path, index=False)
    mlflow.log_artifact(results_csv_path, artifact_path="forecast_results")
    ```

## How to Use

1. **Set Up Configuration**: Ensure that the `config.yml` file is properly set up with the necessary configuration settings such as data paths, ARIMA model parameters, and MLflow run ID.

2. **Install Dependencies**: Install the required dependencies including Ray, MLflow, Prophet, and Statsmodels.
    ```bash
    pip install ray mlflow prophet statsmodels pandas numpy 
    ```

3. **Run the Script**: Execute the `train.py` script to start the forecasting process.
    ```bash
    python train.py
    ```

4. **View Results**: After the script execution, the results will be logged in MLflow. You can view the performance metrics and the best model for each SKU in the MLflow UI.

## Example

Here's an example of how you can utilize the `main_forecast_all_skus` function:
```python
if __name__ == "__main__":
    results_df = main_forecast_all_skus()
    print(results_df)
