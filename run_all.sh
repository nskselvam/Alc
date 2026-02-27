#!/usr/bin/env bash
# convenience script to set up and launch the keystroke dynamics demo
# usage: ./run_all.sh

set -euo pipefail

# ensure we run from the workspace root
cd "$(dirname "$0")"

# create/activate virtual environment
if [ ! -d ".venv" ]; then
    echo "creating virtual environment..."
    python3 -m venv .venv
fi

# shellcheck disable=SC1091
source ".venv/bin/activate"

# install dependencies (requirements.txt lists flask etc.)
python -m pip install --upgrade pip
python -m pip install -r keystroke_project/requirements.txt pytest

# run the test suite to reassure everything works
echo "running tests..."
python -m pytest -q

echo "starting Flask web server (use Ctrl-C to quit)..."
# start from workspace root so package-relative imports resolve
FLASK_APP=keystroke_project.app flask run
