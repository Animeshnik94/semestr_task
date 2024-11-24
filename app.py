from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kfd843H(*&Y$&H)'

login_manager = LoginManager()
login_manager.init_app(app)

# Предопределенные данные для входа
USERNAME = "admin"
PASSWORD = "12345"

# Форма для входа
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

@login_manager.user_loader
def load_user(username):
    # В этом случае, возвращаем пользователя, если имя пользователя верно
    if username == USERNAME:
        return User(username)
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == USERNAME and form.password.data == PASSWORD:
            user = User(form.username.data)
            login_user(user)  # Логин пользователя
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/index')
@login_required
def index():
    return 'Добро пожаловать, админ! <a href="/logout">Выйти</a>'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)         