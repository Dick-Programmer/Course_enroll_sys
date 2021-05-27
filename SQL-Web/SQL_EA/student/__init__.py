from flask import Blueprint

student = Blueprint("student", __name__)

import SQL_EA.student.views
