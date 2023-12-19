from logging import debug
from flask_app.controllers import users
from flask_app.controllers import accounts
from flask_app.controllers import budgets
from flask_app import app


if __name__=="__main__":
    app.run(debug=True)