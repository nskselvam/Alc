"""Example workflow simulating keystroke dynamics analysis."""
from data_simulator import generate_dataset
from privacy import apply_privacy
from features import extract_features
from model import KeystrokeModel


def main():
    # 1. Simulate data collection
    raw = generate_dataset(sessions=1000, decline_fraction=0.15)

    # 2. Apply privacy (strip any text columns)
    safe = apply_privacy(raw)

    # 3. Extract session-level features
    feats = extract_features(safe)
    print("Feature dataframe sample:")
    print(feats.head())

    # 4. Train classifier
    model = KeystrokeModel()
    model.train(feats)

    # Optionally save model for on-device inference
    model.save("keystroke_model.joblib")

    # 5. Example prediction on new simulated session
    new_session = generate_dataset(sessions=1, decline_fraction=0.0)
    new_feats = extract_features(apply_privacy(new_session))

    # drop label (present in simulation) so feature names align with training
    pred_feats = new_feats.drop(columns=["label"], errors="ignore")
    print("Predicted label for fresh session:", model.predict(pred_feats))


if __name__ == "__main__":
    main()
