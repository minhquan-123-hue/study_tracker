from flask import Flask, render_template, request

import json # object store info of data structure 

app = Flask(__name__) # this is an object + special variable 

# save data into json
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
# object call method add parameter / 
# and use decorator to add new functional for the route() method.
def home():
    return render_template("index.html") 


# receive data from HTML
@app.route("/submit", methods=["POST"]) 
# /submit là nhảy sang một đường dẫn khác khi người dùng gõ vào submit
# POST là nhận dữ liệu từ browser 
def submit():

    hours = int(request.form["hours"]) 
    # đây là một trường của dữ liệu mà flask nhận lại từ browser
    # và điền thông tin vào trong đó 
    # sau đó ta lưu lại sang biến hours 

    # save to json file 
    store_study_data(hours)

    #calculate messagge
    message = match_goal(hours)

    # hàm render_template của flask
    # có khả năng đọc các tag và sau đó điền vào thẻ 
    return render_template(
        "result.html",
        hours=hours,
        message=message
    )

app.run(debug=True)
