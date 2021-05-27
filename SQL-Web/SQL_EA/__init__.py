from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1/Student_CV"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'e28e66befe4a4516bb2f8491a88fd28a'
app.debug = True
db = SQLAlchemy(app)

from SQL_EA.login import login as login_blueprint
from SQL_EA.admin import admin as admin_blueprint
from SQL_EA.student import student as student_blueprint
from SQL_EA.teacher import teacher as teacher_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/EA/admin")
app.register_blueprint(student_blueprint, url_prefix="/EA/student")
app.register_blueprint(teacher_blueprint, url_prefix="/EA/teacher")

x = 1
def getx():
    return x
def xadd():
    global x
    x += 1
    return ""
def xzero():
    global x
    x = 1
    return ""
app.add_template_global(getx, 'getx')
app.add_template_global(xadd, 'xadd')
app.add_template_global(xzero, 'xzero')

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("")
