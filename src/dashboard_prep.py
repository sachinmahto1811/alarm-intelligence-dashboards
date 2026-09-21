import argparse
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, parse_dates=["event_time"])
    df["hour"] = df["event_time"].dt.floor("h")

    kpi = (
        df.groupby(["hour", "circle", "alarm_category"], as_index=False)
        .agg(
            alarm_count=("site_id", "size"),
            unique_sites=("site_id", "nunique")
        )
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    kpi.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
