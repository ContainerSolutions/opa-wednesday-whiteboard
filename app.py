import os

from flask import Flask, request, render_template
from user_agents import parse

import json
import requests

import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = Flask(__name__)

opa_url = os.environ.get("OPA_ADDR", "http://localhost:8181")
policy_path = os.environ.get("POLICY_PATH", "/v1/data/httpapi/authz")

def check_auth(url, method, device_brand):
    input_dict = {"input": {
        "device": device_brand,
        "method": method,
    }}

    logging.info("Checking auth...")
    logging.info(json.dumps(input_dict, indent=2))

    try:
        rsp = requests.post(url, data=json.dumps(input_dict))
    except Exception as err:
        logging.info(err)
        return {}
    if rsp.status_code >= 300:
        return {}
    j = rsp.json()
    logging.info("Auth response:")
    logging.info(json.dumps(j, indent=2))
    return j

@app.route("/")
def root():
    device_brand = parse(request.headers.get('User-Agent')).device.brand
    url = opa_url + policy_path

    j = check_auth(url, request.method, device_brand).get("result", {})
    if j.get("allow", False) == True:
        return render_template('index.html', result="https://i.imgur.com/O1VyTHW.mp4")
    return render_template('index.html', result="https://i.imgur.com/DKUR9Tk.png")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
