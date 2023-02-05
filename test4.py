import numpy as np
from math import sqrt
import math
from flask import g,Flask,render_template,request,make_response
import requests
import json
import threading 

import asyncio
import websockets

app = Flask(__name__)

yValues = [60] * 50


@app.route("/getHeartRate", methods=["POST"])
def getHeartRate():
    data = request.get_json()
    global yValues
    newRate = data
    yValues = yValues[1:len(yValues)]
    yValues.append(newRate)
    return ("nothing")

@app.route("/requestUpdate", methods=["POST"])
def requestUpdate():
    global yValues
    return yValues

@app.route("/")
def homePage():
    global yValues
    xValues = list(range(51))
    
    return render_template("heartRate.html", xValues = xValues, yValues = yValues)



def handle(res):
    opcode = res ['op']
    print(res)
    if opcode == 5:
        print(res)
        newRate = res["d"]["val"]
        requests.post("http://localhost:8000", json=res)
        # print(res)
        # global yValues
       
        # print(newRate)
        # yValues = yValues[1:len(yValues)]
        # yValues.append(newRate)x

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

# t1 = threading.Thread(target= foo)
# t2 = threading.Thread(target = bar)

# t1.start()
# t2.start()
# asyncio.run(bar())
foo()
# asyncio.run(foo())