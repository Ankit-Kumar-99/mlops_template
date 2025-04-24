from {{ cookiecutter.project_name }}.src.utils.helpers import read_config

def main_tunner(config=None):
    """
    Main function to tune the model .

    This function serves as the main entry point for tuning a machine learning model. 
    It prints a message indicating that the Start the tuining the model. Users can customize
    this function to include specific Tune logic as needed.

    Parameters:
    config (dict, optional): A dictionary containing configuration parameters. If not provided,
                             the configuration will be read from the default configuration file
                             using the `read_config` function.

    Usage:
    Call this function begin the model tuning process. The configuration
    parameters can be read, and you can add your custom tuning steps within this function.

    Example:
        def main_tunner(config=None):
            print(" Start the tuining the model ")
            # Add your  Tune logic here
            # e.g., initialize Ray, define the search space, start tuning, etc.
            import ray
            from ray import tune
            
            ray.init()
            search_space = {
                "learning_rate": tune.grid_search([0.01, 0.1, 1.0]),
                "batch_size": tune.choice([16, 32, 64])
            }
            
            def trainable(config):
                # Your training logic here
                pass
            
            tune.run(trainable, config=search_space)

    Note:
    Ensure that Ray and Ray Tune are installed and correctly set up in your environment
    before calling this function.

    If running as a script, the function will be executed automatically with the configuration
    read from the configuration file.

    Example usage as a script:
        if __name__ == "__main__":
            config = read_config()
            main_tunner(config)
    """
    print(" Start the tuining the model ")

if __name__ == "__main__":
    config = read_config()
    main_tunner(config)