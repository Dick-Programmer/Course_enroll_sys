from flask import render_template, redirect, request, url_for, flash, session, jsonify
from . import teacher
from SQL_EA import db
from SQL_EA.modles import Teacher,College,Semester,Inform,SelectC,Course,Class,Student,ApplyCourse
from SQL_EA.teacher.forms import informationForm,SettingForm,CourseForm,ClassApplyForm
from functools import wraps
from datetime import *

# 用作临时结构体
class Employee:
    pass

def teacher_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "teacher" not in session:
            return redirect(url_for("login.index", next = request.url))
        return f(*args, **kwargs)
    return decorated_function

# 首页
@teacher.route("/")
@teacher_login_req
def index():
    seme = Semester.query.filter_by(now = 1).first()
    Date = date.today()
    inf = Inform.query.all()
    user = Teacher.query.get(session["teacher"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    return render_template("teacher/teacher-index.html",apc=apc, seme=seme, inf=inf, date=Date, user = user)

# 登出
@teacher.route("/logout")
@teacher_login_req
def logout():
    session.pop("teacher", None)
    return redirect(url_for("login.index"))

# 个人信息
@teacher.route("/info", methods=['GET', 'POST'])
@teacher_login_req
def userinfo():
    form = informationForm()
    form2 = SettingForm()
    user = Teacher.query.get(session["teacher"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    co = College.query.filter_by(yxh = user.yxh).first()
    form.gh.data = user.gh
    form.name.data = user.name
    form.sex.data = user.sex
    form.birthday.data = user.birthday
    form.education.data = user.education
    form.salary.data = user.salary
    form.college.data = co.name
    if form2.validate_on_submit():
        data = form2.data
        user = Teacher.query.get(session["teacher"])
        if not user.check_pwd(data['oldpwd']):
            flash("旧密码有误！")
            return redirect(url_for("teacher.userinfo"))
        elif data['pwd']!=data['cfpwd']:
            flash("两次密码不一致！")
            return redirect(url_for("teacher.userinfo"))
        user.pwd = data['pwd']
        try:
            db.session.add(user)
            db.session.commit()
            flash("修改成功！请重新登录！")
            return redirect(url_for("teacher.logout"))
        except:
            flash("修改失败！")
            return redirect(url_for("teacher.userinfo"))
    return render_template("teacher/teacher-information.html",apc=apc, form = form, form2 = form2, user = user)

# 设置
@teacher.route("/setting", methods=['GET', 'POST'])
@teacher_login_req
def settings():
    form = SettingForm()
    form2 = informationForm()
    user = Teacher.query.get(session["teacher"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    co = College.query.filter_by(yxh = user.yxh).first()
    form2.gh.data = user.gh
    form2.name.data = user.name
    form2.sex.data = user.sex
    form2.birthday.data = user.birthday
    form2.education.data = user.education
    form2.salary.data = user.salary
    form2.college.data = co.name
    if form.validate_on_submit():
        data = form.data
        user = Teacher.query.get(session["teacher"])
        if not user.check_pwd(data['oldpwd']):
            flash("旧密码有误！")
            return redirect(url_for("teacher.settings"))
        elif data['pwd']!=data['cfpwd']:
            flash("两次密码不一致！")
            return redirect(url_for("teacher.settings"))
        user.pwd = data['pwd']
        try:
            db.session.add(user)
            db.session.commit()
            flash("修改成功！请重新登录！")
            return redirect(url_for("teacher.logout"))
        except:
            flash("修改失败！")
            return redirect(url_for("teacher.settings"))
    return render_template("teacher/teacher-setting.html",apc=apc, form = form, form2 = form2, user = user)


# 通知详情
@teacher.route("/informdetail/<string:name>/", methods=['GET','POST'])
@teacher_login_req
def informdetail(name=None):
    if name == None:
        return redirect(url_for('teacher.index'))
    seme = Semester.query.filter_by(now = 1).first()
    user = Teacher.query.get(session["teacher"])
    inf = Inform.query.filter_by(title=name).first()
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    return render_template("teacher/Informdetail.html",apc=apc, inf = inf, seme = seme, user = user)

# 已开课程
@teacher.route("/MyClass/<int:page>/", methods=['GET','POST'])
@teacher_login_req
def myclass(page=None):
    if page == None:
        page = 1
    form = CourseForm()
    if request.method == 'GET':
        form.semester.data = "所有"
    seme = Semester.query.filter_by(now = 1).first()
    user = Teacher.query.get(session["teacher"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    page_data = db.session.query(Class, Course).filter(
        Class.kh == Course.kh,
        Class.gh == user.gh
    ).paginate(page=page, per_page=10)
    if form.validate_on_submit():
        data = form.data
        if data['semester']!='所有':
            page_data = db.session.query(Class, Course).filter(
                Class.semester == data['semester'],
                Class.kh == Course.kh,
                Class.gh == user.gh
            ).paginate(page=page, per_page=10)
    return render_template("teacher/Myclass.html",apc=apc, page_data=page_data, form = form, seme = seme, user = user)

# 课程详情
@teacher.route("/Classdetail/<int:kh>/<string:semes>/", methods=['GET','POST'])
@teacher_login_req
def classdetail(kh=None,semes=None):
    cladetail = Employee()    
    seme = Semester.query.filter_by(now = 1).first()
    user = Teacher.query.get(session["teacher"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    cla = db.session.query(Class,Course).filter(
        Class.kh == kh,
        Class.kh == Course.kh,
        Class.gh == user.gh,
        Class.semester == semes
    ).first()
    page_data = db.session.query(SelectC, Student).filter(
        SelectC.xh == Student.xh,
        SelectC.gh == user.gh,
        SelectC.semester == semes
    ).all()
    if len(page_data) == 0:
        cladetail.pj = 0
        cladetail.passed = 0
        cladetail.excellent = 0
        cladetail.failed = 0
        cladetail.passrate = 0
        cladetail.exrate = 0
        cladetail.count = 0
    else:
        cladetail.excellent = db.session.query(SelectC, Student).filter(
            SelectC.xh == Student.xh,
            SelectC.gh == user.gh,
            SelectC.semester == semes,
            SelectC.zpcj>80
        ).count()
        cladetail.failed = db.session.query(SelectC, Student).filter(
            SelectC.xh == Student.xh,
            SelectC.gh == user.gh,
            SelectC.semester == semes,
            SelectC.zpcj<60
        ).count()
        count = 0
        grade = 0
        for i in page_data:
            count += 1
            if i.SelectC.zpcj==None:
                grade += 0
            else:
                grade += i.SelectC.zpcj
        cladetail.pj = grade/count
        cladetail.passed = count - cladetail.failed
        cladetail.passrate = cladetail.passed/count
        cladetail.exrate = cladetail.excellent/count
        cladetail.count = count
        print(cladetail.pj,cladetail.passed,cladetail.passrate,cladetail.exrate,cladetail.count)
    return render_template("teacher/Classdetail.html",apc=apc, page_data=page_data, cladetail=cladetail, cla = cla, seme = seme, user = user)

# 编辑成绩
@teacher.route("/editgrade", methods=['GET','POST'])
@teacher_login_req
def editgrade():
    if request.method == 'POST':
        form = request.json
        sel = SelectC.query.filter_by(
            semester = form['seme'],
            kh = form['kh'],
            xh = form['xh']
        ).first()
        sel.pscj = form['pscj']
        sel.kscj = form['kscj']
        sql = "call update_zpcj('"+form['seme']+"');"
        try:
            db.session.add(sel)
            db.session.commit()
            db.session.execute(sql)
            zpcj = SelectC.query.filter_by(
                semester = form['seme'],
                kh = form['kh'],
                xh = form['xh']
            ).first().zpcj
            return jsonify(result = "SUCC",zpcj = zpcj)
        except:
            return jsonify(result = "ERR2")

# 开课申请
@teacher.route("/Classapply", methods=['GET','POST'])
@teacher_login_req
def classapply():
    seme = Semester.query.filter_by(now = 1).first()
    user = Teacher.query.get(session["teacher"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh==user.gh,
        Teacher.gh==ApplyCourse.gh
    ).all()
    apc.undo = ApplyCourse.query.filter_by(status=1).count()
    apc.undo += ApplyCourse.query.filter_by(status=2).count()
    form = ClassApplyForm()
    myapply = ApplyCourse.query.filter_by(gh=user.gh).all()
    if form.validate_on_submit():
        data = form.data
        afc = ApplyCourse(
            gh = user.gh,
            name = data['name'],
            credit = data['credit'],
            period = data['period'],
            psrate = data['psrate'],
            yxh = user.yxh,
            detail = data['describe'],
            time = datetime.now(),
            status = 0
        )
        try:
            db.session.add(afc)
            db.session.commit()
            flash("提交成功！")
        except:
            flash("提交失败！")
        return redirect(url_for('teacher.classapply'))
    return render_template("teacher/ClassApply.html",apc=apc, myapply=myapply, form = form, seme = seme, user = user)

# 查看申请
@teacher.route("/Checkapply/<int:gh>/<string:name>", methods=['GET','POST'])
@teacher_login_req
def checkapply(gh=None,name=None):
    apcde = ApplyCourse.query.filter_by(
        gh = gh,
        name = name
    ).first()
    if apcde.status == 1:
        apcde.status = 3
    elif apcde.status == 2:
        apcde.status = 4
    db.session.add(apcde)
    db.session.commit()

    return redirect(url_for('teacher.classapply'))
