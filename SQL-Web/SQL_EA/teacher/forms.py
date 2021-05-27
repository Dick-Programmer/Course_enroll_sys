from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from SQL_EA.modles import Teacher,Semester


class informationForm(FlaskForm):
    """用户信息"""
    gh = StringField(
        label="工号",
        validators=[
            DataRequired("请勿更改")
        ],
        description="工号",
        render_kw={
            "class": "form-control",
            "readonly":"readonly",
            "required": "required"
        }
    )
    name = StringField(
        label="姓名",
        validators=[
            DataRequired("请勿更改")
        ],
        description="姓名",
        render_kw={
            "class": "form-control",
            "readonly":"readonly",
            "required": "required"
        }
    )
    sex = StringField(
        label="性别",
        validators=[
            DataRequired("请勿更改")
        ],
        description="性别",
        render_kw={
            "class": "form-control",
            "readonly":"readonly",
            "required": "required"
        }
    )
    birthday = StringField(
        label="生日",
        validators=[
            DataRequired("请勿更改")
        ],
        description="生日",
        render_kw={
            "class": "form-control",
            "readonly":"readonly",
            "required": "required"
        }
    )
    education = StringField(
        label="职位",
        validators=[
            DataRequired("请勿更改")
        ],
        description="职位",
        render_kw={
            "class": "form-control",
            "readonly":"readonly",
            "required": "required"
        }
    )
    salary = StringField(
        label="基本工资",
        validators=[
            DataRequired("请勿更改")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "readonly":"readonly",
            "required": "required"
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
            "readonly":"readonly",
            "required": "required"
        }
    )


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


class CourseForm(FlaskForm):
    """查看课程——选择学期"""
    def query_factory():
        r = [r.semester for r in  Semester.query.all()]
        r.append("所有")
        return r

    def get_pk(obj):
        return obj
    semester = QuerySelectField(
        label="学期：",
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
        '提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )

class ClassApplyForm(FlaskForm):
    """申请开课"""
    name = StringField(
        label="课程名：",
        validators=[
            DataRequired("请输入课程名")
        ],
        description="课程名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入课程名",
            "required": "required"
        }
    )
    credit = StringField(
        label="学分：",
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
        label="学时：",
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
    psrate = StringField(
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
    describe = TextAreaField(
        label= "课程描述：",
        validators=[
            DataRequired("请输入课程描述！"),
        ],
        description="课程描述",
        render_kw={
            "rows": "10",
            "cols": "80",
            "placeholder": "请输入课程描述...",
            "style": "width: 100%; height: 150px"
        }
    )
    submit = SubmitField(
        '提交申请',
        render_kw={
            "class": "btn btn-primary"
        }
    )
