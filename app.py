from flask import Flask, request
app = Flask(__name__)

@app.route('/oncampus', methods=["POST"])
def oncampus():
  return request

app.run(host='0.0.0.0', port=80)