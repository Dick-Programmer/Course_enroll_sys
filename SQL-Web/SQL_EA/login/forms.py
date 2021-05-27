from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from SQL_EA.modles import Student, Teacher, Manager


class LoginForm(FlaskForm):
    """登陆表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入学号/工号")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入您的工号/学号",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入您的密码",
            "required": "required"
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            "class": "form-control btn btn-info"
        }
    )

    def validate_account(self, field):
        account = field.data
        student = Student.query.filter_by(xh=account).count()
        teacher = Teacher.query.filter_by(gh=account).count()
        admin = Manager.query.filter_by(gh=account).count()
        if student == 0 and teacher == 0 and admin == 0:
            raise ValidationError("学号/工号不存在！")
