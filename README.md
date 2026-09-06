# 🏃 CodeAlpha Fitness Tracker

A web-based Fitness Tracker application built using Python, Flask, SQLite, and Machine Learning.

## 🚀 Features

- 📝 Add daily fitness activities
- 🏃 Select exercise type
- ⏱️ Record workout duration
- 👣 Track daily steps
- 🔥 Record calories burned
- 📊 View total fitness statistics
- 📅 View weekly progress
- 📈 Interactive Steps and Calories charts
- 🧠 Machine Learning-based activity level classification
- 🗑️ Delete activities
- 💻 Simple and user-friendly interface

## 🛠️ Technologies Used

- Python
- Flask
- SQLite
- Pandas
- Scikit-learn
- Joblib
- HTML
- CSS
- JavaScript
- Chart.js

## 🤖 Machine Learning

A Decision Tree Classifier is used to classify activity levels as:

- Low
- Moderate
- High

The model uses workout duration, steps, and calories as input features.

> Note: The ML component is designed as a project demonstration and is not a medical or health assessment tool.

## 📂 Project Structure

```text
Fitness-Tracker/
│
├── app.py
├── create_database.py
├── fitness.db
├── requirements.txt
├── .gitignore
│
├── model/
│   └── activity_model.pkl
│
├── ml/
│   ├── prepare_data.py
│   ├── train_model.py
│   └── predict.py
│
├── templates/
│   ├── index.html
│   └── add_activity.html
│
└── static/
    └── style.css