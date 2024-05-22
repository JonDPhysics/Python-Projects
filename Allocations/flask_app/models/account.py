from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.budget import Budget, SCHEMA

class Account:
    def __init__(self, data):
        self.accounts_id = data["accounts_id"]
        self.user_id = data["user_id"]
        self.account_name = data["account_name"]
        self.current_balance = data["current_balance"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.all_transactions = []

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
        query = "SELECT * FROM accounts WHERE accounts_id = %(id)s;"
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
        query = "INSERT INTO accounts (account_name, current_balance, user_id) VALUE (%(account_name)s, %(current_balance)s, %(user_id)s);"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def update_account(cls, data):
        query = "UPDATE accounts SET aname = %(account_name)s, balance = %(current_balance)s, user_id = %(user_id)s WHERE accounts_id = %(accounts_id)s;"
        connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def delete_account(cls, data):
        query = "DELETE FROM accounts WHERE accounts_id = %(id)s;"
        return connectToMySQL(SCHEMA).query_db(query,data)

    @classmethod
    def delete_all_inputs(cls, data):
        query = "DELETE FROM transactions WHERE account_id = %(account_id)s;"
        return connectToMySQL(SCHEMA).query_db(query,data)

    @classmethod
    def get_accounts_with_budgets(cls, data):
        query = "SELECT * FROM accounts LEFT JOIN transactions ON is.account_id = accounts.accounts_id WHERE accounts.accounts_id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        account = cls(results[0])
        for data in results:
            transaction_data = {
                "transactions_id": data["transanctions.transactions_id"],
                "account_id": data["account_id"],
                "transaction_name": data["transaction_name"],
                "amount": data["amount"],
                "transaction_date": data["transaction_date"],
                "inorout": data["inorout"],
                "frequency": data["frequency"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"]
            }
            account.all_transactions.append(Budget(transaction_data))
        return account

    @staticmethod
    def add_val (pd):
        is_valid = True

        if len(pd["account_name"]) < 1:
            flash("Account name is required.")
            is_valid = False

        return is_valid

