from ..extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .eventM import event_players_competed
from .disciplineM import user_disciplines
from .factionM import user_factions  # Make sure this import is correct

class UnreadNotification(db.Model):
    __tablename__ = 'unread_notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

# Информация о достижениях пользователя
user_achievements = db.Table('user_achievements',
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    extend_existing=True
)

# Информация о фракции пользователя
user_factions = db.Table('user_factions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('faction_id', db.Integer, db.ForeignKey('factions.id')),
    extend_existing=True
)

# Информация о предметах в инвентаре пользователя
user_items = db.Table('user_items',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
    
)

# Список друзей пользователя
friendships = db.Table('friendships',
    db .Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id')),
    extend_existing=True
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Основная информация о пользователе
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    username = db.Column(db.String(50), unique=True, nullable=False)  # Имя пользователя
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email пользователя
    password = db.Column(db.String(200), nullable=False)  # Пароль пользователя
    unread_notifications = db.relationship('UnreadNotification', backref='user', lazy='dynamic')
    # Информация о личности пользователя
    last_name = db.Column(db.String(50), nullable=False)  # Фамилия пользователя
    first_name = db.Column(db.String(50), nullable=False)  # Имя пользователя
    patronymic = db.Column(db.String(50), nullable=True)  # Отчество пользователя
    birthday = db.Column(db.DateTime, nullable=True)  # Дата рождения пользователя

    # Информация о статусе и уровне пользователя
    status = db.Column(db.String(50), default='активный')  # Статус пользователя
    level = db.Column(db.Integer, default=1)  # Уровень пользователя
    cube_coins = db.Column(db.Integer, default=0)  # Куб-коины пользователя
    experience = db.Column(db.Integer, default=0)  # Опыт пользователя
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата регистрации пользователя
    last_active_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата последней активности пользователя
    items = db.relationship('Item', secondary=user_items, backref=db.backref('users', lazy='dynamic'))
    # Информация о роли пользователя
    role = db.Column(db.String(50), default='участник')  # Роль пользователя

    # Информация о профиле пользователя
    avatar = db.Column(db.String(200), nullable=True)  # Аватар пользователя
    bio = db.Column(db.Text, nullable=True)  # Биография пользователя
    contact_info = db.Column(db.String(200), nullable=True)  # Контактная информация пользователя

    # Информация о фракции и должности пользователя
    position = db.Column(db.String(50), default='новичок')  # Должность пользователя
    is_admin = db.Column(db.Boolean, default=False)
    # Информация о социальных сетях пользователя
    telegram_link = db.Column(db.String(200), nullable=True)  # Ссылка на Telegram пользователя
    discord_link = db.Column(db.String(200), nullable=True)  # Ссылка на Discord пользователя
    avatar = db.Column(db.String(200), nullable=True)  # Аватар пользователя
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=True)
    discipline = db.relationship('Discipline', backref='user_disciplines', lazy=True)
    disciplines = db.relationship('Discipline', secondary='user_disciplines', back_populates='users')
    # Информация о группе пользователя
    groups = db.relationship('Group', secondary='user_groups', backref=db.backref('group_members', lazy=True))

    # Информация о предметах и педагогическом стаже учителя (для учителей)
    is_teacher = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Связь с учителем
    teacher = db.relationship('User', remote_side=[id], backref='students')  # Связь с учителем
    discipline_teachers = db.relationship('Discipline', secondary='teacher_disciplines', back_populates='teachers')
    Teacher_subjects = db.relationship('Discipline', secondary='teacher_disciplines', back_populates='teachers', overlaps='discipline_teachers,teachers')
    lore = db.Column(db.Text, nullable=True)  # Лор учителя
    pedstage = db.Column(db.String(100), nullable=True)  # Педагогический стаж учителя
    achievements = db.relationship('Achievement', secondary='user_achievements', back_populates='users')
    comments = db.relationship('Comment', back_populates='author', lazy=True)
    factions = db.relationship('Faction', secondary=user_factions, back_populates='users')
    user_completed_events = db.relationship('Event', secondary='event_players_competed',
                    primaryjoin='User.id == event_players_competed.c.user_id',
                    secondaryjoin='Event.id == event_players_competed.c.event_id',
                    backref='completed_users', lazy=True)
    events = db.relationship('Event', secondary='event_players_competed', backref='user_completed_events', lazy=True, overlaps="event_users,events,players,users")
    student_projects = db.relationship('Project', secondary='project_students', back_populates='project_students')
    teacher_projects = db.relationship('Project', secondary='project_teachers', back_populates='project_teachers')

    # Методы для работы с паролями
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Методы для работы с Flask-Login
    def get_id(self):
        return str(self.id)  # Возвращаем идентификатор пользователя как строку
    
    def get_item_count(self, item_id):
        return len([item for item in self.items if item.id == item_id])

    def add_item(self, item):
        self.items.append(item)

    @property
    def is_active(self):
        """Возвращает, активен ли пользователь.""" 
        return True  # или добавьте логику, если хотите сделать это условным

    def __repr__(self):
        return f'<User {self.username}>'
    
    def add_unread_notification(self, item):
        notification = UnreadNotification(user_id=self.id, item_id=item.id)
        db.session.add(notification)
        db.session.commit()

    def get_unread_notifications(self):
        return self.unread_notifications.all()

    def clear_unread_notifications(self):
        self.unread_notifications.delete()
        db.session.commit()