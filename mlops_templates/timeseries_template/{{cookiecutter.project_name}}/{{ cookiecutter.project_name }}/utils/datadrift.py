import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, ttest_ind, chisquare
import json
import warnings
from typing import Dict, Optional
import mlflow
from scipy import stats
# Suppress FutureWarnings to avoid clutter in output
warnings.filterwarnings("ignore", category=FutureWarning)

# Define Drift Detection Functions for Numerical and Categorical Columns

# Numerical Tests
def ks_stat_test(reference, target):
    """
    Performs the Kolmogorov-Smirnov test to compare the distributions of two samples.

    Args:
    - reference (pd.Series): Reference data sample.
    - target (pd.Series): Current data sample.

    Returns:
    - p_value (float): The p-value of the test.
    """
    statistic, p_value = ks_2samp(reference, target)
    return p_value

def t_test(reference, target):
    """
    Performs the t-test to compare the means of two samples.

    Args:
    - reference (pd.Series): Reference data sample.
    - target (pd.Series): Current data sample.

    Returns:
    - p_value (float): The p-value of the test.
    """
    _, p_value = ttest_ind(reference, target, equal_var=False)  # Welch's t-test
    return p_value

# Categorical Tests
def chi_square_test(reference, target):
    """
    Performs the Chi-square test for categorical data to compare observed and expected frequencies.

    Args:
    - reference (pd.Series): Reference data sample.
    - target (pd.Series): Current data sample.

    Returns:
    - p_value (float): The p-value of the test.
    """
    keys = list(set(reference) | set(target))
    ref_feature_dict = {key: reference.value_counts().get(key, 0) for key in keys}
    current_feature_dict = {key: target.value_counts().get(key, 0) for key in keys}
    k_norm = len(target) / len(reference)
    observed = [current_feature_dict[key] for key in keys]
    expected = [ref_feature_dict[key] * k_norm for key in keys]
    chi2_stat, p_value = stats.chisquare(observed, f_exp=expected)
    return p_value

# Mapping of test names to their corresponding functions
numerical_tests = {
    'ks_stat_test': ks_stat_test,
    't_test': t_test
}

categorical_tests = {
    'chi_square_test': chi_square_test
}

# Combine numerical and categorical tests into a single dictionary
test_functions = {**numerical_tests, **categorical_tests}

def detect_drift(reference: pd.DataFrame, current: pd.DataFrame, drift_params: Optional[Dict[str, Dict[str, float]]] = None) -> Dict[str, dict]:
    """
    Detects data drift by applying statistical tests to columns in reference and current dataframes.

    Args:
    - reference (pd.DataFrame): The reference dataset.
    - current (pd.DataFrame): The current dataset to compare against.
    - drift_params (Optional[Dict[str, Dict[str, float]]]): A dictionary specifying which tests to apply to which columns, along with thresholds.

    Returns:
    - drift_results (Dict[str, dict]): A dictionary containing the results of the drift detection tests.
    """
    drift_results = {}

    # Determine column types in the reference DataFrame
    column_types = reference.dtypes.to_dict()

    # If no specific tests are provided, apply default tests
    if drift_params is None:
        drift_params = {}
        # Apply all numerical tests to numerical columns
        for col, dtype in column_types.items():
            if np.issubdtype(dtype, np.number):
                drift_params[col] = [{'test': test_name, 'threshold': 0.05} for test_name in numerical_tests.keys()]
            else:
                drift_params[col] = [{'test': test_name, 'threshold': 0.05} for test_name in categorical_tests.keys()]

    # Perform drift detection
    for column, tests in drift_params.items():
        if column in column_types:
            reference_column = reference[column]
            current_column = current[column]
            column_results = {}

            for test in tests:
                test_name = test['test']
                threshold = test['threshold']
                test_func = test_functions.get(test_name)

                if test_func:
                    # Perform the test and determine if drift is detected
                    p_value = test_func(reference_column, current_column)
                    drift_detected = p_value < threshold

                    # Store the test results
                    column_results[test_name] = {
                        'p_value': p_value,
                        'drift_detected': bool(drift_detected)  # Convert to native Python bool
                    }

            # Store results for the column
            drift_results[column] = column_results

    return drift_results

# Example Usage
if __name__ == "__main__":

    # Run drift detection tests
    drift_params = {
        'Sales': [{'test': 'ks_stat_test', 'threshold': 0.05}, {'test': 't_test', 'threshold': 0.05}],
        'Category': [{'test': 'g_test', 'threshold': 0.05}, {'test': 'chi_square_test', 'threshold': 0.05}]
    }
    drift_results = detect_drift(reference_df, current_df,drift_params)
    print(drift_results_df)

