import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib


class KeystrokeModel:
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, features: pd.DataFrame):
        """Train the classifier on extracted features."""
        X = features.drop(columns=["label", "session_id"], errors="ignore")
        y = features["label"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        self.clf.fit(X_train, y_train)
        preds = self.clf.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, preds))
        print(classification_report(y_test, preds))

    def predict(self, feature_vector: pd.DataFrame) -> np.ndarray:
        """Return class predictions for given feature vectors."""
        return self.clf.predict(feature_vector)

    def predict_proba(self, feature_vector: pd.DataFrame) -> np.ndarray:
        """Return probability estimates for each class."""
        return self.clf.predict_proba(feature_vector)

    def save(self, path: str):
        joblib.dump(self.clf, path)

    def load(self, path: str):
        self.clf = joblib.load(path)
