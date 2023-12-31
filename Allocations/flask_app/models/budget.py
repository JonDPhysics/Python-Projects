import secrets
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re


BCRYPT = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
SCHEMA = "allocations_db"

class Budget:
    def __init__(self, data):
        self.id = data['id']
        self.account_id = data["account_id"]
        self.iname = data['iname']
        self.amount = data["amount"]
        self.idate = data["idate"]
        self.inorout = data['inorout']
        self.frequency = data["frequency"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_budgets(cls):
        query = "SELECT * FROM inputs;"
        results = connectToMySQL(SCHEMA).query_db(query)
        inputs = []
        for input in results:
            inputs.append(cls(input))
        return inputs

    @classmethod
    def get_budget_by_id(cls, data):
        query = "SELECT * FROM inputs WHERE id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        return Budget(results[0])
    
    @classmethod
    def get_budget_by_account_id(cls, data):
        query = "SELECT * FROM inputs WHERE account_id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        return Budget(results[0])

    @classmethod
    def insert_budget(cls, data):
        query = "INSERT INTO inputs (iname, amount, idate, inorout, frequency, account_id) VALUE (%(iname)s, %(amount)s, %(idate)s, %(inorout)s, %(frequency)s, %(account_id)s);"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def update_budget(cls, data):
        query = "UPDATE inputs SET amount = %(amount)s, idate = %(idate)s, bname = %(iname)s, inorout = %(inorout)s, frequency = %(frequency)s, account_id = %(account_id)s;"
        connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def delete_budget(cls, data):
        query = "DELETE FROM inputs WHERE id = %(id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)


    @staticmethod
    def add_val(pd):
        is_valid = True

        if len(pd["iname"]) < 1:
            flash("Name must be at least one character.")
            is_valid = False

        if float(pd["amount"]) <= 0.00:
            flash("amount must be greater than $0.00.")
            is_valid = False

        return is_valid
