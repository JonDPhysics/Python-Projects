from typing import ParamSpecArgs
from flask_app import app
from flask.globals import request
from flask import render_template, redirect, request
from flask_app.models.budget import Budget
from flask_app.models.account import Account
from flask import url_for

@app.route("/budget/new/<int:id>")
def new_budget(id):
    return render_template("add_budget.html", account = Account.get_account_by_id({"accounts_id":id}))

@app.route("/budget/add/<int:id>", methods=["POST"])
def add_budget(id):
    data = {
        **request.form,
        "account_id": id
    }
    Budget.insert_budget(data)
    return redirect(url_for('budget', accounts_id=id))

@app.route("/budget/edit/<int:account_id>/<int:id>")
def edit_budget(account_id, id):
    return render_template("edit_budget.html", account = Account.get_account_by_id({"accounts_id": id}), transaction = Budget.get_budget_by_id({"id": id}))

@app.route("/budget/update/<int:id>/<int:inputID>", methods=["POST"])
def update_budgets(id, inputID):
    data = {
        **request.form,
        "transactions_id": inputID,
        "account_id": id
    }
    Budget.update_budget(data)
    return redirect(url_for('budget', accounts_id= id))

@app.route("/budget/delete/<int:id>/<int:account_id>")
def delete_the_budget(id, account_id):
    Budget.delete_budget({"transactions_id": id})
    return render_template("budget.html", account = Account.get_accounts_with_budgets({"account_id": account_id}))


