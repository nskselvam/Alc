from flask import Flask, jsonify, render_template, request
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np
import pandas as pd

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
    
    # Get prediction and probability
    pred = trained_model.predict(pred_feats)
    proba = trained_model.predict_proba(pred_feats)
    
    # Return comprehensive results
    return jsonify({
        "prediction": int(pred[0]),
        "probability_decline": float(proba[0][1]),  # probability of class 1 (decline)
        "probability_healthy": float(proba[0][0]),  # probability of class 0 (healthy)
        "features": {
            "hold_mean": float(pred_feats["hold_mean"].iloc[0]),
            "hold_std": float(pred_feats["hold_std"].iloc[0]),
            "flight_mean": float(pred_feats["flight_mean"].iloc[0]),
            "flight_std": float(pred_feats["flight_std"].iloc[0]),
            "error_rate": float(pred_feats["error_rate"].iloc[0]),
            "n_keys": int(pred_feats["n_keys"].iloc[0])
        }
    })


@app.route("/graphs")
def graphs():
    """Generate and return visualization graphs comparing good and bad datasets."""
    # Generate good (healthy) and bad (cognitive decline) datasets
    good_data = generate_dataset(sessions=100, decline_fraction=0.0)
    bad_data = generate_dataset(sessions=100, decline_fraction=1.0)
    
    # Extract features
    good_feats = extract_features(apply_privacy(good_data))
    bad_feats = extract_features(apply_privacy(bad_data))
    
    # Add labels for plotting
    good_feats['Dataset'] = 'Healthy Pattern'
    bad_feats['Dataset'] = 'Cognitive Decline'
    
    combined = pd.concat([good_feats, bad_feats], ignore_index=True)
    
    # Create distribution graph
    fig1, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig1.suptitle('Good vs Bad Typing Patterns Distribution', fontsize=16, fontweight='bold')
    
    sns.histplot(data=combined, x='hold_mean', hue='Dataset', kde=True, ax=axes[0,0])
    axes[0,0].set_title('Hold Time Mean Distribution')
    axes[0,0].set_xlabel('Hold Time (ms)')
    
    sns.histplot(data=combined, x='flight_mean', hue='Dataset', kde=True, ax=axes[0,1])
    axes[0,1].set_title('Flight Time Mean Distribution')
    axes[0,1].set_xlabel('Flight Time (ms)')
    
    sns.histplot(data=combined, x='hold_std', hue='Dataset', kde=True, ax=axes[1,0])
    axes[1,0].set_title('Hold Time Variability')
    axes[1,0].set_xlabel('Standard Deviation (ms)')
    
    sns.histplot(data=combined, x='error_rate', hue='Dataset', kde=True, ax=axes[1,1])
    axes[1,1].set_title('Error Rate Distribution')
    axes[1,1].set_xlabel('Error Rate')
    
    plt.tight_layout()
    
    # Convert to base64
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', dpi=100, bbox_inches='tight')
    buf1.seek(0)
    img1_base64 = base64.b64encode(buf1.read()).decode('utf-8')
    plt.close()
    
    # Create feature comparison graph
    fig2, ax = plt.subplots(figsize=(10, 6))
    
    features_to_plot = ['hold_mean', 'flight_mean', 'hold_std', 'flight_std', 'error_rate']
    good_means = [good_feats[f].mean() for f in features_to_plot]
    bad_means = [bad_feats[f].mean() for f in features_to_plot]
    
    x = np.arange(len(features_to_plot))
    width = 0.35
    
    ax.bar(x - width/2, good_means, width, label='Healthy Pattern', color='#4caf50', alpha=0.8)
    ax.bar(x + width/2, bad_means, width, label='Cognitive Decline', color='#f44336', alpha=0.8)
    
    ax.set_xlabel('Features', fontweight='bold')
    ax.set_ylabel('Average Value', fontweight='bold')
    ax.set_title('Feature Comparison: Healthy vs Cognitive Decline', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['Hold Time\nMean', 'Flight Time\nMean', 'Hold Time\nVariability', 
                        'Flight Time\nVariability', 'Error Rate'])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', dpi=100, bbox_inches='tight')
    buf2.seek(0)
    img2_base64 = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close()
    
    return jsonify({
        "distribution_graph": f"data:image/png;base64,{img1_base64}",
        "feature_comparison": f"data:image/png;base64,{img2_base64}"
    })


if __name__ == "__main__":
    app.run(debug=True, port=8080)
