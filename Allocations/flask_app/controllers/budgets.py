from typing import ParamSpecArgs
from flask_app import app
from flask.globals import request
from flask import render_template, redirect, request, session
from flask_app.models.budget import Budget

@app.route("/budget/new")
def new_budget():
    return render_template("add_budget.html")

@app.route("/budget/add/<int:account_id>", methods=["POST"])
def add_budget(account_id):
    data = {
        **request.form,
        "account_id": account_id
    }
    Budget.insert_budget(data)
    return redirect("budget.html")

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


