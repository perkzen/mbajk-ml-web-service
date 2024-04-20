from src.data.data_manager import DataManager

import numpy as np


def ks_test(data1, data2):
    """
    Izvede Kolmogorov-Smirnov test nad dvema vzorcema podatkov.
    Vrne vrednost testne statistike in p-vrednost.
    """
    if np.array_equal(data1, data2):
        # Če sta vzorca enaka, vrnite trivialne vrednosti
        return 0.0, 1.0
    else:
        n1 = len(data1)
        n2 = len(data2)
        data1 = np.sort(data1)
        data2 = np.sort(data2)
        cdf1 = np.searchsorted(data1, data2, side='right') / n1
        cdf2 = np.searchsorted(data2, data1, side='right') / n2
        d = np.max(np.abs(cdf1 - cdf2))
        # Izračun p-vrednosti
        p_value = 1.0 - np.exp(-2 * (d ** 2) * (n1 * n2) / (n1 + n2))
        return d, p_value


# Example usage
if __name__ == "__main__":

    dm = DataManager(data_path="data")

    current = dm.get_dataframe(folder="processed", file_name="current_data")
    reference = dm.get_dataframe(folder="processed", file_name="reference_data")

    alpha = 0.05

    for column in current.columns:
        d, p_value = ks_test(current[column], reference[column])
        if p_value < alpha:
            raise ValueError(
                f"Sprememba v porazdelitvi značilnice {column} je zaznana (p-vrednost: {p_value}). Prekinjam "
                f"izvajanje cevovoda.")
