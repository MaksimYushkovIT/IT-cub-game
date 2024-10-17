from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ..extensions import db

class Lore(db.Model):
    __tablename__ = 'lores'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='draft')
    views = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)
    image = db.Column(db.String(200), nullable=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship('Post', backref='lore', lazy=True, primaryjoin='Lore.id == Post.lore_id')
    lore_tags = db.Table('lore_tags',
        db.Column('lore_id', db.Integer, db.ForeignKey('lores.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
    )

    tags = db.relationship('Tag', secondary='lore_tags', backref='lores', lazy=True)

    def __repr__(self):
        return f'<Lore {self.title}>'

    def get_tags(self):
        return self.tags

    def get_comments(self):
        return self.comments

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'