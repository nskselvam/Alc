import pandas as pd


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Given a keystroke DataFrame for a session, compute feature summary.

    Features include mean/var of hold/flight times, error frequency, and
    inter-key interval variability.
    The input DataFrame is expected to have columns: hold_time, flight_time,
    error, session_id, label.
    """
    grouped = df.groupby("session_id")

    features = grouped.agg(
        hold_mean=("hold_time", "mean"),
        hold_std=("hold_time", "std"),
        flight_mean=("flight_time", "mean"),
        flight_std=("flight_time", "std"),
        error_rate=("error", "mean"),
        n_keys=("hold_time", "count"),
        label=("label", "first"),
    )
    features.fillna(0, inplace=True)
    return features.reset_index(drop=True)
