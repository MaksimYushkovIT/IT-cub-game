from ..extensions import db
from datetime import datetime

post_players = db.Table('post_players',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

post_likes = db.Table('post_likes',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Post(db.Model):
    __tablename__ = 'posts'  # имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)  # Название поста
    description = db.Column(db.Text, nullable=False)  # Описание поста
    cover_image = db.Column(db.String(500))  # Ссылка на фото обложки
    content = db.Column(db.Text, nullable=False)  # Основной текст поста
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('userM.User', backref='posts', lazy=True, foreign_keys='Post.author_id')  # Автор поста
    category = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания поста
    published_at = db.Column(db.DateTime, nullable=True)  # Дата публикации поста (может быть пустой до момента публикации)
    moderation_status = db.Column(db.String(50), default='pending')  # Статус модерации поста
    likes = db.Column(db.Integer, default=0)  # Количество лайков поста
    comments = db.relationship('Comment', back_populates='post')  # Комментарии к посту
    moderator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ID модератора поста
    moderator = db.relationship('userM.User', backref='moderated_posts', lazy=True, foreign_keys='Post.moderator_id')  # Модератор поста
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)  # ID события
    event = db.relationship('Event', backref='post_event', lazy=True, primaryjoin='Post.event_id == Event.id', overlaps="event,post_event")
    lore_id = db.Column(db.Integer, db.ForeignKey('lores.id'), nullable=True)
    players = db.relationship('User', secondary='post_players', backref=db.backref('post_players', lazy=True))
    liked_by = db.relationship('User', secondary='post_likes', backref=db.backref('liked_posts', lazy='dynamic'))

    def is_liked_by(self, user):
        return user in self.liked_by

    def __repr__(self):
        return f'<Post {self.title}>'