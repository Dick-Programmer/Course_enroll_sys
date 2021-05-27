from functools import wraps

from flask import render_template, redirect, url_for, flash, session, request

from SQL_EA.login.forms import LoginForm
from SQL_EA.modles import Student, Teacher, Manager
from . import login


# def all_login_req(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if "manager" not in session and "student" not in session and "teacher" not in session:
#             return redirect(url_for("login.index", next=request.url))
#         return f(*args, **kwargs)

#     return decorated_function


@login.route("/", methods=['GET', 'POST'])
# @all_login_req
def index():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        student = Student.query.filter_by(xh=data["account"]).count()
        teacher = Teacher.query.filter_by(gh=data["account"]).count()
        manager = Manager.query.filter_by(gh=data["account"]).count()
        if student > 0:
            usr = Student.query.filter_by(xh=data["account"]).first()
            if not usr.check_pwd(data["pwd"]):
                flash("密码有误！")
                return redirect(url_for("login.index"))
            session["student"] = data["account"]
            return redirect(request.args.get("next") or url_for("student.index"))
        elif teacher > 0:
            usr = Teacher.query.filter_by(gh=data["account"]).first()
            if not usr.check_pwd(data["pwd"]):
                flash("密码有误！")
                return redirect(url_for("login.index"))
            session["teacher"] = data["account"]
            return redirect(request.args.get("next") or url_for("teacher.index"))
        elif manager > 0:
            usr = Manager.query.filter_by(gh=data["account"]).first()
            if not usr.check_pwd(data["pwd"]):
                flash("密码有误！")
                return redirect(url_for("login.index"))
            session["manager"] = data["account"]
            return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("SQL_login.html", form=form)
