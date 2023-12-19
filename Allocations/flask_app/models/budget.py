import secrets
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re


BCRYPT = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
SCHEMA = "allocations"

class Budget:
    def __init__(self, data):
        self.id = data['id']
        self.account_id = data["account_id"]
        self.bname = data['bname']
        self.amount = data["amount"]
        self.bdate = data["bdate"]
        self.inout = data['inout']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_budgets(cls):
        query = "SELECT * FROM budgets;"
        results = connectToMySQL(SCHEMA).query_db(query)
        budgets = []
        for budget in results:
            budgets.append(cls(budget))
        return budgets

    @classmethod
    def get_budget_by_id(cls, data):
        query = "SELECT * FROM budgets WHERE id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        return Budget(results[0])

    @classmethod
    def insert_budget(cls, data):
        query = "INSERT FROM budgets (amount, bdate, bname, inout, account_id, account_user_id) VALUE (%(amount)s, %(bdate)s, %(bname)s, %(inout)s, %(account_id)s, %(account_user_id)s);"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def update_budget(cls, data):
        query = "UPDATE budgets SET amount = %(amount)s, bdate = %(bdate)s, bname = %(bname)s, inout = %(inout)s, account_id = %(account_id)s, account_user_id = %(account_user_id)s;"
        connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def delete_budget(cls, data):
        query = "DELETE FROM budgets WHERE id = %(id)s;"
        connectToMySQL(SCHEMA).query_db(query, data)
        return id


    @staticmethod
    def add_val(pd):
        is_valid = True

        if len(pd["bname"]) < 1:
            flash("Name must be at least one character.")
            is_valid = False

        if float(pd["amount"]) <= 0.00:
            flash("amount must be greater than $0.00.")
            is_valid = False

        return is_valid
