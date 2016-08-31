from flask import Flask, request
app = Flask(__name__)

import sqlite3
conn = sqlite3.connect('oncampus')
c = conn.cursor()

@app.route('/oncampus', methods=["POST"])
def oncampus():
  print request.form
  if request.form['text'].lower() == "yes":
    print c.execute("SELECT * FROM oncampus WHERE name = '%s'" % request.form['user_name']).rowcount
    if c.execute("SELECT * FROM oncampus WHERE name = '%s'" % request.form['user_name']) == 1:
      return "You have already checked into the Flatiron School campus."
    else:
      c.execute("INSERT INTO oncampus VALUES (null, '%s')" % request.form['user_name'])
      conn.commit()
      return "You have checked into the Flatiron School campus."
  elif request.form['text'].lower() == "no":
    if c.execute("SELECT * FROM oncampus WHERE name = '%s'" % request.form['user_name']):
      c.execute("DELETE FROM oncampus WHERE name = '%s'" % request.form['user_name'])
      conn.commit()
      return "You have checked out of the Flatiron School campus."
    else:
      return "You never checked in, but I\'ll check you out anyway."
  elif request.form['text'].lower() == "who":
    return "Coming soon."
  else:
    return "Not sure what you are looking for."

app.run(host='0.0.0.0', port=80)