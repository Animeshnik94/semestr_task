from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from semestr_task import db

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    copies = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Book {self.title}, Author {self.author}>'
    

class Reader(db.Model):
    __tablename__ = 'readers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Reader {self.first_name} {self.last_name}>'

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))
    reader = db.relationship('Reader', backref=db.backref('loans', lazy=True))

    def __repr__(self):
        return f'<Loan {self.book.title} to {self.reader.first_name}>'



# # Пример регистрации читателя
def register_reader(first_name, last_name, card_number):
    new_reader = Reader(first_name=first_name, last_name=last_name, card_number=card_number)
    db.session.add(new_reader)
    db.session.commit()

# Функция поиска книги по названию
def find_book_by_title(title):
    return Book.query.filter_by(title=title).all()