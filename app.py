from flask import Flask, render_template, request

import json
import os
import datetime
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "study_tracker.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL UNIQUE,
            hours REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    migrate_json_data()


def migrate_json_data():
    json_file = BASE_DIR / "data.json"
    if not json_file.exists():
        return

    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) AS count FROM study_records").fetchone()["count"]
    if count > 0:
        conn.close()
        return

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            for item in data:
                day = item.get("day")
                hours = item.get("hours")
                if day:
                    conn.execute(
                        "INSERT INTO study_records (day, hours) VALUES (?, ?)",
                        (day, float(hours)),
                    )
            conn.commit()
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        pass

    conn.close()


def load_study_data():
    conn = get_connection()
    rows = conn.execute(
        "SELECT day, hours FROM study_records ORDER BY day DESC"
    ).fetchall()
    conn.close()

    return [{"day": row["day"], "hours": row["hours"]} for row in rows]


def parse_record_date(record):
    try:
        return datetime.date.fromisoformat(record.get("day", ""))
    except (ValueError, TypeError):
        return datetime.date.min


def save_study_data(records):
    sorted_records = sorted(records, key=parse_record_date, reverse=True)
    conn = get_connection()
    conn.execute("DELETE FROM study_records")
    for record in sorted_records:
        conn.execute(
            "INSERT INTO study_records (day, hours) VALUES (?, ?)",
            (record.get("day"), float(record.get("hours", 0))),
        )
    conn.commit()
    conn.close()


def store_study_record(day, hours):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO study_records (day, hours)
        VALUES (?, ?)
        ON CONFLICT(day) DO UPDATE SET hours = excluded.hours
        """,
        (day, float(hours)),
    )
    conn.commit()
    conn.close()


def match_goal(hours):
    if hours >= 6:
        return "Good job, keep going"
    return "Need to improve, try harder"


init_db()


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
     