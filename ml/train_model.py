import sqlite3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import joblib

# Find project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "fitness.db")

# Connect to database
conn = sqlite3.connect(DATABASE)

# Read fitness data
df = pd.read_sql_query("SELECT * FROM activities", conn)

conn.close()

# Create Activity Level
def get_activity_level(row):

    if row["steps"] < 5000 and row["workout_minutes"] < 30:
        return "Low"

    elif row["steps"] < 10000 and row["workout_minutes"] < 60:
        return "Moderate"

    else:
        return "High"


df["activity_level"] = df.apply(get_activity_level, axis=1)

# Select features
X = df[["workout_minutes", "steps", "calories"]]

# Target
y = df["activity_level"]

# Create ML model
model = DecisionTreeClassifier(random_state=42)
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model trained successfully!")
print("Model Accuracy:", accuracy)

# Create model folder
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

# Save model
MODEL_PATH = os.path.join(MODEL_DIR, "activity_model.pkl")
joblib.dump(model, MODEL_PATH)
print("Model saved successfully!")