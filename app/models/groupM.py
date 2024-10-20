from ..extensions import db
from datetime import datetime

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Добавляем поле discipline_id
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    discipline = db.relationship('Discipline', backref=db.backref('groups', lazy=True))

    group_users = db.relationship('User', secondary='user_groups', backref=db.backref('group_members', lazy=True))

    def __repr__(self):
        return f'<Group {self.name}>'

    def get_group_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'discipline_id': self.discipline_id
        }