import os

import click

from blog.database import db


# @click.command("init-db")
# def init_db():
#     """
#     Run in your terminal:
#     flask init-db
#     """
#     db.create_all()
#     print("done!")


@click.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from blog.users.models import User
    username = input('Введите имя пользователя: ')
    email = input('Введите адрес электронной почты: ')
    admin = User(username=username, is_staff=True, email=email)
    admin.password = os.environ.get('ADMIN_PASSWORD') or 'adminpass'

    db.session.add(admin)
    db.session.commit()

    print(f'Суперпользователь {admin} создан')


@click.command("create-articles")
def create_articles():
    """
    Run in your terminal:
    flask create-articles
    > done! created articles >
    """
    from blog.articles.models import Article
    article_one = Article(title="Тайна Коко",
                          body='12-летний Мигель живёт в мексиканской деревушке в семье сапожников и тайно мечтает стать музыкантом. Когда-то его прапрадед оставил жену, прапрабабку Мигеля, ради мечты, которая теперь не даёт спокойно жить и его праправнуку. С тех пор музыкальная тема в семье стала табу.',
                          author_id=1)
    article_two = Article(title="Криминальное чтиво",
                          body='Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса.',
                          author_id=1)
    db.session.add(article_one)
    db.session.add(article_two)
    db.session.commit()
    print(f"done! created users: {article_one}, {article_two}")


@click.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    from blog.articles.models import Tag
    for item in ['мультфильм',
                 'семейное',
                 'боевик',
                 'фантастика',
                 'фэнтези',
                 'ужасы',
                 'триллер',
                 'сериал']:
        tag = Tag(name=item)
        db.session.add(tag)
    db.session.commit()
    print(f"done! tags added!")
