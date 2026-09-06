import joblib
import os

# Find the project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Find the saved ML model
MODEL_PATH = os.path.join(BASE_DIR, "model", "activity_model.pkl")

# Load the trained model
model = joblib.load(MODEL_PATH)

print("ML model loaded successfully!")
# Make a sample prediction
workout_minutes = 30
steps = 5000
calories = 200

prediction = model.predict([
    [workout_minutes, steps, calories]
])

print("Predicted Activity Level:", prediction[0])