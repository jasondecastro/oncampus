from flask import Flask, request
app = Flask(__name__)

@app.route('/oncampus', methods=('POST'))
def oncampus():
  print(request)

app.run()