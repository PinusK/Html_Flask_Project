from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class DeleteStudentForm(FlaskForm):
    login = StringField('логин ученика', validators=[DataRequired()])
    password = PasswordField('Пароль учителя', validators=[DataRequired()])
    submit = SubmitField('удалить')

