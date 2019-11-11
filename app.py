from flask import Flask, request, render_template
from user_agents import parse

app = Flask(__name__)

def send_to_opa(device_brand):
    if device_brand == 'Apple':
        return "https://i.imgur.com/OD8x4U3.png"
    else:
        return "https://i.imgur.com/hvkdIxM.png"

@app.route("/")
def root():
    device_brand = parse(request.headers.get('User-Agent')).device.brand
    
    result = send_to_opa(device_brand)
    return render_template('index.html', result=result)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
