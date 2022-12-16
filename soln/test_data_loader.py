from soln.data_loader import load_data


def test_load_csv_df():
    """
    Basic data loader tests.
    """

    df = load_data("Test1.csv", False)

    # Make sure nothing has shifted under our feet wrt the Test1.csv input
    assert len(df.index) == 20091, \
        "Expected 20091 rows, got {}".format(len(df.index))


def test_clean_and_enrich():
    df = load_data("Test1.csv", True)

    # Make sure nothing has shifted under our feet wrt the Test1.csv input
    # This is sensitive to the thresholds used in trim_start/trim_end
    assert len(df.index) == 19848, \
        "Expected 19848 rows, got {}".format(len(df.index))

    # Make sure the trace is trimmed
    assert df.iloc[0]['fz_1'] > 500
    assert df.iloc[-1]['fz_1'] > 50

    # Make sure we have the total magnitude columns we expect
    assert "f1_magnitude" in df.columns and "f2_magnitude" in df.columns, \
        "Missing force magnitude columns"
