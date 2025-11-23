import os
import pandas as pd
import numpy as np


def load_and_process_data(csv_path=None):
    """Load CSV, create a `status` column from delays, and return (summary, df).

    - Tries these files (in order): provided csv_path, data/input.csv, data/flights.csv
    - Uses `dep_delay` to determine status (Delayed / On Time / Unknown)
    """
    base = os.path.dirname(__file__)

    candidates = []
    if csv_path:
        candidates.append(csv_path)
    candidates.append(os.path.join(base, "data", "input.csv"))
    candidates.append(os.path.join(base, "data", "flights.csv"))

    found = None
    for p in candidates:
        if p and os.path.exists(p):
            found = p
            break
    if not found:
        raise FileNotFoundError(
            f"No CSV found. Tried: {candidates}. Provide a valid path."
        )

    df = pd.read_csv(found)

    # Normalize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # If dep_delay exists but has missing values, coerce to numeric
    if "dep_delay" in df.columns:
        df["dep_delay"] = pd.to_numeric(df["dep_delay"], errors="coerce")
    else:
        # try arr_delay as fallback
        if "arr_delay" in df.columns:
            df["dep_delay"] = pd.to_numeric(df["arr_delay"], errors="coerce")
        else:
            # create a dep_delay column of NaNs
            df["dep_delay"] = np.nan

    # Create status column safely
    def status_from_delay(x):
        if pd.isna(x):
            return "Unknown"
        try:
            # treat floats/ints
            return "Delayed" if float(x) > 0 else "On Time"
        except Exception:
            return "Unknown"

    df["status"] = df["dep_delay"].apply(status_from_delay)

    # Fill certain string columns with 'Unknown' without touching numeric columns
    for col in df.select_dtypes(include=[object]).columns:
        df[col] = df[col].fillna("Unknown")

    # Summary statistics
    total = len(df)
    delayed = int((df["status"] == "Delayed").sum())
    on_time = int((df["status"] == "On Time").sum())
    unknown = int((df["status"] == "Unknown").sum())
    average_delay = float(df["dep_delay"].dropna().mean()) if df["dep_delay"].dropna().size > 0 else None

    # top origins and top carriers (if available)
    top_origins = df["origin"].value_counts().head(5).to_dict() if "origin" in df.columns else {}
    top_carriers = df["carrier"].value_counts().head(5).to_dict() if "carrier" in df.columns else {}

    summary = {
        "total_flights": total,
        "delayed_flights": delayed,
        "on_time_flights": on_time,
        "unknown_status": unknown,
        "average_delay_minutes": average_delay,
        "top_origins": top_origins,
        "top_carriers": top_carriers,
        "sample_rows": df.head(5).to_dict(orient="records")
    }

    return summary, df


if __name__ == "__main__":
    # quick test when run directly
    import pprint
    s, _ = load_and_process_data()
    pprint.pprint(s)