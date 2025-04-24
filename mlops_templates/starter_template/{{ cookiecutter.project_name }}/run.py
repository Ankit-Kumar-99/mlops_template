import argparse
import importlib
import sys
import {{ cookiecutter.project_name }}
from {{ cookiecutter.project_name }}.src.utils.helpers import read_config

def main():
    """
    Main function to dynamically call a specified function with a configuration file.

    This function parses the command line arguments to get the function path to call.
    It reads the configuration using the `read_config` function, dynamically imports
    the specified module, retrieves the function, and calls it with the configuration.

    Usage:
        python script.py <function_path>

    Args:
        <function_path> (str): The dot-separated path to the function to call.
                               Example: src.utils.mlflow_utils.create_mlflow.mlflow_main

    Example:
        To call the function `mlflow_main` located in `src/utils/mlflow_utils/create_mlflow.py`:
        python script.py src.utils.mlflow_utils.create_mlflow.mlflow_main

    Notes:
        - Ensure that the function specified can accept the configuration as an argument.
        - If the function or module cannot be found, an error message will be printed and the program will exit.
        - If no function is provided, the program will print an error message and exit.

    Raises:
        AttributeError: If the specified function cannot be found in the module.
        ModuleNotFoundError: If the specified module cannot be imported.
        Exception: For any other exceptions that occur during function call.
    """
    arg_parser = argparse.ArgumentParser(description="Main arguments")
    arg_parser.add_argument("function", help="Function to call (e.g., src.utils.mlflow_utils.create_mlflow.mlflow_main)")
    args, unknown_args = arg_parser.parse_known_args()

    config = read_config()

    if args.function is None:
        print("Function not provided!")
        sys.exit(1)

    try:
        # Get the root package dynamically
        function_path = args.function.split('.')
        module_path = '.'.join(function_path[:-1])
        function_name = function_path[-1]

        module = importlib.import_module(module_path)
        function_to_call = getattr(module, function_name)

        # Call the function with the config
        function_to_call(config)
    except (AttributeError, ModuleNotFoundError) as e:
        print(f"Error: {e}")
        print(f"Function {args.function} not found or module could not be imported")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
