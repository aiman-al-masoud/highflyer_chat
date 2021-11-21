# Always remember to pull before pushing!

# imports
from flask import Flask, render_template, request
from core import *


# start the app
app = Flask(__name__)
app.config["DEBUG"] = True



@app.route("/")
def on_index():
    return render_template("index.html")


@app.route("/login")
def on_login():
    return render_template("login.html")


@app.route("/signup")
def on_signup():
    return render_template("signup.html")



@app.route("/post_login", methods = ["POST", "GET"])
def on_post_login():

    # get input data from form
    username = request.form["username"]
    password_attempt = request.form["password"]


    #TODO redirect to signup
    # check if username exists
    if not user_exists(username):
        return "You don't have an account yet!"

    # compare entered password's hash to actual password's hash
    if get_passhash(username) == hash_password(password_attempt):
 
        #refresh the last_login_time of the user
        refresh_last_login(username)

        # generate a new session id token, set it for the user and send it to the user
        session_id = generate_session_id()

        set_session_id(username, session_id)

        return render_template("user_console.html", current_user=username, inbox = get_users_inbox(username), session_id = session_id)


    return "Wrong username and/or password!"    



@app.route("/post_signup", methods = ["POST", "GET"])
def on_post_signup():

    # get input data from form
    username = request.form["username"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]

    # check if username is already taken
    if user_exists(username):
        return f'Username {username} is already taken!'


    # check if new password was confirmed correctly
    if password != password_confirm:
        return "Looks like a typo! Passwords don't match! Signup aborted."

    # create a new user:
    create_user(username, password)

    # first login happened NOW
    refresh_last_login(username)

    # welcome new user
    return f'Welcome {username}!'


@app.route("/post_send_message", methods = ["GET", "POST"])
def on_post_send_message():

    sender = request.form["sender"]
    receiver = request.form["receiver"]
    message =  request.form["message"]
    session_id = request.form["session_id"]

    #TODO: get true send time from html document instead
    mess_time = time()

    #get the user's current/last session id
    current_session_id = get_session_id(sender)

    # TODO: redirect to login page
    if int(eval(str(session_id) ) )!=int(eval(str(current_session_id))):
        return "Session id token expired!"

    if send_message(sender, receiver, message, mess_time):
        return render_template("user_console.html", current_user=sender, inbox = get_users_inbox(sender), session_id = get_session_id(sender))

    return  "Send failed!"

















