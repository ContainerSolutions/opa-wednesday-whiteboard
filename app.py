from flask import Flask, request
from user_agents import parse

app = Flask(__name__)

def send_to_opa(device_brand):
    if device_brand == 'Apple':
        return False
    else:
        return True

@app.route("/")
def root():
    device_brand = parse(request.headers.get('User-Agent')).device.brand
    
    result = send_to_opa(device_brand)
    if result:
        return 'yes'
    else:
        return 'no'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
