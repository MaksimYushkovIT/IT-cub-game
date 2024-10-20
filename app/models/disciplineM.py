from ..extensions import db
from datetime import datetime

user_disciplines = db.Table('user_disciplines',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('discipline_id', db.Integer, db.ForeignKey('disciplines.id'))
)

faction_disciplines = db.Table('faction_disciplines',
    db.Column('faction_id', db.Integer, db.ForeignKey('factions.id')),
    db.Column('discipline_id', db.Integer, db.ForeignKey('disciplines.id'))
)

teacher_disciplines = db.Table('teacher_disciplines',
    db.Column('teacher_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('discipline_id', db.Integer, db.ForeignKey('disciplines.id')),
    extend_existing=True
)

class Discipline(db.Model):
    __tablename__ = 'disciplines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    faction_id = db.Column(db.Integer, db.ForeignKey('factions.id', name='fk_discipline_faction', ondelete='SET NULL'), nullable=True)
    
    teachers = db.relationship('User', secondary='teacher_disciplines', back_populates='disciplines')
    users = db.relationship('User', secondary='user_disciplines', back_populates='disciplines')
    faction = db.relationship('Faction', secondary='faction_disciplines', backref='disciplines', lazy=True)

    def __repr__(self):
        return f'<Discipline {self.name}>'

    def get_discipline_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def get_teachers(self):
        return self.teachers

    def get_users(self):
        return self.users

    def get_factions(self):
        return self.factions