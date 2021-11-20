# Always remember to pull before pushing!

# imports
import pandas as pd
from flask import Flask, render_template, request
import hashlib
from time import time
import random



# constants
PASSWORDS_TABLE_PATH = "./user_data/passwords_table.csv"
MESSAGES_TABLE_PATH = "./user_data/messages_table.csv"


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

    # load passwords table
    df = get_passwords_table()

    # get input data from form
    username = request.form["username"]
    password_attempt = request.form["password"]


    #TODO redirect to signup
    # check if username exists
    if not user_exists(username):
        return "You don't have an account yet!"


    # compare entered password's hash to actual password's hash
    if df[df.username==username].hashed_password.to_list()[0] == hash_password(password_attempt):
        
        #refresh the last_login_time of the user
        refresh_last_login(username)

        # generate a new session id token, set it for the user and send it to the user
        session_id = generate_session_id()

        set_session_id(username, session_id)

        return render_template("user_console.html", current_user=username, inbox = get_users_messages(username), session_id = session_id)


    return "Wrong username and/or password!"    




@app.route("/post_signup", methods = ["POST", "GET"])
def on_post_signup():

    # load passwords table
    df = get_passwords_table()

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

    # add the user and hashed password to the passwords table    
    row = pd.DataFrame([(username, hash_password(password), 0)], columns=["username", "hashed_password", "last_login_time"]) 
    df = df.append(row)
    store_passwords_table(df)

    # first login happened NOW
    refresh_last_login(username)

    # welcome new user
    return f'Welcome {username}!'




def get_passwords_table():

    """
    Load the passwords table.
    """
    try:
        # read the table from a csv
        return pd.read_csv(PASSWORDS_TABLE_PATH)
    except:
        # initialize a new empty passwords table if file not found
        return create_passwords_table()



def create_passwords_table():
    return pd.DataFrame([], columns=["username", "hashed_password", "last_login_time", "session_id"])


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
        return render_template("user_console.html", current_user=sender, inbox = get_users_messages(sender), session_id = get_session_id(sender))

    return  "Send failed!"


# TODO: retrieve sender and timestamp info, not just content, maybe make a Message class
def get_users_messages(receiver):
    df = get_messages_table()
    return df[df.receiver==receiver].message.to_list()



def refresh_last_login(username):
    df = get_passwords_table()
    df.loc[df.username == username, 'last_login_time'] = time()
    store_passwords_table(df)


def get_last_login(username):
    df = get_passwords_table()
    return float(df.set_index("username").at[username, "last_login_time"])



# TODO: add RSA encryption
def create_messages_table():
    return pd.DataFrame([], columns=["timestamp","sender", "receiver", "message"])


def get_messages_table():
      try:
        # read the table from a csv
        return pd.read_csv(MESSAGES_TABLE_PATH)
      except:
        # initialize a new empty messages table if file not found
        return create_messages_table()






def send_message(sender, receiver, message, time):

    # TODO: error of some sort
    if not user_exists(sender) or not user_exists(receiver):
        return 

    # TODO: redirect user to login
    if not session_expired(sender):
        return False

    # append new message to table    
    df = get_messages_table()    
    row = pd.DataFrame( [(time, sender, receiver, message)] , columns=["timestamp", "sender", "receiver", "message"])
    df = df.append(row)
    store_messages_table(df)
    
    return True






def store_passwords_table(df):
    """
    Store the passwords table.
    Arguments: passwords dataframe.
    """
    df.to_csv(PASSWORDS_TABLE_PATH, index=False)



def store_messages_table(df):
    df.to_csv(MESSAGES_TABLE_PATH, index=False)






def user_exists(username):
    """
    Checks if a username is taken.
    """

    df = get_passwords_table()
    return (df.username==username).sum() != 0 


def hash_password(password):
    h = hashlib.sha1(password.encode("utf-8")).hexdigest()
    return h




# TODO: improve rule to determine if user is logged in
def session_expired(username):

    # in seconds
    last_time = get_last_login(username)
    current_time = time()

    # 5 minutes
    if current_time - last_time < 300:
        return True

    return False    




def generate_session_id():
    return random.randint(0 , 1000000000)


def set_session_id(username, new_session_id):

    df = get_passwords_table()
    df.loc[df.username == username, 'session_id'] = new_session_id
    store_passwords_table(df)



def get_session_id(username):
    df = get_passwords_table()
    return df.loc[df.username == username, 'session_id'].to_list()[0]







