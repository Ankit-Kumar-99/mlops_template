from {{ cookiecutter.project_name }}.src.utils.helpers import read_config

def main_training(config=None):
    """
    Main function to perform model training.

    This function serves as the main entry point for training a machine learning model.
    It reads the configuration using the `read_config` function, retrieves the model name
    from the configuration, and prints a message indicating that training is being
    performed for the specified model. Users can customize this function to include
    specific training logic as needed.

    Parameters:
    config (dict, optional): A dictionary containing configuration parameters. If not provided,
                             the configuration will be read from the default configuration file
                             using the `read_config` function.

    Usage:
    Call this function to start the training process for your model. The configuration parameters
    will be read, and you can add your custom training steps within this function.

    Example:
        def main_training(config=None):
            config = read_config()
            print(f"Training for ====> {config['model_name']}")
            # Add your training logic here
            # e.g., load data, preprocess data, train the model, save the model, etc.
            training_data = load_data(config['training_data_path'])
            model = train_model(training_data, config['model_params'])
            save_model(model, config['model_output_path'])

    Note:
    Ensure that the configuration file is correctly set up and the `read_config` function
    is working as expected before calling this function.

    If running as a script, the function will be executed automatically.

    Example usage as a script:
        if __name__ == "__main__":
            main_training()
    """
    config = read_config() if config is None else config
    print(f"Training for ====> {config['model_name']}")

if __name__ == "__main__":
    main_training()
