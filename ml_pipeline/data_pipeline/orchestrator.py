import pandas as pd
import json
from .config import OUTPUT_PARQUET, SUMMARY_JSON

def save_outputs(records):
    df = pd.DataFrame(records)

    # Save as Parquet
    df.to_parquet(OUTPUT_PARQUET, index=False)
    print("Saved:", OUTPUT_PARQUET)

    # Generate extended summary
    summary = {
        "total_files": len(df),
        "total_duration_sec": round(df["duration_sec"].sum(), 2),
        "average_duration_sec": round(df["duration_sec"].mean(), 2),
        "sampling_rate_distribution": df["sampling_rate"].value_counts().to_dict(),
        "transcription_lengths": {
            "min": df["transcription"].str.len().min(),
            "max": df["transcription"].str.len().max(),
            "avg": round(df["transcription"].str.len().mean(), 2)
        },
        "token_counts": {
            "min": df["tokens"].apply(len).min(),
            "max": df["tokens"].apply(len).max(),
            "avg": round(df["tokens"].apply(len).mean(), 2)
        }
    }

    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=4)

    print("Summary saved to", SUMMARY_JSON)
    print(json.dumps(summary, indent=4))
