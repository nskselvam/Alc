import numpy as np
import pandas as pd


def simulate_session(num_keys: int = 100, cognitive_decline: bool = False) -> pd.DataFrame:
    """Generate synthetic keystroke timing data for a single typing session.

    Args:
        num_keys: number of keystrokes in the session.
        cognitive_decline: if True, simulate longer hold/flight times and more variability.

    Returns:
        DataFrame with columns [`hold_time`, `flight_time`, `timestamp`, `error`].
    """
    # baseline distributions (milliseconds)
    hold_mu, hold_sigma = (100, 30) if not cognitive_decline else (180, 80)
    flight_mu, flight_sigma = (80, 20) if not cognitive_decline else (150, 60)

    # generate timings
    hold_times = np.abs(np.random.normal(hold_mu, hold_sigma, num_keys))
    flight_times = np.abs(np.random.normal(flight_mu, flight_sigma, num_keys))

    # generate timestamps for event sequence
    timestamps = np.cumsum(np.concatenate([[0], hold_times[:-1] + flight_times[:-1]]))

    # simulate error occurrences (backspaces)
    error_rate = 0.02 if not cognitive_decline else 0.08
    errors = np.random.rand(num_keys) < error_rate

    df = pd.DataFrame({
        "hold_time": hold_times,
        "flight_time": flight_times,
        "timestamp": timestamps,
        "error": errors.astype(int),
    })
    return df


def generate_dataset(sessions: int = 500, decline_fraction: float = 0.1) -> pd.DataFrame:
    """Create a labeled dataset with multiple simulated sessions.

    The label 0 indicates healthy baseline; 1 indicates cognitive decline behavior.
    """
    data = []
    num_decline = int(sessions * decline_fraction)
    for i in range(sessions):
        is_decline = i < num_decline
        df = simulate_session(cognitive_decline=is_decline)
        df["label"] = int(is_decline)
        df["session_id"] = i
        data.append(df)
    return pd.concat(data, ignore_index=True)
