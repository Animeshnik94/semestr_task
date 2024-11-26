from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import User
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kfd843H(*&Y$&H)'

login_manager = LoginManager()
login_manager.init_app(app)

# Предопределенные данные для входа
USERNAME = "admin"
PASSWORD = "12345"

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
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/books')
@login_required
def books():
    return render_template('books.html')

if __name__ == '__main__':
    app.run(debug=True)