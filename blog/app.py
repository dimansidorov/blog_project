from flask import Flask, render_template

from blog.admin import admin
from blog.authors.views import authors
from blog.articles.views import articles
from blog.auth.views import auth_app, login_manager
from blog.users.views import users
from blog.database import db
from blog.security import flask_bcrypt
from blog import commands
import os

from flask_migrate import Migrate


def create_app() -> Flask:
    app = Flask(__name__)
    cfg_name = os.environ.get("CONFIG_NAME") or "DevConfig"
    app.config.from_object(f'blog.configs.{cfg_name}')

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


def register_extensions(app: Flask):
    pass
    flask_bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    migrate = Migrate(app, db, compare_type=True)


def register_blueprints(app: Flask):
    app.register_blueprint(blueprint=articles, name='articles')
    app.register_blueprint(blueprint=users, name='users')
    app.register_blueprint(blueprint=authors, name='authors')
    app.register_blueprint(blueprint=auth_app, name='auth_app')


def register_commands(app: Flask):
    # app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_admin)
    app.cli.add_command(commands.create_articles)
    app.cli.add_command(commands.create_tags)
