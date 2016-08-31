from flask import Flask, request
app = Flask(__name__)

import sqlite3
conn = sqlite3.connect('oncampus.sqlite')
c = conn.cursor()

@app.route('/oncampus', methods=["POST"])
def oncampus():
  print request.form
  if request.form['text'].lower() == "yes":
    c.execute("INSERT INTO oncampus VALUES (%s)" % request.form['name'])
    conn.commit()
    return "You have checked into the Flatiron School campus."
  elif request.form['text'].lower() == "no":
    if c.execute("SELECT * FROM oncampus WHERE name = %s" % request.form['name']):
      c.execute("DELETE FROM oncampus WHERE name = %s" % request.form['name'])
      conn.commit()
      return "You have checked out of the Flatiron School campus."
    else:
      return "You never checked in, but I\'ll check you out anyway."
  elif request.form['text'].lower() == "who":
    return "Coming soon."
  else:
    return "Not sure what you are looking for."

app.run(host='0.0.0.0', port=80)