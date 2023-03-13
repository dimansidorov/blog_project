from blog.database import db
from blog.security import flask_bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), unique=False, nullable=False, default=" ", server_default=" ")
    last_name = db.Column(db.String(128), unique=False, nullable=False, default=" ", server_default=" ")
    username = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String, unique=True)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    author = db.relationship('Author', back_populates="user")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password):
        return flask_bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

    def __str__(self):
        return self.username
