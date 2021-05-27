from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField,StringField, DateTimeField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,ValidationError
from SQL_EA.modles import Semester, College

class SettingForm(FlaskForm):
    """更改密码"""
    oldpwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
            "required": "required"
        }
    )
    cfpwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请确认密码")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请确认密码",
            "required": "required"
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            "class": "form-control btn btn-info"
        }
    )

class InformForm(FlaskForm):
    """通知发布"""
    title = StringField(
        label='标题：',
        validators=[
            DataRequired("请输入标题！"),
        ],
        description="标题",
        render_kw={
            "placeholder": "请输入标题",
            "required": "required",
            "width":"100%"
        }
    )
    editor1 = TextAreaField(
        label='内容',
        validators=[
            DataRequired("请输入内容！"),
        ],
        description="内容",
        render_kw={
            "id": "editor1",
            "rows": "10",
            "cols": "80",
            "placeholder": "请输入内容...",
            "style": "width: 100%; height: 200px"
        }
    )
    submit = SubmitField(
        '发布',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class AddCollege(FlaskForm):
    """添加学院"""
    yxh = StringField(
        label="学院号",
        validators=[
            DataRequired("请输入学院号")
        ],
        description="学院号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学院号(两位数)",
            "required": "required"
        }
    )
    name = StringField(
        label="学院名",
        validators=[
            DataRequired("请输入学院名")
        ],
        description="学院名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学院名",
            "required": "required"
        }
    )
    address = StringField(
        label="地址",
        validators=[
            DataRequired("请输入地址")
        ],
        description="地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地址",
            "required": "required"
        }
    )
    p_no = StringField(
        label="电话",
        validators=[
            DataRequired("请输入电话")
        ],
        description="电话",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入电话(8位)",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class AddTeacher(FlaskForm):
    """添加老师"""
    gh = StringField(
        label="工号",
        validators=[
            DataRequired("请输入工号")
        ],
        description="工号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入工号",
            "required": "required"
        }
    )
    name = StringField(
        label="姓名",
        validators=[
            DataRequired("请输入姓名")
        ],
        description="姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入姓名",
        }
    )
    sex = SelectField(
        label="性别",
        validators=[
            DataRequired("请选择性别")
        ],
        description="性别",
        choices=[
            ('','请选择性别'),
            ('男','男'),
            ('女','女')
        ],
        render_kw={
            "class":"ui-select"
        }
    )
    birthday = StringField(
        label="生日",
        validators=[
            DataRequired("请输入生日")
        ],
        description="生日",
        render_kw={
            "class": "form-control",
            "placeholder": "例：1990-01-01",
        }
    )
    education = StringField(
        label="职位",
        validators=[
            DataRequired("请输入职位")
        ],
        description="职位",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入职位",
        }
    )
    salary = StringField(
        label="基本工资",
        validators=[
            DataRequired("请输入基本工资")
        ],
        description="基本工资",
        render_kw={
            "class": "form-control",
            "placeholder": "数字,小数保留后两位",
        }
    )
    college = StringField(
        label="学院",
        validators=[
            DataRequired("请输入学院")
        ],
        description="学院",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学院号",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class AddStudent(FlaskForm):
    """添加学生"""
    xh = StringField(
        label="学号",
        validators=[
            DataRequired("请输入学号")
        ],
        description="学号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学号",
            "required": "required"
        }
    )
    name = StringField(
        label="姓名",
        validators=[
            DataRequired("请输入姓名")
        ],
        description="姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入姓名",
        }
    )
    sex = SelectField(
        label="性别",
        validators=[
            DataRequired("请选择性别")
        ],
        description="性别",
        choices=[
            ('','请选择性别'),
            ('男','男'),
            ('女','女')
        ],
        render_kw={
            "class":"ui-select"
        }
    )
    birthday = StringField(
        label="生日",
        validators=[
            DataRequired("请输入生日")
        ],
        description="生日",
        render_kw={
            "class": "form-control",
            "placeholder": "例：1990-01-01",
        }
    )
    hometown = StringField(
        label="籍贯",
        validators=[
            DataRequired("请输入籍贯")
        ],
        description="籍贯",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入籍贯",
        }
    )
    mp_no = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号码",
        }
    )
    college = StringField(
        label="学院",
        validators=[
            DataRequired("请勿更改")
        ],
        description="学院",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学院号",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class SemesterForm(FlaskForm):
    """学期"""
    def query_factory():
        return [r.semester for r in  Semester.query.all()] 

    def get_pk(obj):
        return obj
    semesters = [(r.semester,r.semester) for r in  Semester.query.all()] 
    semester = QuerySelectField(
        label="当前学期",
        validators=[
            DataRequired("请选择当前学期")
        ],
        description="学期",
        # choices=semesters,
        query_factory=query_factory,
        get_pk=get_pk,
        render_kw={
            "class":"ui-select"
        }
    )
    weeks = SelectField(
        label="当前周",
        validators=[
            DataRequired("请选择当前周")
        ],
        description="当前周",
        choices=[
            ('第一周','第一周'),
            ('第二周','第二周'),
            ('第三周','第三周'),
            ('第四周','第四周'),
            ('第五周','第五周'),
            ('第六周','第六周'),
            ('第七周','第七周'),
            ('第八周','第八周'),
            ('第九周','第九周'),
            ('第十周','第十周')
        ],
        render_kw={
            "class":"ui-select"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class AddSemester(FlaskForm):
    """添加学期"""
    studyyears = StringField(
        label="学年",
        validators=[
            DataRequired("请输入学年")
        ],
        description="学年",
        render_kw={
            "class": "form-control",
            "placeholder": "例：1996-1997",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class AddSelectC(FlaskForm):
    """添加选课"""
    xh = StringField(
        label="学号",
        validators=[
            DataRequired("请输入学号")
        ],
        description="学号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学号(七位数)",
            "required": "required"
        }
    )
    kh = StringField(
        label="课号",
        validators=[
            DataRequired("请输入课号")
        ],
        description="学院名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入课号(八位数)",
            "required": "required"
        }
    )
    def query_factory():
        return [r.semester for r in  Semester.query.all()] 

    def get_pk(obj):
        return obj
    semester = QuerySelectField(
        label="当前学期",
        validators=[
            DataRequired("请选择当前学期")
        ],
        description="学期",
        query_factory=query_factory,
        get_pk=get_pk,
        render_kw={
            "class":"ui-select"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class AddCourse(FlaskForm):
    """添加课程"""
    kh = StringField(
        label="课号",
        validators=[
            DataRequired("请输入课号")
        ],
        description="学院名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入课号(八位数)",
            "required": "required"
        }
    )
    name = StringField(
        label="课程名",
        validators=[
            DataRequired("请输入课程名")
        ],
        description="工号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入课程名",
            "required": "required"
        }
    )
    credit = StringField(
        label="学分",
        validators=[
            DataRequired("请输入学分")
        ],
        description="学分",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学分",
            "required": "required"
        }
    )
    period = StringField(
        label="学时",
        validators=[
            DataRequired("请输入学时")
        ],
        description="学时",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学时",
            "required": "required"
        }
    )
    pjrate = StringField(
        label="平时分占比：",
        validators=[
            DataRequired("请输入平时分占比")
        ],
        description="平时分占比",
        render_kw={
            "class": "form-control",
            "placeholder": "0<=占比<=1",
            "required": "required"
        }
    )
    def query_factory():
        return [r.name for r in  College.query.all()] 
    def get_pk(obj):
        return obj
    yxh = QuerySelectField(
        label="学院",
        validators=[
            DataRequired("请选择学院")
        ],
        description="学院",
        query_factory=query_factory,
        get_pk=get_pk,
        render_kw={
            "class":"ui-select"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class AddClass(FlaskForm):
    """添加开课"""
    def query_factory():
        return [r.semester for r in  Semester.query.all()] 

    def get_pk(obj):
        return obj
    semester = QuerySelectField(
        label="当前学期",
        validators=[
            DataRequired("请选择当前学期")
        ],
        description="学期",
        query_factory=query_factory,
        get_pk=get_pk,
        render_kw={
            "class":"ui-select"
        }
    )
    kh = StringField(
        label="课号",
        validators=[
            DataRequired("请输入课号")
        ],
        description="学院名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入课号(八位数)",
            "required": "required"
        }
    )
    gh = StringField(
        label="工号",
        validators=[
            DataRequired("请输入工号")
        ],
        description="工号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入工号(四位数)",
            "required": "required"
        }
    )
    time = StringField(
        label="上课时间",
        validators=[
            DataRequired("请输入上课时间")
        ],
        description="上课时间",
        render_kw={
            "class": "form-control",
            "placeholder": "例：星期四 7-8",
            "required": "required"
        }
    )
    maxsize = StringField(
        label="容量",
        validators=[
            DataRequired("请输入容量")
        ],
        description="容量",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入容量",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class SetSelectCtime(FlaskForm):
    """设置选课时间"""
    def query_factory():
        return [r.semester for r in  Semester.query.all()] 

    def get_pk(obj):
        return obj
    semester = QuerySelectField(
        label="选课学期",
        validators=[
            DataRequired("请选择选课学期")
        ],
        description="选课学期",
        query_factory=query_factory,
        get_pk=get_pk,
        render_kw={
            "class":"ui-select"
        }
    )
    begin = StringField(
        label="开始时间",
        validators=[
            DataRequired("请输入开始时间")
        ],
        description="开始时间",
        render_kw={
            "type":"hidden",
            "required": "required"
        }
    )
    end = StringField(
        label="结束时间",
        validators=[
            DataRequired("请输入结束时间")
        ],
        description="结束时间",
        render_kw={
            "type":"hidden",
            "required": "required"
        }
    )
    submit = SubmitField(
        '设置',
        render_kw={
            "class": "btn btn-primary"
        }
    )

