# Ingestion Module

The Ingestion module is responsible for reading, preprocessing, and saving data. It includes scripts to handle data ingestion and preprocessing tasks, ensuring data is ready for further analysis and modeling.

## Structure

The module contains the following scripts:

1. **ingest.py**: Contains functions to read data from files into pandas DataFrames.
2. **preprocess.py**: Contains functions to preprocess data, including removing duplicates, preprocessing time series data for the dashboard, and saving preprocessed data.

## Usage

To use the functions in this module, ensure you have the necessary configuration file (config.yml) with the appropriate settings for data paths.

- **Read Data**: Use the read_data function from ingest.py to read data from a CSV file.
- **Preprocess Data**: Use the functions in preprocess.py to preprocess the data. This includes removing duplicates and preparing time series data for the dashboard.
- **Main Ingestion**: Use the main_ingestion function to execute the complete ingestion and preprocessing pipeline.