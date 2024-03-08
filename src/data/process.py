from scipy.stats import boxcox
from matplotlib import pyplot as plt
import seaborn as sns


def boxcox_transform(df,column):
    # create before and after plots for comparison
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Before Box-Cox
    sns.histplot(df[column], ax=ax[0], kde=True)
    ax[0].set_title("Before Box-Cox")

    # transform data
    data, _ = boxcox(df[column])

    # After Box-Cox
    sns.histplot(data, ax=ax[1], kde=True)
    ax[1].set_title("After Box-Cox")

    # update dataframe
    df[column] = data

    plt.show()