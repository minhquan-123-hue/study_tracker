# Study Tracker

A simple Flask app to track daily study hours.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

The app stores data in a SQLite database file named `study_tracker.db`.
This is better than JSON for deployment because the data will persist in a real database file.
