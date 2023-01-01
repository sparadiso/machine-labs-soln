import numpy as np


def operate_on_copy(fn):
    """
    Any data manipulation should be done on a fresh copy of the dataframe.
    """

    def inner(df, *args, **kwargs):
        df_copy = df.copy()
        return fn(df_copy, *args, **kwargs)

    return inner


@operate_on_copy
def add_space_derivatives(df, fields=['x_enc_1', 'y_enc_1', 'z_enc_1']):
    """
    Compute derivatives and add as a new column
    in the dataframe (col name simply prepended with 'd').
    """

    def avg_gradient(x):
        i0, i1 = x.index[0], x.index[1]
        return (x[i1] - x[i0]) / (len(x) - 1.0)

    for field in fields:
        df['d' + field] = df[field].rolling(2).apply(avg_gradient)

    # Trim the first row (with no gradient information)
    return df.iloc[1:]


@operate_on_copy
def add_arm_distance(df, fields=['x_enc_1', 'y_enc_1', 'z_enc_1']):
    """
    Add a feature for the x, y, and z distance between the robot arms
    at each time step.
    """

    for x in ['x', 'y', 'z']:
        df['R12_d' + x] = df['{}_enc_1'.format(x)] - df['{}_enc_2'.format(x)]

    return df


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


@operate_on_copy
def add_deformation_force(df):
    """
    Add a column for the R1 + R2 force (negate the opposing robot force).
    """

    for coord in ['x', 'y', 'z']:
        df[f"f{coord}_deformation"] = df[f"f{coord}_1"] + df[f"f{coord}_2"]

    return df
