from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

# Форма для входа
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Форма для добавления/редактирования книги
class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    publication_year = IntegerField('Год издания', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    copies = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

