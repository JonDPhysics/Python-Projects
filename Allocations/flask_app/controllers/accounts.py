from typing import ParamSpecArgs
from flask_app.models.budget import Budget
from flask_app import app
from flask.globals import request
from flask import render_template, redirect, request, session
from flask_app.models.account import Account

@app.route("/accounts/new")
def new_accounts():
    return render_template("add_account.html")

@app.route("/accounts/add", methods = ['POST'])
def add_accounts():
    data = {
        **request.form,
        'user_id': session["uuid"]
    }
    Account.insert_account(data)

    return redirect("/dashboard")

@app.route("/budget/<int:id>")
def display_budget(id):
    return render_template("budget.html", account = Account.get_accounts_with_budgets({"id": id}), theAccount = Account.get_account_by_id({"id":id}))

@app.route("/account/edit/<int:id>")
def edit_account(id):
    return render_template("edit_account.html", account = Account.get_account_by_id({"id": id}))

@app.route("/account/update", methods = ["POST"])
def update_account():
    data ={
        **request.form,
        "user_id": session["uuid"]
    }
    Account.update_account(data)
    return redirect("/dashboard")

@app.route("/budget/delete/<int:id>")
def delete(id):
    Budget.delete_budget({"id": id})
    return render_template("budget.html")