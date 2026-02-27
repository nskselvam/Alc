import pandas as pd


def apply_privacy(df: pd.DataFrame) -> pd.DataFrame:
    """Remove any sensitive information from the keystroke DataFrame.

    In our simulation we do not have characters, but in a real keyboard the
    privacy layer would discard the actual text and keep only timing metadata
    (hold_time, flight_time, coordinates if needed).
    """
    # make a shallow copy and drop columns that would contain text
    safe_df = df.copy()
    for col in ["char", "x", "y"]:
        if col in safe_df.columns:
            safe_df.drop(columns=[col], inplace=True)
    return safe_df
