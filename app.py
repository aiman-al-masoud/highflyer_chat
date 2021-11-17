from flask import Flask, render_template, request


app = Flask(__name__)

app.config["DEBUG"] = True


@app.route("/")
def on_index():
    return render_template("index.html")


@app.route("/login")
def on_login():
    return render_template("login.html")


@app.route("/success", methods = ["POST", "GET"])
def on_success():
    return str(request.form)



@app.route("/signup")
def on_signup():
    return render_template("signup.html")


@app.route("/new_user", methods = ["POST", "GET"])
def on_new_user():
    return "welcome!"+str(request.form)














