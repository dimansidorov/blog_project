from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from blog.users.models import User
from blog.database import db
from .forms import RegisterUserForm, LoginForm

auth_app = Blueprint(
    'auth_app',
    __name__
)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth_app.login'))


@auth_app.route('/register/', methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('articles.list'))

    title = 'Регистрация'
    error = None
    form = RegisterUserForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("Такой пользователь уже существует!")
            return render_template("auth/register.html", form=form, title=title)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("Пользователь с таким email уже существует!")
            return render_template("auth/register.html", form=form, title=title)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info(f"Created user {user}")
            login_user(user)
            return redirect(url_for("articles.list"))
    return render_template("auth/register.html", form=form, error=error, title=title)


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('articles.list'))

    errors = None
    title = 'Авторизация'
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, errors="username doesn't exist", title=title)

        if not user.validate_password(form.password.data):
            return render_template("auth/login.html", form=form, errors="invalid username or password", title=title)

        login_user(user)
        return redirect(url_for("articles.list"))
    return render_template("auth/login.html", form=form, title=title)


@auth_app.route('/login-as/', methods=['GET', 'POST'])
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):
        raise NotFound


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("articles.list"))


@auth_app.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"


__all__ = (
    'login_manager',
    'auth_app',
)
