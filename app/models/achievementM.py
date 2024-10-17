from ..extensions import db
from datetime import datetime

achievement_factions = db.Table('achievement_factions',
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id')),
    db.Column('faction_id', db.Integer, db.ForeignKey('factions.id')),
    extend_existing=True
)

class Achievement(db.Model):
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    avatar = db.Column(db.String(200), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)

    event = db.relationship('Event', backref='event_achievements', lazy=True)
    users = db.relationship('User', secondary='user_achievements', backref='achievement_users', lazy=True)

    def __repr__(self):
        return f'<Achievement {self.name}>'

    def get_achievement_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'type': self.type,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'avatar': self.avatar,
            'event_id': self.event_id
        }

    def get_event(self):
        return self.event

    def get_users(self):
        return self.users