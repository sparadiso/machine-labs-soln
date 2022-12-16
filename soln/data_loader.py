import pandas as pd
import numpy as np


# Some useful decorators
def operate_on_copy(fn):
    """
    Any data manipulation should be done on a fresh copy of the dataframe.
    """
    def inner(df, *args, **kwargs):
        df_copy = df.copy()
        return fn(df_copy, *args, **kwargs)

    return inner


@operate_on_copy
def clean_df(initial_df):
    """
    Clean the input dataframe.
    """

    return initial_df.copy()


@operate_on_copy
def trim_start(df, force_threshold=500):
    """
    Trim the trace to start t=0 with z-axis contact
    """

    # Don't overthink it
    skip_idx = 0
    for fz_value in df['fz_1'].to_numpy():

        # Drop the first `skip_idx` rows
        if fz_value > force_threshold:
            t0 = df.loc[skip_idx, 't']
            df.loc[:, 't'] -= t0

            return df.iloc[skip_idx:]

        skip_idx += 1

    assert False, "trim_start couldn't find the start of the build!"


@operate_on_copy
def trim_end(df, force_threshold=50):
    """
    Trim the trace to end with the last z-axis pullback
    """

    # Don't overthink it
    fz_np = df['fz_1'].to_numpy()
    for i in range(1, len(fz_np)):
        fz_value = fz_np[-i]

        # Drop the last `i` rows
        if fz_value > force_threshold:
            return df.iloc[:-i]

    assert False, "trim_end couldn't find the end of the build!"


@operate_on_copy
def add_force_magnitudes(df):
    """
    Add a column for |<fx, fy, fz>| (both R1 and R2).
    """

    for idx in [1, 2]:
        x = df[f"fx_{idx}"]
        y = df[f"fy_{idx}"]
        z = df[f"fz_{idx}"]

        df[f"f{idx}_magnitude"] = (x*x + y*y + z*z).map(np.sqrt)

    return df


def load_data(csv_fname, clean=False):
    """
    Load in csv data to a pandas dataframe, clean it, and (optionally)
    add any enrichments that shouldn't be part of the modeling pipeline.
    """

    df = pd.read_csv(csv_fname)

    if not clean:
        return df

    cleaned = df.pipe(trim_start)\
                .pipe(trim_end)\
                .pipe(add_force_magnitudes)

    return cleaned
