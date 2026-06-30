# import flask
# import json

from flask import Flask, render_template, request
import json

# create app with this file
app = Flask(__name__) 

# save data into json
def save_data(hours):
    # store hours in a simple json object
    data = {"hours": hours}
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# message to user
def messages(hours):
    
    if hours >= 6:
        return "good bro, keep it going!"
    else:
        return "haizz, not ok enough, kill Distraction bro, only goal"
    

# home page
@app.route("/")
def home():
    return render_template("home.html")

# result page
@app.route("/submit", methods=["POST"])
def result():

    hours = int(request.form["hours"])

    save_data(hours)

    message = messages(hours)

    return render_template(
        "result.html",
        hours=hours,
        message=message
    )

app.run(debug=True)