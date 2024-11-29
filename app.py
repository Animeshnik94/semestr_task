from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from semestr_task.forms import LoginForm, BookForm
from semestr_task import create_app, db, login_manager
from semestr_task.models import User, Book

app = create_app()

# Предопределенные данные для входа
USERNAME = "admin"
PASSWORD = "12345"

@login_manager.user_loader
def load_user(username):
    if username == USERNAME:
        return User(username)
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == USERNAME and form.password.data == PASSWORD:
            user = User(form.username.data)
            login_user(user)
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

@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    form = BookForm()  # Создание объекта формы
    books = Book.query.all()
    
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            publication_year=form.publication_year.data,
            genre=form.genre.data,
            copies=form.copies.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('books'))

    return render_template('books.html', books=books, form=form)  # Передаем форму в шаблон


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)  # Предполагается, что вы добавили BookForm
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.publication_year = form.publication_year.data
        book.genre = form.genre.data
        book.copies = form.copies.data
        db.session.commit()
        flash('Книга успешно обновлена!', 'success')
        return redirect(url_for('books'))
    return render_template('edit_book.html', form=form, book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Книга успешно удалена!', 'danger')
    return redirect(url_for('books'))

@app.route('/add_book', methods=['POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        print(f'Добавляем книгу: {form.title.data}, {form.author.data}, {form.publication_year.data}, {form.genre.data}, {form.copies.data}')  # Логируем данные
        existing_book = Book.query.filter_by(
            title=form.title.data,
            author=form.author.data,
            publication_year=form.publication_year.data
        ).first()

        if existing_book:
            existing_book.copies += form.copies.data
            db.session.commit()
            flash('Количество копий книги увеличено!', 'success')
        else:
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                publication_year=form.publication_year.data,
                genre=form.genre.data,
                copies=form.copies.data
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('books', form=form))
    else:
        print(form.errors)
        flash('Ошибка при добавлении книги. Пожалуйста, проверьте введенные данные.', 'danger')

    # Если форма не корректна, отправьте обратно на страницу books
    # или отобразите сообщения об ошибках.
    return redirect(url_for('books'))  # Либо вы можете отобразить ошибки

if __name__ == '__main__':
    app.run(debug=True)
