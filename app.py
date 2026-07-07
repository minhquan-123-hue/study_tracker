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

            if isinstance(data, dict):
                return [{"day": data.get("day", "unknown"), "hours": data.get("hours", 0)}]

            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def parse_record_data(record):
    if not isinstance(record, dict):
        return datetime.date.min

    try:
        return datetime.date.fromisoformat(record.get("day", ""))
    except (ValueError, TypeError):
        return datetime.date.min


def save_study_data(records):
    new_records = sorted(records, key=parse_record_data, reverse=True)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(new_records, file, indent=4)


def store_study_data(day, hours):
    new_record = {"day": day, "hours": hours}
    records = load_study_data()

    is_exist = False
    for record in records:
        if record.get("day", "") == day:
            record["hours"] = hours
            is_exist = True
            break

    if not is_exist:
        records.append(new_record)

    save_study_data(records)


def messages(hours):
    if hours >= 6:
        return "good bro, keep it going!"
    return "haizz, not ok enough, kill Distraction bro, only goal"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/submit", methods=["POST"])
def result():
    hours = int(request.form.get("hours", 0))
    day = request.form.get("day", "unknown")

    store_study_data(day, hours)

    message = messages(hours)
    records = load_study_data()

    return render_template("result.html", hours=hours, day=day, message=message, records=records)


if __name__ == "__main__":
    app.run(debug=True)
