from {{ cookiecutter.project_name }}.src.utils.helpers import read_config

def main_predictions(config=None):
    """
    Main function to perform model loading and predictions.

    This function serves as the main entry point for loading the production model
    and making predictions. It reads the configuration using the `read_config` function,
    retrieves the model name from the configuration, and prints messages indicating the
    loading of the model and the prediction process. Users can customize this function
    to include specific prediction logic as needed.

    Parameters:
    config (dict, optional): A dictionary containing configuration parameters. If not provided,
                             the configuration will be read from the default configuration file
                             using the `read_config` function.

    Usage:
    Call this function to start the process of loading the production model and making predictions.
    The configuration parameters will be read, and you can add your custom model loading and
    prediction steps within this function.

    Example:
        def main_predictions(config=None):
            config = read_config()
            prod_model = config["model_name"]
            print(f"Loading =======> {prod_model}")
            print("Prediction")
            # Add your model loading logic here
            # model = load_model(config['model_path'])
            # Add your prediction logic here
            # predictions = model.predict(test_data)
            # print(f"Predictions: {predictions}")

    Note:
    Ensure that the configuration file is correctly set up and the `read_config` function
    is working as expected before calling this function.

    If running as a script, the function will be executed automatically.

    Example usage as a script:
        if __name__ == "__main__":
            main_predictions()
    """
    config = read_config() if config is None else config
    prod_model = config["model_name"]
    print(f"Loading =======> {prod_model}")
    print("Prediction")

if __name__ == "__main__":    
    main_predictions()