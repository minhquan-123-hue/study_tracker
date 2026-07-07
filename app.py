from flask import Flask, render_template, request

import json
import os
import datetime

app = Flask(__name__)


def load_study_data():
    if not os.path.exists("data.json"):
        return []

    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def parse_record_date(record):
    try:
        return datetime.date.fromisoformat(record.get("day", ""))
    except (ValueError, TypeError):
        return datetime.date.min


# Save records sorted from newest day to oldest day.
def save_study_data(records):
    sorted_records = sorted(records, key=parse_record_date, reverse=True)
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(sorted_records, file, indent=4)


def store_study_record(day, hours):
    record = {"day": day, "hours": hours}
    records = load_study_data()

    updated = False
    for existing in records:
        if existing.get("day") == day:
            existing["hours"] = hours
            updated = True
            break

    if not updated:
        records.append(record)

    save_study_data(records)


def match_goal(hours):
    if hours >= 6:
        return "Good job, keep going"
    return "Need to improve, try harder"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/goal")
def goal():
    goals = [
        {"subject": "Math / Physics", "time": "2 hours"},
        {"subject": "Software", "time": "2 hours"},
        {"subject": "Review lessons", "time": "30 minutes"},
        {"subject": "English", "time": "30 minutes"},
        {"subject": "Book and game", "time": "1 hour"},
    ]
    return render_template("goal.html", goals=goals)


@app.route("/submit", methods=["POST"])
def submit():
    day = request.form.get("day")
    hours_raw = request.form.get("hours", "0")

    if not day:
        day = datetime.date.today().isoformat()

    try:
        hours = float(hours_raw)
    except ValueError:
        hours = 0.0

    store_study_record(day, hours)

    message = match_goal(hours)
    history = load_study_data()

    return render_template("result.html", hours=hours, message=message, history=history)


if __name__ == "__main__":
    app.run(debug=True)
     