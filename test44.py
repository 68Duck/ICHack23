import numpy as np
from math import sqrt
import math
from flask import g,Flask,render_template,request,make_response
import requests
import json
import threading 
import sqlite3
from os import path

import asyncio
import websockets


fileDir = path.dirname(__file__)
app = Flask(__name__)

DATABASE = 'logins.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path.join(fileDir,DATABASE))
    return db

@app.teardown_appcontext  #closes the database when the file is closed
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/attemptToLogin", methods = ["POST"])
def attemptToLogin():
    data = request.get_json()
    if data is None:
        pass 
    else:
        pass


yValues = [60] * 50


@app.route("/getHeartRate", methods=["POST"])
def getHeartRate():
    data = request.get_json()
    global yValues
    newRate = data
    yValues = yValues[1:len(yValues)]
    yValues.append(newRate)
    return ("nothing")

@app.route("/", methods=["POST"])
def getInfo():
    global yValues
    data= request.get_json()
    print(data)
    newRate = data["d"]["val"]
    print(newRate)
    yValues = yValues[1:len(yValues)]
    yValues.append(newRate)
    return ("nothing")


@app.route("/requestUpdate", methods=["POST"])
def requestUpdate():
    global yValues
    return yValues

@app.route("/home")
def homePage():
    global yValues
    xValues = list(range(51))
    
    return render_template("heartRate.html", xValues = xValues, yValues = yValues)



def handle(res):
    opcode = res ['op']
    
    if opcode == 5:
        print(res)
        global yValues
        newRate = res["d"]["val"]
        print(newRate)
        yValues = yValues[1:len(yValues)]
        yValues.append(newRate)

def getAuth():
    dev_id = "ichack23-dev-3R8k93a9x3"
    api_key = "7b5a00daf6898a1d533df213c17d6b6281007bb7a4e9077db6c9117d0805ad73"

    headers = {
        "dev-id": dev_id,
        "x-api-key": api_key
    }

    response = requests.post("https://ws.tryterra.co/auth/developer", headers=headers)

    response = json.loads(response.text)

    print(response)

    return response ["token"]

async def hello():
    uri = "wss://ws.tryterra.co/connect"

    token = getAuth()

    print(token)
    auth = {
        "op": 3,
        "d": {
            "token": token,
            "type": 1
        }
    }


    async with websockets.connect(uri) as websocket:

        hello = json.loads(await websocket.recv())

        heartbeat = hello ["d"]["heartbeat_interval"]

        await websocket.send(json.dumps(auth))

        while True:
            await websocket.send(json.dumps({"op": 0}))
            res = json.loads(await websocket.recv())

            handle(res)

            res = json.loads(await websocket.recv())

            handle(res)


def foo():
    asyncio.get_event_loop().run_until_complete(hello())

def bar():
    app.run(host="localhost", port = 8000)

bar()