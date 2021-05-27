from flask import Blueprint

login = Blueprint("login", __name__)

import SQL_EA.login.views
