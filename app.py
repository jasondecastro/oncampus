from flask import Flask, request, jsonify, render_template, redirect, url_for
app = Flask(__name__)

import sqlite3
conn = sqlite3.connect('oncampus')
c = conn.cursor()

@app.route('/')
def hello():
  oncampus = c.execute("SELECT name FROM oncampus")
  return render_template('index.html', oncampus = oncampus)

@app.route('/oncampus', methods=["POST"])
def oncampus():
  if request.form['token'] == '7G2tFCrlxpnHAHn7MfzxzWm1':
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
      text_response = []
      for username in c.execute("SELECT name FROM oncampus"):
        text_response.append("%s is currently on campus. \n" % username)

      c.execute("SELECT COUNT(*) FROM oncampus")
      result = c.fetchone()[0]

      return jsonify({"response_type": "ephemeral", "text": "There are %s people on campus right now!" % str(result), "attachments": [{"text": "\n".join(text_response)}]})
    else:
      return "Not sure what you are looking for."
  else:
    return "This request doesn't appear to be coming from Slack.\nYour IP has been logged."

@app.route('/<anything>', methods=['GET'])
def redirect_this(anything):
  return redirect(url_for('hello'))

if __name__ == '__main__':
  app.run()