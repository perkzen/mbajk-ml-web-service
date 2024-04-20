import numpy as np

from src.data.data_manager import DataManager


def ks_test(data1, data2):
    """
    Performs the Kolmogorov-Smirnov test between two samples.
    Returns the test statistic value and the p-value.
    """
    if np.array_equal(data1, data2):
        # If the samples are equal, return trivial values
        return 0.0, 1.0
    else:
        # Calculate the cumulative distribution functions
        hist1, bin_edges1 = np.histogram(data1, bins=100, density=True)
        hist2, bin_edges2 = np.histogram(data2, bins=100, density=True)
        cdf1 = np.cumsum(hist1 * np.diff(bin_edges1))
        cdf2 = np.cumsum(hist2 * np.diff(bin_edges2))
        d = np.max(np.abs(cdf1 - cdf2))
        # Calculate the p-value using an approximation
        p_value = 1.0 - np.exp(-2 * (d ** 2))
        return d, p_value


# Example usage
if __name__ == "__main__":
    # Assume DataManager is properly defined
    dm = DataManager(data_path="data")

    current = dm.get_dataframe(folder="processed", file_name="current_data")
    reference = dm.get_dataframe(folder="processed", file_name="reference_data")

    alpha = 0.1

    for column in current.columns:
        d, p_value = ks_test(current[column], reference[column])
        if p_value < alpha:
            print(
                f"Change in the distribution of column {column} is detected (p-value: {p_value}). Stopping the pipeline."
            )
