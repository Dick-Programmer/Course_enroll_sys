from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError,EqualTo,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from SQL_EA.modles import Semester


class informationForm(FlaskForm):
    """用户信息"""
    xh = StringField(
        label="学号",
        validators=[
            DataRequired("请勿更改")
        ],
        description="学号",
        render_kw={
            "class": "form-control",
            "readonly": "readonly",
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
            "readonly": "readonly",
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
            "readonly": "readonly",
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
            "readonly": "readonly",
            "required": "required"
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
            "required": "required"
        }
    )
    mp_no = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码"),
            Regexp("1[34578]\\d{9}",message="手机号码格式不正确！")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号码",
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
            "readonly": "readonly",
            "required": "required"
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "form-control btn btn-info"
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

class SearchClass(FlaskForm):
    select =  SelectField(
        label="查询方式：",
        validators=[
            DataRequired("请选择查询方式")
        ],
        description="查询方式",
        choices=[
            ('课程号','课程号'),
            ('课程名','课程名'),
            ('学院','学院'),
            ('教师号','教师号'),
            ('教师名','教师名')
        ],
        render_kw={
            "class":"ui-select"
        }
    )
    match = StringField(
        label="查找内容：",
        validators=[
            DataRequired("请输入查找内容")
        ],
        description="查找内容",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入查找内容",
            "required": "required"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )