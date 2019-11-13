import json
import logging
import os
import sys

import requests
from flask import Flask, render_template, request
from user_agents import parse

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = Flask(__name__)

opa_url = os.environ.get("OPA_ADDR", "http://localhost:8181")
policy_path = os.environ.get("POLICY_PATH", "/v1/data/httpapi/authz")


def check_auth(url, method, device_os_family):
    input_dict = {"input": {"os_family": device_os_family, "method": method,}}

    logging.info("Checking auth...")
    logging.info(json.dumps(input_dict, indent=2))

    try:
        r = requests.post(url, json=input_dict)
        r.raise_for_status()
    except Exception as err:
        logging.info(err)
        return {}

    if r.status_code >= 300:
        return {}

    logging.info("Auth response:")
    logging.info(json.dumps(r.json(), indent=2))
    return r.json()


@app.route("/")
def root():
    device_os_family = parse(request.headers.get("User-Agent")).os.family
    print(parse(request.headers.get("User-Agent")))
    url = opa_url + policy_path

    j = check_auth(url, request.method, device_os_family).get("result", {})
    if j.get("allow", False) == True:
        return render_template("index.html", result="https://i.imgur.com/O1VyTHW.mp4")
    return render_template("index.html", result="https://i.imgur.com/DKUR9Tk.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
