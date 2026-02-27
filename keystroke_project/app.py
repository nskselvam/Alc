from flask import Flask, jsonify, render_template, request

from .data_simulator import generate_dataset
from .privacy import apply_privacy
from .features import extract_features
from .model import KeystrokeModel

app = Flask(__name__)

# train a model once at startup so routes can use it without re-training each
# time.  In a real deployment the model would be persisted to disk after
# training and loaded on startup.

raw_data = generate_dataset(sessions=500, decline_fraction=0.15)
safe_data = apply_privacy(raw_data)
feature_data = extract_features(safe_data)
trained_model = KeystrokeModel()
trained_model.train(feature_data)


@app.route("/")
def home():
    # A very simple page explaining the idea in plain English.
    return render_template("index.html")


@app.route("/report")
def report():
    """Return evaluation metrics for the pretrained model.

    We reuse the global `trained_model` and evaluate it on a fresh batch of
    synthetic sessions so that the browser can fetch a JSON payload without
    having to retrain the classifier from scratch on every request.
    """
    # evaluate on new data so the results aren't trivially the same as the
    # training set (but this is still synthetic, so accuracy will be perfect).
    raw = generate_dataset(sessions=200, decline_fraction=0.15)
    safe = apply_privacy(raw)
    feats = extract_features(safe)

    X = feats.drop(columns=["label", "session_id"], errors="ignore")
    y = feats["label"]
    preds = trained_model.clf.predict(X)

    from sklearn.metrics import accuracy_score, classification_report

    acc = accuracy_score(y, preds)
    report_dict = classification_report(y, preds, output_dict=True)

    return jsonify({"accuracy": acc, "classification_report": report_dict})



@app.route("/predict")
def predict():
    """Simulate a single typing session and return the model's label.

    This shows how a client could ask the AI to classify one batch of keystroke
    data.  Real apps would receive actual timing metadata from the keyboard
    rather than generating it artificially.
    """
    new_session = generate_dataset(sessions=1, decline_fraction=0.0)
    new_feats = extract_features(apply_privacy(new_session))
    pred_feats = new_feats.drop(columns=["label", "session_id"], errors="ignore")
    pred = trained_model.predict(pred_feats)
    return jsonify({"prediction": pred.tolist()})


@app.route("/submit", methods=["POST"])
def submit():
    """Receive keystroke timing data from the frontend and return a label.

    Expected JSON format:
    {
        "events": [
            {"hold_time": float, "flight_time": float, "error": 0|1},
            ...
        ]
    }
    """
    payload = request.get_json(force=True)
    events = payload.get("events", [])
    if not events:
        return jsonify({"error": "no keystroke events provided"}), 400

    # build DataFrame compatible with feature extractor
    import pandas as pd
    df = pd.DataFrame(events)
    # ensure required columns exist
    required = {"hold_time", "flight_time", "error"}
    if not required.issubset(df.columns):
        return jsonify({"error": "events missing required fields"}), 400

    # compute timestamps as sequential sums; if flight_time missing treat zero
    df = df.copy()
    df["timestamp"] = df["hold_time"].cumsum() + df["flight_time"].cumsum()
    df["label"] = 0  # dummy for feature extractor
    df["session_id"] = 0
    # privacy step isn't really necessary since no chars, but keep contract
    safe = apply_privacy(df)
    feats = extract_features(safe)
    pred_feats = feats.drop(columns=["label", "session_id"], errors="ignore")
    pred = trained_model.predict(pred_feats)
    return jsonify({"prediction": pred.tolist()})


if __name__ == "__main__":
    app.run(debug=True)
