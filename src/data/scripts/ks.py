import math

from src.data.data_manager import DataManager


def ks_test(datalist1, datalist2):
    n1 = len(datalist1)
    n2 = len(datalist2)
    datalist1.sort()
    datalist2.sort()

    j1 = 0
    j2 = 0
    d = 0.0
    fn1 = 0.0
    fn2 = 0.0
    while j1 < n1 and j2 < n2:
        d1 = datalist1[j1]
        d2 = datalist2[j2]
        if d1 <= d2:
            fn1 = (float(j1) + 1.0) / float(n1)
            j1 += 1
        if d2 <= d1:
            fn2 = (float(j2) + 1.0) / float(n2)
            j2 += 1
        dtemp = math.fabs(fn2 - fn1)
        if dtemp > d:
            d = dtemp

    ne = float(n1 * n2) / float(n1 + n2)
    nesq = math.sqrt(ne)
    prob = ks_prob((nesq + 0.12 + 0.11 / nesq) * d)
    return d, prob, ne


def ks_prob(alam):
    fac = 2.0
    sum = 0.0
    termbf = 0.0

    a2 = -2.0 * alam * alam
    for j in range(1, 101):
        term = fac * math.exp(a2 * j * j)
        sum += term
        if math.fabs(term) <= 0.001 * termbf or math.fabs(term) <= 1.0e-8 * sum:
            return sum
        fac = -fac
        termbf = math.fabs(term)

    return 1.0


# Example usage
if __name__ == "__main__":
    # Assume DataManager is properly defined
    dm = DataManager(data_path="data")

    current = dm.get_dataframe(folder="processed", file_name="current_data")
    reference = dm.get_dataframe(folder="processed", file_name="reference_data")

    alpha = 0.1

    for column in current.columns:
        current_data = current[column].tolist()
        reference_data = reference[column].tolist()

        # Perform the Kolmogorov-Smirnov test
        d, prob, ne = ks_test(current_data, reference_data)

        # Decide based on the significance level
        if prob < alpha:
            print(f"Column '{column}': D = {d}, Prob = {prob}. Distribution significantly different.")
            raise ValueError(f"Column '{column}': D = {d}, Prob = {prob}. Distribution significantly different.")
        else:
            print(f"Column '{column}': D = {d}, Prob = {prob}. Distribution not significantly different.")
