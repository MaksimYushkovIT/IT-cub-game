from ..extensions import db
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=True)
    achievement = db.relationship('Achievement', backref='items', lazy=True)

    def __repr__(self):
        return f'<Item {self.name}>'

    def get_item_info(self):
        return {
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'image': self.image
        }