import pandas as pd
import json

def save_outputs(records):
    df = pd.DataFrame(records)
    df.to_parquet("metavoice_output.parquet", index=False)
    print("Saved output to metavoice_output.parquet")