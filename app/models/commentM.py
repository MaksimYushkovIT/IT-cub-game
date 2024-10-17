from ..extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship('User', back_populates='comments', lazy=True)
    post = db.relationship('Post', back_populates='comments', lazy=True)

    def __repr__(self):
        return f'<Comment {self.text}>'

    def get_comment_info(self):
        return {
            'id': self.id,
            'text': self.text,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def get_author(self):
        return self.author

    def get_post(self):
        return self.post