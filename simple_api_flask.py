#!/usr/bin/env python
from flask import Flask , jsonify,request
from flask_session import Session

app=Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

numbers = {
        "first":{},
        "scnd":{},
        "third":{},
    }


admin = "superuser"
password_pass = "password"

@app.route("/",methods=["GET","POST"])
def index():


    if request.method == "POST":
        req = request.authorization
        if req.username==admin and req.password == password_pass :
            sent = request.json
            for i in sent:
                numbers[i] = sent[i]

            return jsonify(numbers)
        else :
            return "Not allowed to change any api"

    return jsonify(numbers)



app.run(debug=True)

"""
req = requests.get('http://localhost:5000/')
keys_json=req.json().keys()
>>> for i in keys_json:
...     req = requests.post('http://localhost:5000/',auth=('superuser','password'),json={i:"changed"})
... 
>>> req = requests.get('http://localhost:5000/')
>>> req.json()['012']
'changed'

"""
