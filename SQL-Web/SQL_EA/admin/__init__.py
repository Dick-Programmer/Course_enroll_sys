from flask import Blueprint

admin = Blueprint("admin", __name__)

import SQL_EA.admin.views
