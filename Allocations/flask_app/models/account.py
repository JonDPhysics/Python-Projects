from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.budget import Budget, SCHEMA

class Account:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.aname = data["aname"]
        self.balance = data["balance"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.all_inputs = []

    @classmethod
    def get_accounts(cls):
        query = "SELECT * FROM accounts;"
        results = connectToMySQL(SCHEMA).query_db(query)
        accounts = []
        for account in results:
            accounts.append(cls(account))
        return accounts

    @classmethod
    def get_account_by_id(cls, data):
        query = "SELECT * FROM accounts WHERE id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        return Account(results[0])
    
    @classmethod
    def get_accounts_by_user_id(cls, data):
        query = "SELECT * FROM accounts WHERE user_id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        accounts = []
        for account in results:
            accounts.append(cls(account))
        return accounts
        

    @classmethod
    def insert_account(cls, data):
        query = "INSERT INTO accounts (aname, balance, user_id) VALUE (%(aname)s, %(balance)s, %(user_id)s);"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def update_account(cls, data):
        query = "UPDATE accounts SET aname = %(aname)s, balance = %(balance)s, user_id = %(user_id)s WHERE id = %(id)s;"
        connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def delete_account(cls, data):
        query = "DELETE FROM accounts WHERE id = %(id)s;"
        return connectToMySQL(SCHEMA).query_db(query,data)

    @classmethod
    def get_accounts_with_budgets(cls, data):
        query = "SELECT * FROM accounts LEFT JOIN inputs ON inputs.account_id = accounts.id WHERE accounts.id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        account = cls(results[0])
        for data in results:
            input_data = {
                "id": data["inputs.id"],
                "account_id": data["account_id"],
                "iname": data["iname"],
                "amount": data["amount"],
                "idate": data["idate"],
                "inorout": data["inorout"],
                "frequency": data["frequency"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"]
            }
            account.all_inputs.append(Budget(input_data))
        return account

    @staticmethod
    def add_val (pd):
        is_valid = True

        if len(pd["aname"]) < 1:
            flash("Account name is required.")
            is_valid = False

        return is_valid

