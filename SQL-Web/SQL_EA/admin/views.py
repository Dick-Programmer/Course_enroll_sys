from functools import wraps

from flask import render_template, redirect, url_for, session, request, flash, jsonify

from SQL_EA import db
from SQL_EA.admin.forms import InformForm, AddCollege, AddTeacher, AddStudent,SemesterForm,AddSemester,AddSelectC, AddCourse, AddClass, SetSelectCtime,SettingForm
from SQL_EA.modles import Manager, College, Teacher, Student, SelectC, Course, Class, Semester, Inform, SelectCtime, ApplyCourse
from . import admin
import decimal
from datetime import *

# 用作临时结构体
class Employee:
    pass

def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "manager" not in session:
            return redirect(url_for("login.index", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

@admin.route("/")
@admin_login_req
def index():
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    username = user.gh
    Date = date.today()
    inf = Inform.query.all()
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    return render_template("admin/admin-index.html", apc=apc, inf=inf, seme = seme, username=username, date=Date)

# 登出
@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("manager", None)
    return redirect(url_for("login.index"))

# 设置
@admin.route("/setting", methods=['GET', 'POST'])
@admin_login_req
def settings():
    form = SettingForm()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    if form.validate_on_submit():
        data = form.data
        user = Manager.query.get(session["manager"])
        if not user.check_pwd(data['oldpwd']):
            flash("旧密码有误！")
            return redirect(url_for("admin.settings"))
        elif data['pwd']!=data['cfpwd']:
            flash("两次密码不一致！")
            return redirect(url_for("admin.settings"))
        user.pwd = data['pwd']
        try:
            db.session.add(user)
            db.session.commit()
            flash("修改成功！请重新登录！")
            return redirect(url_for("admin.logout"))
        except:
            flash("修改失败！")
            return redirect(url_for("admin.settings"))
    return render_template("admin/admin-setting.html",apc=apc, form = form, username = user.gh)

# 管理学院信息
@admin.route("/collegesetting/<int:page>/", methods=['GET','POST'])
@admin_login_req
def collegesetting(page=None):
    if page is None:
        page = 1
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    page_data = College.query.paginate(page=page, per_page=10)
    form = AddCollege()
    if form.validate_on_submit():
        data = form.data
        count = College.query.filter_by(yxh=data['yxh']).count()
        if count == 0:
            col = College(
                yxh = data["yxh"],
                name = data["name"],
                adress = data["address"],
                p_no = data["p_no"]
            )
            try:
                db.session.add(col)
                db.session.commit()
                flash("添加成功！")
                return redirect(url_for('admin.collegesetting',page = page))
            except:
                flash("添加失败！")
                return redirect(url_for('admin.collegesetting',page = page))
        else:
            flash("学院号已存在，请重新输入！")
            return redirect(url_for('admin.collegesetting',page = page))
    return render_template("admin/Set-college.html",apc=apc, form = form, page_data=page_data, seme= seme, username=user.gh)

# 编辑学院信息
@admin.route("/editcollege", methods=['GET','POST'])
@admin_login_req
def editcollege(yxh = None):
    if request.method == 'POST':
        form = request.json
        col = College.query.filter_by(yxh=form['origin']).first_or_404()
        count = College.query.filter_by(yxh=form['yxh']).count()
        if form['yxh']!=col.yxh and count == 1:
            return jsonify(result = "ERR1") 
        col.yxh = form['yxh']
        col.name = form['name']
        col.adress = form['adress']
        col.p_no = form['phone']
        try:
            db.session.add(col)
            db.session.commit()
            return jsonify(result = "SUCC")
        except:
            return jsonify(result = "ERR2")
    

# 删除学院信息
@admin.route("/collegedelete/<int:yxh>/", methods=['GET'])
@admin_login_req
def collegedel(yxh = None):
    col = College.query.filter_by(yxh=yxh).first_or_404()
    try:
        db.session.delete(col)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.collegesetting",page=1))
    

# 管理教师信息
@admin.route("/teachersetting/<int:page>/", methods=['GET','POST'])
@admin_login_req
def teachersetting(page=None):
    if page is None:
        page = 1
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    page_data = db.session.query(College, Teacher).filter(
        Teacher.yxh == College.yxh,
    ).paginate(page=page, per_page=10)
    form = AddTeacher()
    if form.validate_on_submit():
        data = form.data
        count = Teacher.query.filter_by(gh=data['gh']).count()
        if count == 0:
            tea = Teacher(
                gh = data["gh"],
                name = data["name"],
                sex = data["sex"],
                birthday = data["birthday"],
                education = data["education"],
                salary = data["salary"],
                yxh = data["college"],
                pwd = data["gh"]
            )
            try:
                db.session.add(tea)
                db.session.commit()
                flash("添加成功！")
                return redirect(url_for('admin.teachersetting',page = page))
            except:
                flash("添加失败！")
                return redirect(url_for('admin.teachersetting',page = page))
        else:
            flash("工号已存在，请重新输入！")
            return redirect(url_for('admin.teachersetting',page = page))
    return render_template("admin/Set-teacher.html",apc=apc, page_data=page_data, form=form, seme=seme, username=user.gh)

# 编辑教师信息
@admin.route("/editteacher", methods=['GET','POST'])
@admin_login_req
def editteacher():
    if request.method == 'POST':
        form = request.json
        tea = Teacher.query.filter_by(gh=form['origin']).first_or_404()
        count = Teacher.query.filter_by(gh=form['gh']).count()
        if form['gh']!=tea.gh and count == 1:
            return jsonify(result = "ERR1") 
        yx = College.query.filter_by(name=form['college']).first()
        tea.gh = form['gh']
        tea.name = form['name']
        tea.sex = form['sex']
        tea.birthday = form['birthday']
        tea.education = form['education']
        tea.salary = form['salary']
        tea.yxh = yx.yxh
        try:
            db.session.add(tea)
            db.session.commit()
            return jsonify(result = "SUCC")
        except:
            return jsonify(result = "ERR2")
    
# 删除教师信息
@admin.route("/teacherdelete/<int:gh>/", methods=['GET'])
@admin_login_req
def teacherdel(gh = None):
    tea = Teacher.query.filter_by(gh=gh).first_or_404()
    try:
        db.session.delete(tea)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.teachersetting",page=1))

# 管理学生信息
@admin.route("/studentsetting/<int:page>/", methods=['GET','POST'])
@admin_login_req
def studentsetting(page=None):
    if page is None:
        page = 1
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    page_data = db.session.query(College, Student).filter(
        Student.yxh == College.yxh,
    ).paginate(page=page, per_page=10)
    form = AddStudent()
    if form.validate_on_submit():
        data = form.data
        count = Student.query.filter_by(xh=data['xh']).count()
        if count == 0:
            stu = Student(
                xh = data["xh"],
                name = data["name"],
                sex = data["sex"],
                birthday = data["birthday"],
                hometown = data["hometown"],
                mp_no = data["mp_no"],
                yxh = data["college"],
                pwd = data["xh"]
            )
            try:
                db.session.add(stu)
                db.session.commit()
                flash("添加成功！")
                return redirect(url_for('admin.studentsetting',page = page))
            except:
                flash("添加失败！")
                return redirect(url_for('admin.studentsetting',page = page))
        else:
            flash("学号已存在，请重新输入！")
            return redirect(url_for('admin.studentsetting',page = page))
    return render_template("admin/Set-student.html",apc=apc, page_data=page_data, form=form, seme=seme, username=user.gh)

# 编辑学生信息
@admin.route("/editstudent", methods=['GET','POST'])
@admin_login_req
def editstudent():
    if request.method == 'POST':
        form = request.json
        stu = Student.query.filter_by(xh=form['origin']).first_or_404()
        count = Student.query.filter_by(xh=form['xh']).count()
        if form['xh']!=stu.xh and count == 1:
            return jsonify(result = "ERR1") 
        yx = College.query.filter_by(name=form['college']).first()
        stu.xh = form['xh']
        stu.name = form['name']
        stu.sex = form['sex']
        stu.birthday = form['birthday']
        stu.hometown = form['hometown']
        stu.mp_no = form['phone']
        stu.yxh = yx.yxh
        try:
            db.session.add(stu)
            db.session.commit()
            return jsonify(result = "SUCC")
        except:
            return jsonify(result = "ERR2")
    
# 删除学生信息
@admin.route("/studentdelete/<int:xh>/", methods=['GET'])
@admin_login_req
def studentdel(xh = None):
    stu = Student.query.filter_by(xh=xh).first_or_404()
    try:
        db.session.delete(stu)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.studentsetting",page=1))

# 管理学期信息
@admin.route("/semestersetting", methods=['GET','POST'])
@admin_login_req
def semestersetting():
    form = SemesterForm()
    form2 = AddSemester()
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    if request.method == 'GET':
        form.semester.data = seme.semester
        form.weeks.data = seme.weeks
    if form.validate_on_submit():
        data = form.data
        now = Semester.query.filter_by(now = 1).first()
        if now.semester != data['semester']:
            now.now = 0
            now.weeks = ""
            now = Semester.query.filter_by(semester = data['semester']).first()
            now.now = 1
        now.weeks = data['weeks']
        try:
            db.session.add(now)
            db.session.commit()
            flash("修改成功！")
        except:
            flash("修改失败！")
        return redirect(url_for('admin.semestersetting'))
    if form2.validate_on_submit():  
        data = form2.data
        if len(data['studyyears'])!=9:
            flash("输入有误！请重新输入！")
            return redirect(url_for('admin.semestersetting'))
        else:
            a = Semester(
                semester = data['studyyears'] +" 秋季",
                weeks = "",
                now = 0
            )
            b = Semester(
                semester = data['studyyears'] +" 冬季",
                weeks = "",
                now = 0
            )
            c = Semester(
                semester = data['studyyears'] +" 春季",
                weeks = "",
                now = 0
            )
            d = Semester(
                semester = data['studyyears'] +" 夏季",
                weeks = "",
                now = 0
            )
            try:
                db.session.add(a)
                db.session.add(b)
                db.session.add(c)
                db.session.add(d)
                db.session.commit()
                flash("添加成功！")
            except:
                flash("添加失败！")
            return redirect(url_for('admin.semestersetting'))
    return render_template("admin/Set-semester.html",apc=apc, form = form, form2 = form2, seme=seme, username=user.gh)

# 管理选课信息
@admin.route("/selectCsetting/<int:page>/", methods=['GET','POST'])
@admin_login_req
def selectCsetting(page=None):
    if page is None:
        page = 1
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    page_data = SelectC.query.paginate(page=page, per_page=10)
    form = AddSelectC()
    if form.validate_on_submit():
        data = form.data
        countC = SelectC.query.filter_by(xh=data['xh'],kh=data['kh'],semester=data['semester']).count()
        countS = Student.query.filter_by(xh=data['xh']).count()
        if countS != 0 and countC == 0:
            cla = Class.query.filter_by(kh=data['kh'],semester=data['semester']).first()
            if cla == None:
                flash("未开此课程！")
                return redirect(url_for('admin.selectCsetting',page = page))
            sc = SelectC(
                xh = data["xh"],
                kh = data["kh"],
                semester = data["semester"],
                gh = cla.gh
            )
            try:
                db.session.add(sc)
                db.session.commit()
                flash("添加成功！")
                return redirect(url_for('admin.selectCsetting',page = page))
            except:
                flash("添加失败！")
                return redirect(url_for('admin.selectCsetting',page = page))
        elif countS ==0:
            flash("学号不存在！")
            return redirect(url_for('admin.selectCsetting',page = page))
        else:
            flash("选课已存在，请重新输入！")
            return redirect(url_for('admin.selectCsetting',page = page))
    return render_template("admin/Set-selectC.html",apc=apc, form = form, page_data=page_data, seme= seme, username=user.gh)

# 删除选课信息
@admin.route("/selecCdelete/<int:xh>/<int:kh>/<string:semester>/", methods=['GET'])
@admin_login_req
def selectCdel(xh = None,kh = None,semester = None):
    sc = SelectC.query.filter_by(xh=xh,kh=kh,semester=semester).first_or_404()
    try:
        db.session.delete(sc)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.selectCsetting",page=1))

# 管理课程信息
@admin.route("/classsetting/<int:page>/<int:page2>/", methods=['GET','POST'])
@admin_login_req
def classsetting(page=None,page2=None):
    if page is None:
        page = 1
    if page2 is None:
        page2 = 1
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    page_data = Course.query.paginate(page=page, per_page=10)
    page_data2 = Class.query.paginate(page=page2, per_page=10)
    form = AddCourse()
    form2 = AddClass()
    if form.validate_on_submit():
        data = form.data
        col = College.query.filter_by(name = data['yxh']).first()
        cou = Course(
            kh = data['kh'],
            name = data['name'],
            credit = data['credit'],
            period = data['period'],
            pjrate = data['pjrate'],
            yxh = col.yxh
        )
        try:
            db.session.add(cou)
            db.session.commit()
            flash("添加成功！")
            return redirect(url_for('admin.classsetting',page = page))
        except:
            flash("添加失败！")
            return redirect(url_for('admin.classsetting',page = page))
    if form2.validate_on_submit():
        data = form2.data
        countC = Class.query.filter_by(gh=data['gh'],kh=data['kh'],semester=data['semester']).count()
        countT = Teacher.query.filter_by(gh=data['gh']).count()
        if countT != 0 and countC == 0:
            cou = Course.query.filter_by(kh=data['kh']).first()
            if cou == None:
                flash("课程库中没有此课程！")
                return redirect(url_for('admin.classsetting',page = page, page2 = page2))
            cla = Class(
                gh = data["gh"],
                kh = data["kh"],
                semester = data["semester"],
                class_time = data["time"],
                maxsize = data['maxsize'],
                nowsize = 0
            )
            try:
                db.session.add(cla)
                db.session.commit()
                flash("添加成功！")
                return redirect(url_for('admin.classsetting',page = page, page2 = page2))
            except:
                flash("添加失败！")
                return redirect(url_for('admin.classsetting',page = page, page2 = page2))
        elif countT ==0:
            flash("工号不存在！")
            return redirect(url_for('admin.classsetting',page = page, page2 = page2))
        else:
            flash("此课程已存在，请重新输入！")
            return redirect(url_for('admin.classsetting',page = page, page2 = page2))
    return render_template("admin/Set-class.html",apc=apc, form = form, form2=form2, page_data=page_data, page_data2=page_data2, seme= seme, username=user.gh)

# 删除课程信息
@admin.route("/coursedelete/<int:kh>/", methods=['GET'])
@admin_login_req
def coursedel(kh = None):
    cou = Course.query.filter_by(kh=kh).first_or_404()
    try:
        db.session.delete(cou)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.classsetting",page=1,page2=1))

# 删除选课信息
@admin.route("/classdelete/<int:gh>/<int:kh>/<string:semester>/", methods=['GET'])
@admin_login_req
def classdel(gh = None,kh = None,semester = None):
    sc = Class.query.filter_by(gh=gh,kh=kh,semester=semester).first_or_404()
    try:
        db.session.delete(sc)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.classsetting",page=1,page2=1))

# 选课时间
@admin.route("/selectCtimesetting", methods=['GET','POST'])
@admin_login_req
def setselectCtime():
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    form = SetSelectCtime()
    nowsel = SelectCtime.query.first()
    if form.validate_on_submit():
        data = form.data
        print(data['begin'],data['end'])
        seltime = SelectCtime.query.first()
        seltime.semester = data['semester']
        seltime.begin = data['begin']
        seltime.end = data['end']
        try:
            db.session.add(seltime)
            db.session.commit()
            flash("设置成功")
        except:
            flash("设置失败")
        return redirect(url_for('admin.setselectCtime'))
    return render_template("admin/Set-selectCtime.html",apc=apc, nowsel=nowsel, form=form, seme=seme, username=user.gh)

# 编辑发布通知
@admin.route("/editinform", methods=['GET','POST'])
@admin_login_req
def informedit():
    form = InformForm()
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    if form.validate_on_submit():
        data = form.data
        pre = data['editor1'][0:99]
        inf = Inform(
            gh = user.gh,
            title = data['title'],
            time = datetime.utcnow(),
            detail = data['editor1'],
            preview = pre
        )
        try:
            db.session.add(inf)
            db.session.commit()
            flash("发布成功！")
        except:
            flash("发布失败！")
        return redirect(url_for('admin.informedit'))
    return render_template("admin/Sendinform.html",apc=apc, form=form, seme=seme, username=user.gh)

# 查看历史通知
@admin.route("/historicinform", methods=['GET'])
@admin_login_req
def historicinform():
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    username = user.gh
    inf = Inform.query.all()
    panel = {
        1:"panel panel-solid-danger",
        2:"panel panel-solid-warning",
        3:"panel panel-solid-success",
        4:"panel panel-solid-info"
    }
    return render_template("admin/Historicinform.html",apc=apc, inf=inf, panel=panel, seme = seme, username=username)

# 通知详情
@admin.route("/informdetail/<string:name>/", methods=['GET','POST'])
@admin_login_req
def informdetail(name=None):
    if name == None:
        return redirect(url_for('admin.index'))
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    inf = Inform.query.filter_by(title=name).first()
    return render_template("admin/Informdetail.html",apc=apc, inf = inf, seme = seme, username=user.gh)

# 删除通知
@admin.route("/infodelete/<int:gh>/<string:title>/", methods=['GET'])
@admin_login_req
def informdel(gh = None, title = None):
    inf = Inform.query.filter_by(gh=gh,title=title).first_or_404()
    try:
        db.session.delete(inf)
        db.session.commit()
        flash("删除成功！")
    except:
        flash("数据删除失败！")
    return redirect(url_for("admin.historicinform"))

# 申请列表
@admin.route("/ApplyforCourse", methods=['GET','POST'])
@admin_login_req
def applyforcourse():
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    return render_template("admin/Allapply.html",apc=apc, seme = seme, username=user.gh)

# 申请详情
@admin.route("/Applydetail/<int:gh>/<string:name>/", methods=['GET','POST'])
@admin_login_req
def applydetail(gh = None,name = None):
    seme = Semester.query.filter_by(now = 1).first()
    user = Manager.query.get(session["manager"])
    apc = Employee()
    apc.apc = db.session.query(ApplyCourse,Teacher).filter(Teacher.gh==ApplyCourse.gh).all()
    apc.undo = ApplyCourse.query.filter_by(status=0).count()
    apcde = db.session.query(ApplyCourse,Teacher).filter(
        ApplyCourse.gh == gh,
        ApplyCourse.name == name,
        Teacher.gh == ApplyCourse.gh
    ).first()
    return render_template("admin/Applydetail.html",apc=apc, apcde=apcde, seme = seme, username=user.gh)

# 拒绝申请
@admin.route("/Applyignore/<string:gh>/<string:name>/", methods=['GET','POST'])
@admin_login_req
def applyignore(gh = None,name = None):
    apcde = ApplyCourse.query.filter_by(
        gh = gh,
        name = name
    ).first()
    apcde.status = 2
    try:
        db.session.add(apcde)
        db.session.commit()
        flash("已拒绝申请")
    except:
        flash("发生错误！请重试！")
    return redirect(url_for('admin.applydetail',gh = gh, name=name))

# 允许申请
@admin.route("/Applyallow", methods=['GET','POST'])
@admin_login_req
def applyallow():
    if request.method == 'POST':
        form = request.json
        count = Course.query.filter_by(kh=form['kh']).count()
        if count != 0:
            return jsonify(result = "ERR1") 
        apcde = ApplyCourse.query.filter_by(
            gh = form['gh'],
            name = form['name'],
        ).first()
        apcde.status = 1
        cou = Course(
            kh = form['kh'],
            name = apcde.name,
            credit = apcde.credit,
            period = apcde.period,
            psrate = apcde.psrate,
            yxh = apcde.yxh
        )
        try:
            db.session.add(cou)
            db.session.commit()
            return jsonify(result = "SUCC")
        except:
            return jsonify(result = "ERR2")



