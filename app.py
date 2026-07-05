from flask import Flask, render_template, request

import json 
import os 
import datetime

app = Flask(__name__)


def load_study_data():
    if not os.path.exists("data.json"):
        return [] 
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            print(data)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        return []


def parse_record_date(record):
    try:
        return datetime.date.fromisoformat(record.get("day", ""))
    
    except (ValueError, TypeError): 
        return datetime.date.min


# Save records sorted from newest day to oldest day.
def save_study_data(records):
    sorted_records = sorted(records, key=parse_record_date, reverse=True)  
    with open("data.json", "w") as file:
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
    else:
        return "Need to improve, try harder"


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Receive form data and save it. Then show the history page.
@app.route("/submit", methods=["POST"])
def submit():
    
    day = request.form.get("day")
    hours_raw = request.form.get("hours", "0")

    # If the user didn't enter a day, use today's date in YYYY-MM-DD format.
    if not day:
        day = datetime.date.today().isoformat()

    # Convert hours to integer; if conversion fails, default to 0.
    try:
        hours = int(hours_raw)
    except ValueError:
        hours = 0

    # Store the new record (newest first in the file).
    store_study_record(day, hours)

    # Prepare data for the template: the most-recent entry's message and the full history.
    message = match_goal(hours)
    history = load_study_data()

    return render_template("result.html", hours=hours, message=message, history=history)


if __name__ == "__main__":
    app.run(debug=True)
     