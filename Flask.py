from flask import Flask
from flask import render_template
from flask import request
import users
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world"

"""
@app.route("/hello/<string:username>")
def hello_user2(username):
    return render_template(
        "template.html",
        title = "Hello User",
        description = f"Hallo {username}!")
"""

@app.route("/hello/<string:username>")
def hello_user(username):
    user = users.User.from_db(username)
    return render_template(
        "template.html",
        title = "Hello User",
        description = f"Hallo {username}!")

@app.route("/hello_flask")
def hello_flask():
    return render_template(
        "template.html",
        title = "Hello Flask",
        description = "This is my first website!")

@app.route("/add_user", methods=["GET", "POST"])
def user_form():
    if request.method == "GET":
        # Zeige das Formular an
        return '''<form method="POST">
                          <div><label>Username: <input type="text" name="username"></label></div>
                          <div><label>Firstname: <input type="text" name="firstname"></label></div>
                          <div><label>Lastname: <input type="text" name="lastname"></label></div>
                          <input type="submit" value="Submit">
                      </form>'''
    else:
        # Verarbeite die Informationen
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        user = users.User(username, firstname, lastname)
        user.to_db()
        return f"Benutzer {username} wurde hinzugefügt"