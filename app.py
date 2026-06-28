from flask import Flask, render_template
import json

app = Flask(__name__)

def read_data():
    with open("data.json" , "r") as file:
        data = json.load(file)

    return data

@app.route("/")
def home():
    hours = read_data()

    return render_template("index.html", hours = hours)

app.run(debug=True)