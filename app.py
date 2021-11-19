# Always remember to pull before pushing!

# imports
import pandas as pd
from flask import Flask, render_template, request
import hashlib


# constants
PASSWORDS_TABLE_PATH = "./data/passwords_table.csv"


# start the app
app = Flask(__name__)
app.config["DEBUG"] = True






@app.route("/")
def on_index():
    return render_template("index.html")


@app.route("/login")
def on_login():
    return render_template("login.html")

@app.route("/post_login", methods = ["POST", "GET"])
def on_post_login():

    # load passwords table
    df = load_passwords_table()

    # get input data from form
    username = request.form["username"]
    password_attempt = request.form["password"]


    # check if username exists
    if not user_exists(username):
        return "You don't have an account yet!"


    # compare entered password's hash to actual password's hash
    if df[df.username==username].hashed_password.to_list()[0] == hash_password(password_attempt):
        return "It's you!"

    return "You're not who you say you are!"    



@app.route("/signup")
def on_signup():
    return render_template("signup.html")


@app.route("/post_signup", methods = ["POST", "GET"])
def on_post_signup():

    # load passwords table
    df = load_passwords_table()

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
    row = pd.DataFrame([(username, hash_password(password))], columns=["username", "hashed_password"]) 
    df = df.append(row)
    store_passwords_table(df)

    # welcome new user
    return f'Welcome {username}!'


def load_passwords_table():

    """
    Load the passwords table.
    """
    try:
        # read the table from a csv
        return pd.read_csv(PASSWORDS_TABLE_PATH)
    except:
        # initialize a new passwords table if file not found
        return pd.DataFrame([], columns=["username", "hashed_password"])
    


def store_passwords_table(df):
    """
    Store the passwords table.
    Arguments: passwords dataframe.
    """
    df.to_csv(PASSWORDS_TABLE_PATH, index=False)



def user_exists(username):
    """
    Checks if a username is taken.
    """

    df = load_passwords_table()
    return (df.username==username).sum() != 0 


def hash_password(password):
    h = hashlib.sha1(password.encode("utf-8")).hexdigest()
    return h




