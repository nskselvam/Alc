# Keystroke Dynamics Typing Test - AI-Powered Cognitive Health Analysis

## 🎯 Project Overview

This is an advanced typing test that uses Machine Learning to analyze keystroke dynamics for potential cognitive health monitoring. Unlike traditional typing tests that only measure speed and accuracy, this application analyzes the subtle patterns in how you type to detect potential early signs of cognitive decline.

## 🧠 How It Works

The application captures your typing patterns and analyzes them using a **Random Forest Classifier** - a sophisticated machine learning algorithm that combines multiple decision trees to make accurate predictions.

### Features Analyzed

1. **Hold Time**: How long each key is pressed (milliseconds)
2. **Flight Time**: Time between releasing one key and pressing the next
3. **Error Rate**: Frequency of backspaces and corrections
4. **Typing Variability**: Consistency in your typing rhythm

### The Al Algorithm: Random Forest

- **Type**: Ensemble Learning Method
- **Model Configuration**: 100 decision trees
- **Training Data**: 500+ sessions with both healthy and cognitive-decline patterns
- **Accuracy**: Evaluated on test data with detailed classification reports

## ✨ Key Features

### 1. Interactive Typing Test
- Text is displayed above (like a WPM test)
- Real-time character-by-character comparison
- Visual feedback (green for correct, red for incorrect)
- Current position highlighted

### 2. Real-Time Statistics
- **Words Per Minute (WPM)**: Measures typing speed
- **Accuracy**: Percentage of correctly typed characters
- **Keys Pressed**: Total keystroke count
- **Time Elapsed**: Test duration

### 3. Two ML Outputs

**Output 1: Classification**
- Binary prediction: "Healthy Pattern" or "Potential Decline Detected"
- Based on comprehensive feature analysis

**Output 2: Confidence Score**
- Probability percentage showing decline risk
- Visual progress bar indicating confidence level
- Ranges from 0% (healthy) to 100% (high decline risk)

### 4. Dataset Visualization

**Graph 1: Good vs Bad Typing Patterns**
- Distribution histograms comparing healthy and decline patterns
- Shows clear differences in:
  - Hold time means
  - Flight time means
  - Variability measures
  - Error rates

**Graph 2: Feature Comparison**
- Bar chart comparing average values
- Side-by-side comparison of healthy vs decline patterns
- All 5 key features displayed

### 5. Detailed Pattern Analysis
- Average hold time with millisecond precision
- Hold time variability (standard deviation)
- Average flight time
- Flight time variability
- Error rate percentage
- Total keystrokes analyzed

## 🚀 Installation & Setup

### Prerequisites
- Python 3.14+ (or Python 3.7+)
- Virtual environment (recommended)

### Installation Steps

1. **Navigate to the project directory**
```bash
cd "KeyStroke Dynamics"
```

2. **Activate virtual environment**
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r keystroke_project/requirements.txt
```

### Required Packages
- flask - Web framework
- numpy - Numerical computations
- pandas - Data manipulation
- scikit-learn - Machine learning
- matplotlib - Graph generation
- seaborn - Statistical visualizations

## 🎮 Usage

### Starting the Application

```bash
cd keystroke_project
python -m flask --app app run
```

Or use the provided script:
```bash
./run_all.sh
```

### Using the Typing Test

1. **Open your browser** and go to `http://127.0.0.1:8080`

2. **Read the text** displayed in the orange box

3. **Click the input field** and start typing the text exactly as shown

4. **Watch real-time stats** update as you type:
   - WPM (Words Per Minute)
   - Accuracy percentage
   - Key count
   - Time elapsed

5. **Click "Analyze My Typing Pattern"** when done to get ML analysis:
   - Classification result (Healthy/Decline)
   - Confidence score with visual bar
   - Detailed pattern metrics

6. **Click "Show Dataset Graphs"** to see:
   - Good vs Bad typing pattern distributions
   - Feature comparison charts

7. **Click "Get Model Report"** for detailed model performance metrics

8. **Click "Reset Test"** to start over

## 📊 Understanding the Results

### Classification Output
- **Healthy Pattern**: Your typing rhythm matches normal patterns
- **Potential Decline Detected**: Patterns suggest further evaluation may be needed

### Confidence Score
- **0-30%**: Strong healthy pattern
- **30-70%**: Intermediate/unclear pattern
- **70-100%**: Strong decline indicators

⚠️ **Important**: This is a demonstration tool and should NOT be used for medical diagnosis. Always consult healthcare professionals for medical concerns.

## 🔬 Technical Details

### Data Flow

1. **Keystroke Capture**
   - JavaScript captures keydown/keyup events
   - Records precise timing (performance.now())
   - Tracks hold time, flight time, and errors

2. **Privacy Protection**
   - Only timing data is recorded
   - Actual text typed is never sent to server
   - Privacy module strips any text content

3. **Feature Extraction**
   - Calculates statistical features per session
   - Mean, standard deviation, error rate
   - Session-level aggregation

4. **ML Prediction**
   - Random Forest classifier processes features
   - Returns binary prediction (0=healthy, 1=decline)
   - Provides probability estimates for both classes

5. **Visualization**
   - Generates datasets on-demand
   - Creates matplotlib/seaborn graphs
   - Converts to base64 for web display

### File Structure

```
keystroke_project/
├── __init__.py           # Package initialization
├── app.py                # Flask web application
├── data_simulator.py     # Synthetic data generation
├── features.py           # Feature extraction logic
├── model.py              # Random Forest classifier
├── privacy.py            # Privacy protection module
├── main.py               # Command-line workflow
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface (typing test)
└── tests/
    ├── test_web.py       # Web endpoint tests
    └── test_workflow.py  # Workflow tests
```

## 🧪 Testing

Run the test workflow:
```bash
python -m keystroke_project.main
```

Run web tests:
```bash
python -m pytest keystroke_project/tests/
```

## 🎨 Design Features

- **Modern gradient UI** with purple theme
- **Responsive layout** adapts to all screen sizes
- **Real-time visual feedback** for typing
- **Animated statistics** with smooth transitions
- **Professional graphs** with clear labeling
- **Accessibility-friendly** color schemes

## 🔐 Privacy & Ethics

- **No personal data collection**: Only timing information
- **No text recording**: Typed content never leaves browser
- **Transparent processing**: All code is open and reviewable
- **Educational purpose**: Demonstrative tool, not medical device
- **Informed consent**: Clear explanation of what's measured

## 📈 Future Enhancements

Potential improvements:
- [ ] User profiles for longitudinal tracking
- [ ] Multiple difficulty levels for text
- [ ] Custom text input option
- [ ] Export results as PDF reports
- [ ] Mobile app version
- [ ] Comparison with historical baselines
- [ ] More ML models (SVM, Neural Networks)

## 🤝 Contributing

This is an educational project demonstrating AI/ML concepts. Contributions for improvements are welcome!

## 📄 License

This project is for educational and demonstrative purposes.

## 👨‍💻 Author

Built to demonstrate the intersection of:
- Machine Learning (Random Forest)
- Web Development (Flask, JavaScript)
- Data Visualization (Matplotlib, Seaborn)
- Privacy-Preserving AI
- Healthcare Technology

---

**Remember**: This is a demonstration tool. For actual health concerns, always consult qualified healthcare professionals.
