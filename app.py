from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from semestr_task.forms import LoginForm, BookForm, ReaderForm
from semestr_task import create_app, db, login_manager
from semestr_task.models import User, Book, Reader

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

#---------------BOOKS PAGE------------------------

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
def edit_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash('Книга не найдена.', 'danger')
        return redirect(url_for('books'))

    form = BookForm(obj=book)  # Предзаполняем форму данными книги
    if form.validate_on_submit():
        # Обновляем только те поля, которые заданы в форме
        if form.title.data:  # Проверка на заполнение поля
            book.title = form.title.data
        if form.author.data:
            book.author = form.author.data
        if form.publication_year.data:
            book.publication_year = form.publication_year.data
        if form.genre.data:
            book.genre = form.genre.data
        if form.copies.data:
            book.copies = form.copies.data
        
        db.session.commit()  # Сохраняем изменения в базе данных
        flash('Книга успешно обновлена!', 'success')
        return redirect(url_for('books'))  # Возвращаемся на страницу со списком книг

    return render_template('edit_book.html', form=form, book=book)  # Показываем страницу редактирования

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

#---------------READERS---------------

@app.route('/readers', methods=['GET', 'POST'])
@login_required
def readers():
    form = ReaderForm()
    readers = Reader.query.all()

    if form.validate_on_submit():
        new_reader = Reader(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            card_number=form.card_number.data
        )
        db.session.add(new_reader)
        db.session.commit()
        flash('Читатель успешно добавлен!', 'success')
        return redirect(url_for('readers'))

    return render_template('readers.html', readers=readers, form=form)

@app.route('/add_reader', methods=['POST'])
@login_required
def add_reader():
    form = ReaderForm()
    if form.validate_on_submit():
        print(f'Добавляем читателя: {form.first_name.data}, {form.last_name.data}, {form.card_number.data}')
        existing_reader = Reader.query.filter_by(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            card_number=form.card_number.data
        ).first()

        if existing_reader:
            flash('Такой чувак уже есть!', 'danger')
        else:
            new_reader = Reader(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                card_number=form.card_number.data
            )
            db.session.add(new_reader)
            db.session.commit()
            flash('Читатель успешно добавлен!', 'success')
        return redirect(url_for('readers', form=form))
    else:
        print(form.errors)
        flash('Ошибка при добавлении читателя. Пожалуйста, проверьте введенные данные.', 'danger')
    return redirect(url_for('readers', form=form))

@app.route('/edit_reader/<int:reader_id>', methods=['GET', 'POST'])
def edit_reader(reader_id):
    reader = Reader.query.get(reader_id)
    if not reader:
        flash('Читатель не найден.', 'danger')
        return redirect(url_for('readers'))

    form = ReaderForm(obj=reader)  # Предзаполняем форму данными Читателя
    if form.validate_on_submit():
        # Обновляем только те поля, которые заданы в форме
        if form.first_name.data:  # Проверка на заполнение поля
            reader.first_name = form.first_name.data
        if form.last_name.data:
            reader.last_name = form.last_name.data
        
        
        db.session.commit()  # Сохраняем изменения в базе данных
        flash('Читатель успешно обновлен!', 'success')
        return redirect(url_for('readers'))  # Возвращаемся на страницу со списком книг

    return render_template('edit_reader.html', form=form, reader=reader)  # Показываем страницу редактирования

@app.route('/delete_reader/<int:reader_id>', methods=['POST'])
@login_required
def delete_reader(reader_id):
    reader = Reader.query.get_or_404(reader_id)
    db.session.delete(reader)
    db.session.commit()
    flash('Читатель успешно удален!', 'success')
    return redirect(url_for('readers'))
    

#-------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
