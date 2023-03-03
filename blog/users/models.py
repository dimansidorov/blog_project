from blog.database import db
from blog.security import flask_bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String, unique=True)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    articles = db.relationship('Article', backref='user', lazy=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.check_password_hash(value)

    def validate_password(self, password):
        return flask_bcrypt.check_password_hash(self._password, password)


    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"
