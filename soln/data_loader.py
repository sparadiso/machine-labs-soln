import pandas as pd

from soln.features import operate_on_copy
from soln.features import add_deformation_force
from soln.features import add_space_derivatives
from soln.features import add_force_magnitudes
from soln.features import add_arm_distance


def load(csv_fname, raw=False):
    """
    Load a csv data file, clean it, and add all features.
    """

    df = pd.read_csv(csv_fname)

    if raw:
        return df

    return df.pipe(trim_start)\
             .pipe(trim_end)\
             .pipe(add_force_magnitudes)\
             .pipe(add_space_derivatives)\
             .pipe(add_deformation_force)\
             .pipe(add_arm_distance)


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
