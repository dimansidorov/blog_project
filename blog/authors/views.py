from flask import Blueprint, render_template
from flask_login import login_required, current_user

from blog.authors.models import Author

authors = Blueprint(
    'authors',
    __name__,
    url_prefix='/authors',
    template_folder='../templates',
    static_folder='../static'
)


@authors.route('/', endpoint='list')
@login_required
def authors_list():
    all_authors = Author.query.all()
    return render_template('authors/authors.html',
                           title='Авторы',
                           authors=all_authors)


@authors.route('/<id>', endpoint='detail')
@login_required
def author_detail(id):
    author = Author.query.filter_by(id=id).one_or_none()
    # print(current_user.is_staff)
    if author is None:
        title = 'Автор не найден'
        return render_template('authors/author_detail.html',
                               title=title)

    else:
        return render_template('authors/author_detail.html',
                               title=f'Автор {author.user.username}',
                               author=author)
