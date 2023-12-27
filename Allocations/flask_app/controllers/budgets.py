from typing import ParamSpecArgs
from flask_app import app
from flask.globals import request
from flask import render_template, redirect, request
from flask_app.models.budget import Budget
from flask_app.models.account import Account

@app.route("/budget/new/<int:id>")
def new_budget(id):
    return render_template("add_budget.html", account = Account.get_account_by_id({"id":id}))

@app.route("/budget/add/<int:id>", methods=["POST"])
def add_budget(id):
    data = {
        **request.form,
        "account_id": id
    }
    Budget.insert_budget(data)
    return redirect("/dashboard")

@app.route("/budget/edit/<int:id>")
def edit_budget(id):
    return render_template("edit_budget.html", budget = Budget.get_budget_by_id({"id": id}))

@app.route("/budget/update/<int:account_id>")
def update_budget(account_id):
    data = {
        **request.form,
        "account_id": account_id
    }
    Budget.update_budget(data)
    return render_template("budget.html")

@app.route("/budget/delete/<int:id>")
def delete_the_budget(id):
    Budget.delete_budget({"id": id})
    return render_template("budget.html")


