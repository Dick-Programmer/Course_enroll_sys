from flask import Blueprint

teacher = Blueprint("teacher", __name__)

import SQL_EA.teacher.views
