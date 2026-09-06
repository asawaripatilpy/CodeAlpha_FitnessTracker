import sqlite3
import pandas as pd
import os

# Connect to database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "fitness.db")

conn = sqlite3.connect(DATABASE)

# Read fitness data
df = pd.read_sql_query("SELECT * FROM activities", conn)

# Close database connection
conn.close()

# Display the data
print("Fitness Data:")
print(df)

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)
# Select useful columns for Machine Learning
ml_data = df[
    ["exercise_type", "workout_minutes", "steps", "calories"]
]

print("\nML Dataset:")
print(ml_data)
# Create Activity Level
def get_activity_level(row):

    if row["steps"] < 5000 and row["workout_minutes"] < 30:
        return "Low"

    elif row["steps"] < 10000 and row["workout_minutes"] < 60:
        return "Moderate"

    else:
        return "High"


ml_data["activity_level"] = ml_data.apply(get_activity_level, axis=1)

print("\nActivity Level:")
print(ml_data)