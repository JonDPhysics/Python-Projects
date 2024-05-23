from typing import ParamSpecArgs
from flask.globals import request
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.account import Account
from flask_app.models.budget import BCRYPT

@app.route("/")
def start():
    return render_template("reg_log.html")

@app.route("/dashboard")
def dashboard():
    if not session:
        return redirect("/")
    user = User.get_user_with_accounts({"users_id": session['uuid']})
    print(user)
    print(user.all_accounts)
    return render_template("dashboard.html", user = user)

@app.route("/register", methods=['POST'])
def reg():
    if not User.reg_val(request.form):
        return redirect("/")
    hash_it_out = BCRYPT.generate_password_hash(request.form['password_hash'])
    data = {
        **request.form,
        "password_hash": hash_it_out
    }

    User.insert_user(data)
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    if not User.log_val(request.form):
        return redirect("/")
    user = User.get_user_by_email({"email": request.form["email"]})
    session["uuid"] = user.users_id
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")