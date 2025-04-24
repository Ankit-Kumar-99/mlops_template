from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession
from {{ cookiecutter.project_name }}.tests import main

# Create a new Databricks Connect session. If this fails,
# check that you have configured Databricks Connect correctly.
# See https://docs.databricks.com/dev-tools/databricks-connect.html.

SparkSession.builder = DatabricksSession.builder
SparkSession.builder.getOrCreate()

def test_main():
    """
    Test function to validate the get_taxis function.

    This function serves as a test to validate that the `get_taxis` function from
    the `{{ cookiecutter.project_name }}.src.tests.main` module is working correctly. It retrieves
    the taxi data using the `get_taxis` function and asserts that the count of the
    retrieved data is greater than 5.

    Usage:
    Call this function to run the test and validate the `get_taxis` function. The
    function uses Databricks Connect to create a Spark session and then performs
    the test.

    Example:
        def test_main():
            taxis = main.get_taxis()
            assert taxis.count() > 5

    Note:
    Ensure that Databricks Connect is configured correctly before running this function.
    If the Databricks Connect session fails to initialize, check the configuration
    according to the Databricks Connect documentation:
    https://docs.databricks.com/dev-tools/databricks-connect.html

    If running as a script, the function will be executed automatically.

    Example usage as a script:
        if __name__ == "__main__":
            test_main()
    """
    taxis = main.get_taxis()
    assert taxis.count() > 5

if __name__ == "__main__":
    test_main()
