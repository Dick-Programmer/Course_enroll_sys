from flask import render_template, redirect, url_for, session, request, flash
from . import student
from SQL_EA import db
from SQL_EA.modles import Student, College, SelectC, Class, Course, Teacher, Semester, Inform, SelectCtime
from SQL_EA.student.forms import informationForm, SettingForm, CourseForm, SearchClass
from functools import wraps
from datetime import *

# 用作临时结构体
class Employee:
    pass

def student_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "student" not in session:
            return redirect(url_for("login.index", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

# 首页
@student.route("/")
@student_login_req
def index():
    seme = Semester.query.filter_by(now = 1).first()
    Date = date.today()
    inf = Inform.query.all()
    user = Student.query.get(session["student"])
    return render_template("student/student-index.html", seme=seme, inf=inf, date=Date, user=user)

# 登出
@student.route("/logout")
@student_login_req
def logout():
    session.pop("student", None)
    return redirect(url_for("login.index"))

# 个人信息
@student.route("/info", methods=['GET', 'POST'])
@student_login_req
def userinfo():
    form = informationForm()
    form2 = SettingForm()
    user = Student.query.get(session["student"])
    co = College.query.filter_by(yxh=user.yxh).first()
    if request.method == 'GET':
        form.xh.data = user.xh
        form.name.data = user.name
        form.sex.data = user.sex
        form.birthday.data = user.birthday
        form.hometown.data = user.hometown
        form.mp_no.data = user.mp_no
        form.college.data = co.name
    if form.validate_on_submit():
        data = form.data
        user = Student.query.get(session["student"])
        user.hometown = data["hometown"]
        user.mp_no = data["mp_no"]
        try:
            db.session.add(user)
            db.session.commit()
            flash('修改成功！')
            return redirect(url_for("student.userinfo"))
        except:
            flash('修改失败！')
            return redirect(url_for("student.userinfo"))
    if form2.validate_on_submit():
        data = form2.data
        user = Student.query.get(session["student"])
        if not user.check_pwd(data['oldpwd']):
            flash("旧密码有误！")
            return redirect(url_for("student.userinfo"))
        elif data['pwd']!=data['cfpwd']:
            flash("两次密码不一致！")
            return redirect(url_for("student.userinfo"))
        user.pwd = data['pwd']
        try:
            db.session.add(user)
            db.session.commit()
            flash("修改成功！请重新登录！")
            return redirect(url_for("student.logout"))
        except:
            flash("修改失败！")
            return redirect(url_for("student.userinfo"))
    return render_template("student/student-information.html", form=form, form2=form2, user=user)

# 设置
@student.route("/setting", methods=['GET', 'POST'])
@student_login_req
def settings():
    form = SettingForm()
    form2 = informationForm()
    user = Student.query.get(session["student"])
    co = College.query.filter_by(yxh=user.yxh).first()
    if form.validate_on_submit():
        data = form.data
        user = Student.query.get(session["student"])
        if not user.check_pwd(data['oldpwd']):
            flash("旧密码有误！")
            return redirect(url_for("student.settings"))
        elif data['pwd']!=data['cfpwd']:
            flash("两次密码不一致！")
            return redirect(url_for("student.settings"))
        user.pwd = data['pwd']
        try:
            db.session.add(user)
            db.session.commit()
            flash("修改成功！请重新登录！")
            return redirect(url_for("student.logout"))
        except:
            flash("修改失败！")
            return redirect(url_for("student.settings"))
    if request.method == 'GET':
        form2.xh.data = user.xh
        form2.name.data = user.name
        form2.sex.data = user.sex
        form2.birthday.data = user.birthday
        form2.hometown.data = user.hometown
        form2.mp_no.data = user.mp_no
        form2.college.data = co.name
    if form2.validate_on_submit():
        data = form2.data
        user = Student.query.get(session["student"])
        user.hometown = data["hometown"]
        user.mp_no = data["mp_no"]
        print(user.hometown,data["hometown"])
        try:
            db.session.add(user)
            db.session.commit()
            flash('修改成功！')
            return redirect(url_for("student.settings"))
        except:
            flash('修改失败！')
            return redirect(url_for("student.settings"))
    return render_template("student/student-setting.html", form=form, form2=form2, user=user)

# 当前课程
@student.route("/ClassList/<int:page>/<int:page2>/", methods=['GET','POST'])
@student_login_req
def ChosedClassList(page=None,page2=None):
    if page is None:
        page = 1
    if page2 is None:
        page2 = 1
    user = Student.query.get(session["student"])
    seme = Semester.query.filter_by(now = 1).first()
    form = CourseForm()
    if request.method == 'GET':
        form.semester.data = "所有"
    page_data = db.session.query(SelectC, Course, College, Class, Teacher).filter(
        SelectC.xh == user.xh,
        SelectC.kh == Course.kh,
        Course.yxh == College.yxh,
        Class.semester == SelectC.semester,
        Class.semester == seme.semester,
        Class.gh == SelectC.gh,
        Class.kh == SelectC.kh,
        SelectC.gh == Teacher.gh
    ).paginate(page=page, per_page=10)
    page_course = db.session.query(SelectC, Course, College, Class, Teacher).filter(
        SelectC.xh == user.xh,
        SelectC.kh == Course.kh,
        Course.yxh == College.yxh,
        Class.semester == SelectC.semester,
        Class.gh == SelectC.gh,
        Class.kh == SelectC.kh,
        SelectC.gh == Teacher.gh
    ).paginate(page=page, per_page=10)
    if form.validate_on_submit():
        data = form.data
        if data['semester'] != "所有":
            page_course = db.session.query(SelectC, Course, College, Class, Teacher).filter(
                SelectC.xh == user.xh,
                SelectC.kh == Course.kh,
                Course.yxh == College.yxh,
                Class.semester == SelectC.semester,
                Class.semester == data['semester'],
                Class.gh == SelectC.gh,
                Class.kh == SelectC.kh,
                SelectC.gh == Teacher.gh
            ).paginate(page=page, per_page=10)
    return render_template("student/ChosedClass.html", page_data=page_data, page_course=page_course, form=form, seme=seme, user=user)

# 通知详情
@student.route("/informdetail/<string:name>/", methods=['GET','POST'])
@student_login_req
def informdetail(name=None):
    if name == None:
        return redirect(url_for('student.index'))
    seme = Semester.query.filter_by(now = 1).first()
    user = Student.query.get(session["student"])
    inf = Inform.query.filter_by(title=name).first()
    return render_template("student/Informdetail.html",inf = inf, seme = seme, user=user)

# 成绩查询
@student.route("/Grade/<int:page>/", methods=['GET','POST'])
@student_login_req
def Gradedetail(page=None):
    if page == None:
        page = 1
    user = Student.query.get(session["student"])
    seme = Semester.query.filter_by(now = 1).first()
    form = CourseForm()
    if request.method == 'GET':
        form.semester.data = "所有"
    page_data = db.session.query(SelectC, Course, Teacher).filter(
        SelectC.xh == user.xh,
        SelectC.kh == Course.kh,
        SelectC.gh == Teacher.gh
    ).paginate(page=page, per_page=10)
    credit = 0
    grade = 0
    pj = Employee()
    for i in page_data.items:
        credit += i.Course.credit
        if i.SelectC.zpcj==None:
            grade += 0
        else:
            grade += i.Course.credit * i.SelectC.zpcj
    pj.credit = credit
    pj.grade = grade/credit
    if form.validate_on_submit():
        data = form.data
        if data['semester'] != "所有":
            page_data = db.session.query(SelectC, Course, Teacher).filter(
                SelectC.xh == user.xh,
                SelectC.kh == Course.kh,
                SelectC.semester == data['semester'],
                SelectC.gh == Teacher.gh
            ).paginate(page=page, per_page=10)
            credit = 0
            grade = 0
            for i in page_data.items:
                credit += i.Course.credit
                if i.SelectC.zpcj==None:
                    grade += 0
                else:
                    grade += i.Course.credit * i.SelectC.zpcj
            pj.credit = credit
            if credit!=0:
                pj.grade = grade/credit
            else:
                pj.grade = 0
    return render_template("student/Gradedetail.html", pj=pj, page_data=page_data, form=form, seme=seme, user=user)

# 课程查询
@student.route("/Select/<int:page>/", methods=['GET','POST'])
@student_login_req
def selectclass(page=None):
    if page == None:
        page = 1
    user = Student.query.get(session["student"])
    seme = Semester.query.filter_by(now = 1).first()
    form = SearchClass()
    page_data = None
    now = datetime.now()
    seltime = SelectCtime.query.first()
    if now >= seltime.begin and now <= seltime.end:
        print(now,1)
        select = True
        selseme = seltime.semester
    else:
        print(now,2)
        select = False
        selseme = seme.semester
        print(selseme)
    cla = db.session.query(SelectC, Course, College, Class, Teacher).filter(
        SelectC.xh == user.xh,
        SelectC.kh == Course.kh,
        Course.yxh == College.yxh,
        Class.semester == SelectC.semester,
        Class.semester == selseme,
        Class.gh == SelectC.gh,
        Class.kh == SelectC.kh,
        SelectC.gh == Teacher.gh
    ).all()
    if form.validate_on_submit():
        data = form.data
        if data['select']=="课程号":
            print(seme.semester,data["match"])
            page_data = db.session.query(Class,Course,Teacher,College).filter(
                Class.semester == selseme,
                Class.kh == data["match"],
                Class.kh == Course.kh,
                Class.gh == Teacher.gh,
                Course.yxh == College.yxh
            ).paginate(page=page, per_page=10)
            # return redirect(url_for('student.selectclass',page = 1))
        elif data['select']=="课程名":
            page_data = db.session.query(Class,Course,Teacher,College).filter(
                Class.semester == selseme,
                Class.kh == Course.kh,
                Class.gh == Teacher.gh,
                Course.yxh == College.yxh,
                Course.name.like('%'+data["match"]+'%')
            ).paginate(page=page, per_page=10)
            # return redirect(url_for('student.selectclass',page = 1))
        elif data['select']=="学院":
            page_data = db.session.query(Class,Course,Teacher,College).filter(
                Class.semester == selseme,
                Class.kh == Course.kh,
                Class.gh == Teacher.gh,
                Course.yxh == College.yxh,
                College.name.like('%'+data["match"]+'%')
            ).paginate(page=page, per_page=10)
            # return redirect(url_for('student.selectclass',page = 1))
        elif data['select']=="教师号":
            page_data = db.session.query(Class,Course,Teacher,College).filter(
                Class.semester == selseme,
                Class.kh == Course.kh,
                Class.gh == Teacher.gh,
                Course.yxh == College.yxh,
                Class.gh == data["match"]
            ).paginate(page=page, per_page=10)
            # return redirect(url_for('student.selectclass',page = 1))
        else:
            page_data = db.session.query(Class,Course,Teacher,College).filter(
                Class.semester == selseme,
                Class.kh == Course.kh,
                Class.gh == Teacher.gh,
                Course.yxh == College.yxh,
                Teacher.name.like('%'+data["match"]+'%')
            ).paginate(page=page, per_page=10)
            # return redirect(url_for('student.selectclass',page = 1))
    return render_template("student/SelectClass.html", select=select, selseme=selseme, cla = cla, page_data=page_data, form=form, seme=seme, user=user)

# 选课
@student.route("/Chose/<string:kh>/<string:name>/", methods=['GET','POST'])
@student_login_req
def choseclass(kh=None, name=None):
    now = datetime.now()
    seltime = SelectCtime.query.first()
    if now <= seltime.begin or now >= seltime.end:
        flash("当前不在选课时间段内！")
        return redirect(url_for('student.selectclass',page=1))
    cla = db.session.query(Class,Teacher).filter(
        Class.kh == kh,
        Class.gh == Teacher.gh,
        Teacher.name == name
    ).first_or_404()
    user = Student.query.get(session["student"])
    sel = SelectC(
        xh = user.xh,
        semester = cla.Class.semester,
        kh = cla.Class.kh,
        gh = cla.Class.gh,
        pscj = None,
        kscj = None,
        zpcj = None
    )
    try:
        print(db.session.add(sel))
        print(db.session.commit())
        flash("选课成功！")
        return redirect(url_for('student.selectclass',page=1))
    except:
        flash("人数已满,选课失败！")
        return redirect(url_for('student.selectclass',page=1))

# 退课
@student.route("/delete/<string:kh>/<string:name>/", methods=['GET','POST'])
@student_login_req
def delclass(kh=None, name=None):
    now = datetime.now()
    seltime = SelectCtime.query.first()
    if now <= seltime.begin or now >= seltime.end:
        flash("当前不在选课时间段内！")
        return redirect(url_for('student.selectclass',page=1))
    user = Student.query.get(session["student"])
    seme = Semester.query.filter_by(now = 1).first()
    cla = db.session.query(Class,Teacher).filter(
        Class.kh == kh,
        Class.gh == Teacher.gh,
        Teacher.name == name
    ).first_or_404()
    sel = SelectC.query.filter_by(
        semester = seme.semester,
        kh = cla.Class.kh,
        gh = cla.Teacher.gh
    ).first()
    try:
        db.session.delete(sel)
        db.session.commit()
        flash("退课成功！")
        return redirect(url_for('student.selectclass',page=1))
    except:
        flash("退课失败！")
        return redirect(url_for('student.selectclass',page=1))

