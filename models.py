from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Модель пользователя
class User(UserMixin):
    def __init__(self, username):
        self.username = username
    def get_id(self):
        return self.username  # Возвращаем username как идентификатор