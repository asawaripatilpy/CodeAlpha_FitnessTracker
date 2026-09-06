from flask import Flask, render_template, request, redirect
import sqlite3
import os
import joblib
import pandas as pd
from datetime import date, timedelta

app = Flask(__name__)

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "fitness.db")
MODEL_PATH = os.path.join(BASE_DIR, "model", "activity_model.pkl")

# Load ML model
model = joblib.load(MODEL_PATH)


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# HOME / DASHBOARD
# =========================================================

@app.route("/")
def home():

    conn = get_db_connection()

    # Get all activities
    activities = conn.execute(
        "SELECT * FROM activities ORDER BY date DESC"
    ).fetchall()
    activities = [dict(activity) for activity in activities]

    for activity in activities:
        activity["activity_level"] = model.predict(pd.DataFrame([[
        activity["workout_minutes"],
        activity["steps"],
        activity["calories"]
        ]], columns=["workout_minutes", "steps", "calories"]))[0]

    # Calculate totals
    totals = conn.execute("""
        SELECT
            SUM(steps) AS total_steps,
            SUM(calories) AS total_calories,
            SUM(workout_minutes) AS total_workout
        FROM activities
    """).fetchone()
    # Calculate weekly progress
    today = date.today()
    week_start = today - timedelta(days=6)

    weekly_progress = conn.execute("""
    SELECT
        COALESCE(SUM(steps), 0) AS weekly_steps,
        COALESCE(SUM(calories), 0) AS weekly_calories,
        COALESCE(SUM(workout_minutes), 0) AS weekly_workout,
        COUNT(*) AS weekly_activities
    FROM activities
    WHERE date BETWEEN ? AND ?
    """, (
    week_start.isoformat(),
    today.isoformat()
    )).fetchone()

    # Get latest activity
    latest_activity = conn.execute(
        "SELECT * FROM activities ORDER BY id DESC LIMIT 1"
    ).fetchone()

    conn.close()

    # Data for Steps Chart
    chart_dates = [activity["date"] for activity in activities]
    chart_steps = [activity["steps"] for activity in activities]
    chart_calories = [activity["calories"] for activity in activities]

    # Latest ML Prediction
    latest_prediction = "No data"

    if latest_activity:
        latest_prediction = model.predict(pd.DataFrame([[
        latest_activity["workout_minutes"],
        latest_activity["steps"],
        latest_activity["calories"]
    ]], columns=["workout_minutes", "steps", "calories"]))[0]

    return render_template(
        "index.html",
        activities=activities,
        totals=totals,
        weekly_progress=weekly_progress,
        latest_prediction=latest_prediction,
        chart_dates=chart_dates,
        chart_steps=chart_steps,
        chart_calories=chart_calories
    )


# =========================================================
# ADD ACTIVITY
# =========================================================

@app.route("/add", methods=["GET", "POST"])
def add_activity():

    if request.method == "POST":

        # Get form data
        date = request.form["date"]
        exercise_type = request.form["exercise_type"]
        workout_minutes = request.form["workout_minutes"]
        steps = request.form["steps"]
        calories = request.form["calories"]

        # ML Prediction
        prediction = model.predict(pd.DataFrame([[
        int(workout_minutes),
        int(steps),
        int(calories)
        ]], columns=["workout_minutes", "steps", "calories"]))

        activity_level = prediction[0]

        # Save activity to database
        conn = get_db_connection()

        conn.execute("""
            INSERT INTO activities
            (date, exercise_type, workout_minutes, steps, calories)
            VALUES (?, ?, ?, ?, ?)
        """, (
            date,
            exercise_type,
            workout_minutes,
            steps,
            calories
        ))

        conn.commit()
        conn.close()

        # Show ML prediction
        return render_template(
            "add_activity.html",
            prediction=activity_level
        )

    return render_template("add_activity.html")


# =========================================================
# RUN APPLICATION
# =========================================================
@app.route("/delete/<int:activity_id>", methods=["POST"])
def delete_activity(activity_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM activities WHERE id = ?",
        (activity_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)