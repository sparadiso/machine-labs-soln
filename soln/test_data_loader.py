from soln.data_loader import load


def test_load_csv_df():
    """
    Basic data loader tests.
    """

    df = load("Test1.csv", raw=True)

    # Make sure nothing has shifted under our feet wrt the Test1.csv input
    assert len(df.index) == 20091, \
        "Expected 20091 rows, got {}".format(len(df.index))


def test_clean_and_enrich():
    df = load("Test1.csv")

    # Make sure nothing has shifted under our feet wrt the Test1.csv input
    # This is sensitive to the thresholds used in trim_start/trim_end
    assert len(df.index) == 19847, \
        "Expected 19847 rows, got {}".format(len(df.index))

    # Make sure the trace is trimmed
    assert df.iloc[0]['fz_1'] > 500
    assert df.iloc[-1]['fz_1'] > 50

    # Make sure we have the total magnitude columns we expect
    assert "f1_magnitude" in df.columns and "f2_magnitude" in df.columns, \
        "Missing force magnitude columns"

    # Make sure we have the derivative columns we expect
    assert all([f"d{x}_enc_1" in df.columns for x in ['x', 'y', 'z']]), \
        "Missing derivative columns"
