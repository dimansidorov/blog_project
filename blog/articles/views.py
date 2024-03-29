import datetime
import os.path

import werkzeug
from flask import Blueprint, render_template, redirect, request, current_app, url_for
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from blog.database import db

from blog.articles.forms import CreateArticleForm, UpdateArticleForm
from blog.authors.models import Author
from blog.articles.models import Article, Tag
import blog.app

articles = Blueprint(
    'articles',
    __name__,
    url_prefix='/articles',
    static_folder='../static'
)


@articles.route('/', endpoint='list')
def article_list():
    error = None
    per_page = 2
    try:
        page = request.args.get('page', type=int)
        all_articles = Article.query.filter_by(active=True).paginate(page=page, per_page=per_page)
    except werkzeug.exceptions.NotFound:
        all_articles = Article.query.paginate(page=1, per_page=per_page)
        error = 'Такой страницы не существует'
    # except Exception as err:
    #     error = type(err)
    #     all_articles = Article.query.paginate(page=1, per_page=2)
    finally:
        return render_template(
            'articles/articles.html',
            title='Статьи',
            articles=all_articles,
            error=error
        )


@articles.route('/<id>', endpoint='detail')
# @login_required
def article_detail(id):
    _article = Article.query.filter_by(id=id).options(
        joinedload(Article.tag)
    ).one_or_none()
    if _article is None or _article.active == False:
        title = 'Статья не найдена'
        return render_template('articles/article_detail.html',
                               title=title)

    else:
        return render_template('articles/article_detail.html',
                               title=f'Статья о "{_article.title}"',
                               article=_article)


@articles.route('/add_article', methods=['GET', 'POST'], endpoint='add_article')
@login_required
def add_article():
    title = 'Добавить статью'
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        if current_user.author:
            author_id = int(str(current_user.author)[1:-1])
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.commit()
            author_id = int(str(current_user.author)[1:-1])

        file = request.files['cover']
        if file.filename == '':
            cover = '/uploads/image/default.png'
        else:
            cover = blog.app.images.save(request.files['cover'])
            cover = os.path.join('/uploads/image/', cover)
        article = Article(title=form.title.data, body=form.body.data, author_id=author_id, cover=cover)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tag.append(tag)
        db.session.add(article)

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles.detail", id=article.id, title=article.title))

    return render_template('articles/add_article.html', form=form, title=title, errors=error)


@articles.route('/delete/<id>', endpoint='delete_article')
@login_required
def delete_article(id):
    article = Article.query.filter_by(id=id).one_or_none()
    if current_user.id == article.author.user.id:
        try:
            article.active = False
            db.session.commit()
        except Exception as err:
            print(err)
    return redirect(url_for('articles.list'))


@articles.route('/update_article/<int:id>', methods=['GET', 'POST'], endpoint='update_article')
@login_required
def update_article(id):
    article = Article.query.filter_by(id=id).options(
        joinedload(Article.tag)
    ).one_or_none()
    title = f'Редактирование статьи {article.title}'
    error = None
    form = UpdateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if form.title.data:
            article.title = form.title.data
        if form.body.data:
            article.body = form.body.data
        file = request.files['cover']
        if file.filename != '':
            cover = blog.app.images.save(request.files['cover'])
            cover = os.path.join('static/uploads/', cover)
            article.cover = cover
            print(cover)
        article.update_at = datetime.datetime.utcnow()
        try:
            db.session.commit()
        except Exception as err:
            return render_template('articles/update_article.html',
                                   article=article,
                                   form=form,
                                   title=title,
                                   errors=err)
        else:
            return redirect(url_for('articles.detail', id=id))

    return render_template('articles/update_article.html',
                           article=article,
                           form=form,
                           title=title,
                           errors=error)
