import pytest
import os, sys
# ensure workspace root is on path so package imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from keystroke_project.data_simulator import generate_dataset
from keystroke_project.privacy import apply_privacy
from keystroke_project.features import extract_features
from keystroke_project.model import KeystrokeModel


def test_end_to_end():
    df = generate_dataset(sessions=50, decline_fraction=0.2)
    safe = apply_privacy(df)
    feats = extract_features(safe)
    assert not feats.empty
    model = KeystrokeModel()
    model.train(feats)
    preds = model.predict(feats.drop(columns=["label"], errors="ignore"))
    assert len(preds) == len(feats)
