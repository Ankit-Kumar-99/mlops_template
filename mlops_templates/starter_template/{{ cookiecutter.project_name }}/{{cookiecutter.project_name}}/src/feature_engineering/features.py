from {{ cookiecutter.project_name }}.src.utils.helpers import read_config

def features_main(config=None):
    """
    Main function to perform the feature engineering.

    This function serves as the main entry point for performing feature engineering
    for the specified model. It reads the configuration using the `read_config` function
    and prints the model name for which feature engineering is being performed. Users can
    customize this function to include specific feature engineering steps as needed.

    Parameters:
    config (dict, optional): A dictionary containing configuration parameters. If not provided,
                             the configuration will be read from the default configuration file
                             using the `read_config` function.

    Usage:
    Call this function to start the feature engineering process. The configuration parameters
    will be read, and you can add your custom feature engineering steps within this function.



    Note:
    Ensure that the configuration file is correctly set up and the `read_config` function
    is working as expected before calling this function.

    If running as a script, the function will be executed automatically.

 
    """
    config = read_config()    
    print(f"Feature eninerring for =====> {config['model_name']}")

if __name__ == "__main__":
    features_main()