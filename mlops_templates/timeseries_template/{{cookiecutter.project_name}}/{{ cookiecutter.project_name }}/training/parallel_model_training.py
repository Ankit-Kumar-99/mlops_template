import os
import mlflow
from {{ cookiecutter.project_name }}.ingestion.ingest import read_data
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.metrics import mean_squared_error
import ray
from ray.util.spark import setup_ray_cluster,shutdown_ray_cluster
from {{ cookiecutter.project_name }}.utils.helpers import get_root_dir, read_config,get_current_mlflow_run_id,get_storage_output_path


def train_test_split_data(data,feature_column, target_feature, product):
    """
    Split data into training and testing datasets based on dates.
    """
   
    data[target_feature] = data[target_feature].astype(float)  # Ensure target feature is float
    dataset = data[data[feature_column].isin([product])]
    train_data = dataset[(dataset['date'] >= '2013-01-01') & (dataset['date'] <= '2016-12-31')]
    test_data = dataset[dataset['date'] >= '2017-01-01']
    train_data.set_index('date', inplace=True)
    test_data.set_index('date', inplace=True)
    return train_data[[target_feature]], test_data[[target_feature]]
 
 
def arima_forecast(train, test, target_feature):
    """ Perform ARIMA forecasting """
    model = ARIMA(train[target_feature], order=(2,0,1))
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=len(test))
    return predictions, test[target_feature]
 
def prophet_forecast(train, test, target_feature):
    """ Perform Prophet forecasting """
    df_train = pd.DataFrame({'ds': train.index, 'y': train[target_feature].values})
    model = Prophet()
    model.fit(df_train)
    future = model.make_future_dataframe(periods=len(test), freq='D')
    forecast = model.predict(future)
    predictions = forecast.loc[forecast['ds'].isin(test.index), 'yhat'].values
    return predictions, test[target_feature]
 
@ray.remote
def main_train_func(model_type, train, test, target_feature, sku):
    """ Evaluate a single model """
    if model_type == 'ARIMA':
        predictions, actuals = arima_forecast(train, test, target_feature)
    elif model_type == 'Prophet':
        predictions, actuals = prophet_forecast(train, test, target_feature)
    else:
        raise ValueError("Invalid model type")
 
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    return sku, model_type, rmse
 
def main_forecast_all_skus(config):
    """
    Perform forecasting for all SKUs using ARIMA and Prophet models in parallel using Ray.
 
    This function reads data, splits it into training and testing sets for each SKU,
    evaluates ARIMA and Prophet models for each SKU, determines the best model based on
    RMSE (Root Mean Squared Error), and logs the results using MLflow.
 
    Returns:
    -------
    results_df : pandas.DataFrame
        DataFrame containing SKU-wise results including the best model, ARIMA RMSE,
        and Prophet RMSE.
    """
   
 
    # reading preprocessed data
    storage_output_path=get_storage_output_path()
    data = read_data(f"/{storage_output_path}/{config['output_data']['preprocessed']}")
   
    # find root path for python module
    path = get_root_dir()

    print("path",path)
 
    # setup the ray cluster with minimum resources
    conn_str=setup_ray_cluster(
    num_cpus_per_node=4, #number of Cpu core to allocate on each node in the Ray cluster
    num_worker_nodes=1,  #number of worker node in ray cluster
    autocaling=True
   
    )
    # dashboard_host=conn_str[1].split(":")[0] + ":" +conn_str[1].split(":")[1]
    # initilizing ray
    ray.init()
    # job_config=ray.job_config.JobConfig(code_search_path=[path])


    # setup_ray_cluster(
    # min_worker_nodes=1,
    # max_worker_nodes=1,
    # num_cpus_per_node=4,
    # num_gpus_worker_node=0)

    # # Pass any custom Ray configuration with ray.init
    # ray.init(ignore_reinit_error=True) 
 
   
    data['date'] = pd.to_datetime(data['date'])
    feature_column = config["feature_columns"]
    target_feature = config["target_columns"]
    # Extract unique SKUs from data
    sku_list = data[feature_column].unique().tolist()
   
   
    # Define model types
    model_types = ['ARIMA', 'Prophet']
   
    # Create combinations of models and SKUs
    combinations = [(model_type, sku) for model_type in model_types for sku in sku_list]
   
    # Perform model evaluation for each combination in parallel
    results_refs = []
    for model_type, sku in combinations:
        train, test = train_test_split_data(data,feature_column, target_feature, sku)
        result_ref = main_train_func.remote(model_type, train, test, target_feature, sku)
        results_refs.append(result_ref)
   
    # Gather results from Ray tasks
    results = ray.get(results_refs)
 
    # Process results
    results_dict = {}
    for sku, model_type, rmse in results:
        if sku not in results_dict:
            results_dict[sku] = {}
        results_dict[sku][model_type] = rmse
 
    # Determine the best model for each SKU
    best_models = []
    for sku, rmses in results_dict.items():
        best_model = min(rmses, key=rmses.get)
        best_models.append((sku, best_model, rmses['ARIMA'], rmses['Prophet']))
 
    # Create DataFrame to store results
    results_df = pd.DataFrame(best_models, columns=['SKU', 'Best Model', 'ARIMA RMSE', 'Prophet RMSE'])
   
    # Save results to CSV
    storage_output_path=get_storage_output_path()
    results_df.to_csv(f"/{storage_output_path}/{config['output_data']['resutl_data']}", index=False)
   
   
    # Print and return results DataFrame
    print(results_df)
    shutdown_ray_cluster()
 
    # get run_id and log the parameters and metrics to mlflow
    mlflow_run_id=get_current_mlflow_run_id()
    if mlflow_run_id != None:
        with mlflow.start_run(run_id=mlflow_run_id):  
            mlflow.log_param("p", config["Arima_order"]["p"])
            mlflow.log_param("d", config["Arima_order"]["d"])
            mlflow.log_param("q", config["Arima_order"]["q"])
 
            mlflow.log_metric("arima_rmse", results_df['ARIMA RMSE'][0])
            mlflow.log_metric("prophet_rmse", results_df['Prophet RMSE'][0])
    return results_df
 
 
if __name__ == "__main__":
    config = read_config()
    main_forecast_all_skus(config)