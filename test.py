from flask import Flask 

app = Flask(__name__)

@app.route("/")
def test():
    return "test"


@app.route("/api/terra", methods=["POST"])
def handle_terra_data():
    request_body = request.get_json()
    data_payload = request_body.get("data", {})

    if request_body["type"] == "ACTIVITY":

        pass 
    elif request_body["type"] == "BODY":
        pass

    print(json.dumps(request_body, indent=4))

    return flask.Response(status=http.HTTPSatus.OK)


if __name__ == "__main__":
    app.run(host="localhost", port = 8000)


