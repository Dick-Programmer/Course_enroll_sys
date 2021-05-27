from datetime import datetime

from SQL_EA import db


# 学院
class College(db.Model):
    __tablename__ = "s_College"
    yxh = db.Column(db.String(2), primary_key=True)  # 院系号
    name = db.Column(db.String(50))  # 名称
    adress = db.Column(db.String(100))  # 地址
    p_no = db.Column(db.String(8))  # 电话号码

    def __repr__(self):
        return "<College %r>" % self.name


# 学生
class Student(db.Model):
    __tablename__ = "s_Student"
    xh = db.Column(db.String(8), primary_key=True)  # 学号
    name = db.Column(db.String(20))  # 姓名
    sex = db.Column(db.String(10))  # 性别
    birthday = db.Column(db.Date)  # 出生日期
    hometown = db.Column(db.String(10))  # 籍贯
    mp_no = db.Column(db.String(11))  # 手机号码
    yxh = db.Column(db.String(2), db.ForeignKey(College.yxh))  # 院系号
    pwd = db.Column(db.String(16))  # 密码
    # userlogs = db.relationship('Studentlog', backref='student')

    def __repr__(self):
        return "<Student %r %r>" % (self.xh, self.name)

    def check_pwd(self, pwd):
        return self.pwd == pwd


# 学生登陆日志
class Studentlog(db.Model):
    __tablename__ = "studentlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    xh = db.Column(db.String(8), db.ForeignKey(Student.xh))  # 所属学生学号
    ip = db.Column(db.String(100))  # 登陆IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Studentlog %r>" % self.id


# 老师
class Teacher(db.Model):
    __tablename__ = "s_Teacher"
    gh = db.Column(db.String(4), primary_key=True)  # 工号
    name = db.Column(db.String(20))  # 姓名
    sex = db.Column(db.String(10))  # 性别
    birthday = db.Column(db.Date)  # 出生日期
    education = db.Column(db.String(10))  # 学历
    salary = db.Column(db.DECIMAL(7, 2))  # 基本工资
    yxh = db.Column(db.String(2), db.ForeignKey(College.yxh))  # 院系号
    pwd = db.Column(db.String(16))  # 密码
    # userlogs = db.relationship('Teacherlog', backref='teacher')

    def __repr__(self):
        return "<Teacher %r %r>" % (self.gh, self.name)

    def check_pwd(self, pwd):
        return self.pwd == pwd


# 老师登陆日志
class Teacherlog(db.Model):
    __tablename__ = "teacherlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    gh = db.Column(db.String(8), db.ForeignKey(Teacher.gh))  # 所属教师工号
    ip = db.Column(db.String(100))  # 登陆IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Teachertlog %r>" % self.id


# 管理员
class Manager(db.Model):
    __tablename__ = "s_Manager"
    gh = db.Column(db.String(5), primary_key=True)  # 工号
    pwd = db.Column(db.String(16))  # 密码

    def __repr__(self):
        return "<Manager %r>" % self.gh

    def check_pwd(self, pwd):
        return self.pwd == pwd


# 管理员登陆日志
class Manangerlog(db.Model):
    __tablename__ = "managerlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    gh = db.Column(db.String(8), db.ForeignKey(Manager.gh))  # 所属管理员工号
    ip = db.Column(db.String(100))  # 登陆IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Teachertlog %r>" % self.id


# 课程
class Course(db.Model):
    __tablename__ = "s_Course"
    kh = db.Column(db.String(8), primary_key=True)  # 课程号
    name = db.Column(db.String(20))  # 课程名
    credit = db.Column(db.SMALLINT)  # 学分
    period = db.Column(db.SMALLINT)  # 学时
    psrate = db.Column(db.Float)     # 平时分比例
    yxh = db.Column(db.String(2), db.ForeignKey(College.yxh))  # 院系号

    def __repr__(self):
        return "<Course %r>" % self.name


# 开课
class Class(db.Model):
    __tablename__ = "s_Class"
    semester = db.Column(db.String(14), primary_key=True)  # 学期
    kh = db.Column(db.String(8), db.ForeignKey(Course.kh), primary_key=True)  # 课程号
    gh = db.Column(db.String(4), db.ForeignKey(Teacher.gh), primary_key=True)  # 教师工号
    class_time = db.Column(db.String(12))   # 上课时间
    maxsize = db.Column(db.SMALLINT)        # 最大容量
    nowsize = db.Column(db.SMALLINT)        # 现在容量

    def __repr__(self):
        return "<Class %r %r %r>" % (self.semester, self.kh, self.gh)


# 选课
class SelectC(db.Model):
    __tablename__ = "s_SelectC"
    xh = db.Column(db.String(8), db.ForeignKey(Student.xh), primary_key=True)  # 学号
    semester = db.Column(db.String(14), primary_key=True)  # 学期
    kh = db.Column(db.String(8), db.ForeignKey(Course.kh), primary_key=True)  # 课程号
    gh = db.Column(db.String(4), db.ForeignKey(Teacher.gh), primary_key=True)  # 教师工号
    pscj = db.Column(db.SMALLINT)  # 平时成绩
    kscj = db.Column(db.SMALLINT)  # 考试成绩
    zpcj = db.Column(db.SMALLINT)  # 总评成绩

    def __repr__(self):
        return "<SelectC %r %r %r %r>" % (self.semester, self.xh, self.kh, self.gh)

# 学期
class Semester(db.Model):
    __tablename__ = "s_Semester"
    semester = db.Column(db.String(14),primary_key=True) # 学期
    weeks = db.Column(db.String(6))  # 当前周
    now = db.Column(db.SMALLINT) # 是否为当前学期

    def __repr__(self):
        return "<Semester %r>" % (self.semester)

# 选课时间
class SelectCtime(db.Model):
    __tablename__ = "s_SelectCtime"
    semester = db.Column(db.String(14),primary_key=True) # 学期
    begin = db.Column(db.DateTime)  # 开始时间
    end = db.Column(db.DateTime) # 结束时间

    def __repr__(self):
        return "<SelectCtime %r %r %r>" % (self.semester,self.begin,self.end)

# 通知
class Inform(db.Model):
    __tablename__ = "s_Inform"
    gh = db.Column(db.String(5), db.ForeignKey(Manager.gh), primary_key=True)  # 工号
    title = db.Column(db.String(100),primary_key=True) # 标题
    time = db.Column(db.DateTime)  # 发布时间
    preview = db.Column(db.Text) # 内容预览
    detail = db.Column(db.Text) # 内容

    def __repr__(self):
        return "<Inform %r>" % (self.title)

# 申请开课表
class ApplyCourse(db.Model):
    __tablename__ = "ApplyCourse"
    gh = db.Column(db.String(5), db.ForeignKey(Teacher.gh), primary_key=True)  # 工号
    name = db.Column(db.String(20),primary_key=True) # 课程名
    credit = db.Column(db.SMALLINT)  # 学分
    period = db.Column(db.SMALLINT)  # 学时
    psrate = db.Column(db.Float)     # 平时分比例
    yxh = db.Column(db.String(2), db.ForeignKey(College.yxh))  # 院系号
    time = db.Column(db.DateTime)  # 申请时间
    detail = db.Column(db.Text) # 课程描述
    status = db.Column(db.SMALLINT) # 状态

    def __repr__(self):
        return "<ApplyCourse %r>" % (self.name)

