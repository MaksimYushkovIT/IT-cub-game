from ..extensions import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String(250))
    teacher =db.Column(db.String(250))
    student = db.Column(db.String(250))
    date = db.Column(db.DateTime, default=datetime.utcnow)