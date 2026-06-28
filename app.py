from flask import Flask, render_template, request

import json

app = Flask(__name__)

#save data into json
def store_study_data(hours):

    with open("data.json", "w") as file:
        json.dump(hours, file, indent=4)


# check goal
def match_goal(hours):

    if hours >= 6:
        return "Good job, keep going"
    else:
        return "Need to improve, try harder"
    

# home page
@app.route("/")

def home():
    return render_template("index.html")


# receive data from HTML
@app.route("/submit", methods=["POST"])
def submit():

    hours = int(request.form["hours"])

    # save
    store_study_data(hours)

    #calculate messagge
    message = match_goal(hours)

    return render_template(
        "result.html",
        hours=hours,
        message=message
    )

app.run(debug=True)
