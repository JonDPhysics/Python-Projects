from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.budget import SCHEMA, EMAIL_REGEX, BCRYPT
from flask_app.models.account import Account
from flask import flash


class User:
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_accounts = []

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(SCHEMA).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(SCHEMA).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(SCHEMA).query_db(query, data)
        if len(result) < 1:
            return False
        return User(result[0])

    @classmethod
    def insert_user(cls, data):
        query = "INSERT INTO users (fname, lname, email, pw) VALUE (%(fname)s, %(lname)s, %(email)s, %(pw)s)"
        return connectToMySQL(SCHEMA).query_db(query, data)

    @classmethod
    def get_user_with_accounts(cls, data):
        query = "SELECT * FROM users LEFT JOIN accounts ON accounts.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        user = cls(results[0])
        for data in results:
            account_data = {
                "id": data["accounts.id"],
                "user_id": data["user_id"],
                "aname" : data["aname"],
                "balance": data["balance"],
                "created_at" : data["accounts.created_at"],
                "updated_at" : data["accounts.updated_at"]
            }
            user.all_accounts.append(Account(account_data))
        return user

    @staticmethod
    def reg_val(pd):
        is_valid = True

        if len(pd["fname"]) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False

        if len(pd["lname"]) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        if not EMAIL_REGEX.match(pd["email"]):
            flash("Invalid email address.")
            is_valid = False
        else:
            user = User.get_user_by_email({'email': pd['email']})
            if user:
                flash("Email is already in use.")
                is_valid = False

        if len(pd["pw"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        if pd["pw"] != pd["cpw"]:
            flash("Passwords do not match.")
            is_valid = False

        return is_valid

    @staticmethod
    def log_val(pd):
        user = User.get_user_by_email({'email': pd['email']})

        if not user:
            flash("Email not registered")
            return False

        if not BCRYPT.check_password_hash(user.pw, pd["pw"]):
            flash("Incorrect Password")
            return False

        return True