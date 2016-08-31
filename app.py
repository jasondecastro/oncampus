from flask import Flask, request, jsonify
app = Flask(__name__)

import sqlite3
conn = sqlite3.connect('oncampus')
c = conn.cursor()

@app.route('/oncampus', methods=["POST"])
def oncampus():
  print request.form
  if request.form['text'].lower() == "yes":
    if c.execute("SELECT * FROM oncampus WHERE name = '%s'" % request.form['user_name']).fetchone() == 1:
      return "You have already checked into the Flatiron School campus."
    else:
      try:
        c.execute("INSERT INTO oncampus VALUES (null, '%s')" % request.form['user_name'])
      except sqlite3.IntegrityError:
        return "You have already checked into the Flatiron School campus."
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
    return jsonify({"response_type": "in_channel", "text": "There are %d people on campus right now." % c.execute("SELECT COUNT(*) FROM oncampus"), "attachments": [{"text":"You are online."}]})
  else:
    return "Not sure what you are looking for."

app.run(host='0.0.0.0', port=80)