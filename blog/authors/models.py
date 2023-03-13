from blog.database import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    user = db.relationship('User', back_populates="author")
    article = db.relationship('Article', back_populates='author')

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.user.username
