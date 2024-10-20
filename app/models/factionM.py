from ..extensions import db
from datetime import datetime

user_factions = db.Table('user_factions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('faction_id', db.Integer, db.ForeignKey('factions.id')),
    extend_existing=True
)

achievement_factions = db.Table('achievement_factions',
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id')),
    db.Column('faction_id', db.Integer, db.ForeignKey('factions.id')),
    extend_existing=True
)
class Faction(db.Model):
    __tablename__ = 'factions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_faction_leader', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    experience = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    leader = db.relationship('User', foreign_keys=[leader_id], backref='faction_leader', lazy=True)
    users = db.relationship('User', secondary=user_factions, back_populates='factions')
    ranks = db.relationship('Rank', backref='faction', lazy=True)
    achievements = db.relationship('Achievement', secondary='achievement_factions', backref=db.backref('faction_achievements', lazy=True))
    users = db.relationship('User', secondary=user_factions, back_populates='factions')
    
    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= 1000:
            self.level_up()
        
        db.session.commit()

    def level_up(self):
        self.level += 1
        self.experience -= 1000

    def __repr__(self):
        return f'<Faction {self.name}>'

    def get_faction_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'leader_id': self.leader_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'experience': self.experience,
            'level': self.level
        }

class Rank(db.Model):
    __tablename__ = 'ranks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    faction_id = db.Column(db.Integer, db.ForeignKey('factions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Rank {self.name}>'