import pandas as pd


def load_data(csv_fname):
    """
    Load in csv test data to a pandas dataframe.
    """

    return pd.read_csv(csv_fname)


def clean_df(initial_df):
    """
    Clean the input dataframe.
    """

    return initial_df
