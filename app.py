# Always remember to pull before pushing!


import pandas as pd


from flask import Flask, render_template, request


app = Flask(__name__)

app.config["DEBUG"] = True



HASHED_PASSWORDS_TABLE = "./data/passwords_table.pickle"



@app.route("/")
def on_index():
    return render_template("index.html")


@app.route("/login")
def on_login():
    return render_template("login.html")

@app.route("/post_login", methods = ["POST", "GET"])
def on_post_login():

    username = request.form["username"]
    password_attempt = request.form["password"]

    df = load_passwords_table()

    if df[df.username==username].hashed_password.to_list()[0] == hash(password_attempt):
        return "It's you!"

    return "You're not who you say you are!"    



@app.route("/signup")
def on_signup():
    return render_template("signup.html")


@app.route("/post_signup", methods = ["POST", "GET"])
def on_post_signup():

    username = request.form["username"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]

    if password != password_confirm:
        return "Looks like a typo! Passwords don't match! Signup aborted."

    df = load_passwords_table()

    row = pd.DataFrame([(username, hash(password))], columns=["username", "hashed_password"]) 

    df = df.append(row)

    store_passwords_table(df)

    return "Welcome"+username+"!"



# username : hashed_password
def load_passwords_table():
    try:
        return pd.read_pickle(HASHED_PASSWORDS_TABLE)
    except:
        return pd.DataFrame([], columns=["username", "hashed_password"])


def store_passwords_table(df):
    df.to_pickle(HASHED_PASSWORDS_TABLE)













