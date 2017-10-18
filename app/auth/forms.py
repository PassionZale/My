from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import FlaskyConfigs


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(message='请输入邮箱'), Email(message='邮箱不合法')])
    password = PasswordField('密码', validators=[Required(message='请输入密码')]) 
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField(
        '邮箱',
        validators=[
            Required(message='邮箱不能为空'),
            Length(1, 64, '邮箱长度为1-64位'),
            Email(message='邮箱格式不合法')
        ])
    username = StringField(
        '用户名',
        validators=[
            Required(message='用户名不能为空'),
            Length(1, 16, '用户名长度为1-16位'),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母,数字,点号,下划线')
        ])
    password = PasswordField(
        '密码',
        validators=[
            Required(message='密码不能为空'),
            Length(1, 16),
            EqualTo('confirm_pwd', message='两次输入的密码必须相同')
        ])
    confirm_pwd = PasswordField(
        '确认密码', validators=[Required(message='请再次输入密码')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if FlaskyConfigs.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if FlaskyConfigs.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')