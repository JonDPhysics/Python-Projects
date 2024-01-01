from typing import ParamSpecArgs
from flask_app.models.budget import Budget
from flask_app import app
from flask.globals import request
from flask import render_template, redirect, request, session
from flask_app.models.account import Account
from flask_app.models.user import User

@app.route("/account/new")
def new_accounts():
    return render_template("add_account.html")

@app.route("/account/add", methods = ['POST'])
def add_accounts():
    data = {
        **request.form,
        'user_id': session["uuid"]
    }
    Account.insert_account(data)

    return redirect("/dashboard")

@app.route("/budget/<int:id>")
def display_budget(id):
    return render_template("budget.html", account = Account.get_accounts_with_budgets({"id": id}))

@app.route("/account/edit/<int:id>")
def edit_account(id):
    return render_template("edit_account.html", account = Account.get_account_by_id({"id": id}))

@app.route("/account/update/<int:id>", methods = ["POST"])
def update_account(id):
    data ={
        **request.form,
        "id": id,
        "user_id": session["uuid"]
    }
    Account.update_account(data)
    return redirect("/dashboard")

@app.route("/account/delete/<int:id>")
def delete_the_account(id):
    Account.delete_all_inputs({"account_id:": id})
    Account.delete_account({"id": id})
    return redirect("/dashboard")