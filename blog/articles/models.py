import datetime

from sqlalchemy import func

from blog.database import db

article_tag_association_table = db.Table(
    'article_tag_association',
    db.metadata,
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False)
)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), server_default=func.now())
    update_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    author = db.relationship('Author', back_populates='article')
    tag = db.relationship(
        'Tag',
        secondary=article_tag_association_table,
        back_populates='article'
    )

    def __repr__(self):
        return f'{self.title}'

    def __str__(self):
        return self.title

    @staticmethod
    def show_date(date):
        return str(date)[:-10]


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    article = db.relationship(
        'Article',
        secondary=article_tag_association_table,
        back_populates='tag'
    )

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.name
