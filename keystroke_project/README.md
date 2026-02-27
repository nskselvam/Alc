# Keystroke Dynamics for Early Cognitive Decline

This project simulates a system for detecting mild cognitive impairment (MCI) and early Alzheimer's disease by analyzing keystroke dynamics. It includes modules to:

- Simulate keystroke timing data (hold time, flight time, cadence variability, error rates).
- Apply a privacy layer that discards actual typed characters.
- Extract features from timing metadata.
- Train a machine learning classifier using Python (e.g., Random Forest).

This repository is purely demonstrative. In a real-world implementation, the frontend would be an Android keyboard collecting timing metadata using the `InputMethodService` API; the backend/model would run on the device and continuously adapt to the user's typing baseline.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Structure

- `data_simulator.py` – generates synthetic keystroke sessions.
- `privacy.py` – enforces privacy by stripping characters.
- `features.py` – computes features used by the classifier.
- `model.py` – trains and evaluates a classifier.
- `main.py` – example workflow.

## Usage

Run the command‑line demonstration:

```bash
python main.py
```

Launch the web interface (after installing new dependency `flask`).
Because the application uses package-relative imports, start the server from the
workspace root (the folder that contains the `keystroke_project` package).

```bash
cd ".."  # move to the directory above keystroke_project if you aren't already
python -m flask --app keystroke_project.app run
```

or equivalently:

```bash
FLASK_APP=keystroke_project.app flask run
```

Avoid running `flask` from inside the `keystroke_project` folder itself, otherwise
Python won't be able to locate the package and you'll see an ImportError.  With
the server running, open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your
browser.

Then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

The `/report` endpoint returns a JSON report suitable for programmatic
consumption, while the home page explains the idea in simple terms.



source "/Users/sudharsans/Documents/KeyStroke Dynamics/.venv/bin/activate"
python keystroke_project/main.py
