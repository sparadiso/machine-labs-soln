from soln.data_loader import load_data

def test_load_csv_df():
    df = load_data("Test1.csv")

    # Make sure nothing has shifted under our feet wrt the Test1.csv input
    assert len(df.index) == 20091, "Expected 20091 rows, got {}".format(len(df.index))
