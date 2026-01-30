import pandas as pd
import zipfile

zip_path = "H:/GitHub/dashboard_demo/output/cleaned_data.zip"
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    csv_filename = "cleaned_data.csv"
    with zip_ref.open(csv_filename) as f:
        df = pd.read_csv(f, index_col=0, nrows=10)
        print("Columns:", len(df.columns))
        print("\nShape:", df.shape)
        print("\nEventCount in columns:", "EventCount" in df.columns)
        if "EventCount" in df.columns:
            print("EventCount values:", df["EventCount"].tolist())
            print("EventCount dtype:", df["EventCount"].dtype)
        else:
            print("EventCount NOT FOUND!")
            print("Available columns:", df.columns.tolist())
