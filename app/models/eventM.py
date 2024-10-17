from ..extensions import db
from datetime import datetime, timedelta
from app.models.postM import Post
from app.models.projectsM import Project, project_students

event_players_competed = db.Table('event_players_competed',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)
user_events = db.Table('user_events',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    type = db.Column(db.String(50), nullable=False, default='мероприятие')

    users = db.relationship('User', secondary='user_events', backref=db.backref('event_users', lazy=True))
    discipline = db.relationship('Discipline', backref='events', lazy=True)
    group = db.relationship('Group', backref='events', lazy=True)
    experience = db.Column(db.Integer, default=0,nullable=False)  # Очки опыта за выполнение
    money_reward = db.Column(db.Integer, default=0, nullable=False)  # Деньги за выполнение
    participation_points = db.Column(db.Integer, default=0, nullable=False)  # Очки за участие
    victory_points = db.Column(db.Integer, default=0, nullable=False)  # Очки за победу
    importance = db.Column(db.String(50), nullable=False)  # Важность мероприятия (куб, район, город, область, регион, страна, весь мир)
    achievements = db.relationship('Achievement', backref='event_achievements', lazy=True)
    is_completed = db.Column(db.Boolean, default=False)  # Завершаемое ли событие или нет
    completion_date = db.Column(db.DateTime, nullable=True)  # Дата завершения
    post = db.relationship('Post', backref='user_events', lazy=True, primaryjoin='Event.id == Post.event_id', overlaps="event,post_event")
    players = db.relationship('User', secondary='user_events', backref=db.backref('event_players', lazy=True, overlaps="event_users,events,users"))
    completed_players = db.relationship('User', secondary='event_players_competed',
                    primaryjoin='Event.id == event_players_competed.c.event_id',
                    secondaryjoin='User.id == event_players_competed.c.user_id',
                    backref='event_players_completed', lazy=True)
    event_players = db.relationship('User', secondary='event_players_competed', backref='completed_events', lazy=True, overlaps="event_users,events,players,users")
    event_projects = db.relationship('Project', back_populates='event')
    passport_deadline = db.Column(db.DateTime, nullable=True)
    materials_deadline = db.Column(db.DateTime, nullable=True)
    presentation_deadline = db.Column(db.DateTime, nullable=True)

    
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        # Устанавливаем дедлайны автоматически при создании события
        if self.start_date and self.end_date:
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d') if isinstance(self.start_date, str) else self.start_date
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d') if isinstance(self.end_date, str) else self.end_date
            
            if start_date >= end_date - timedelta(days=15):
                self.passport_deadline = start_date + timedelta(days=7)
                self.materials_deadline = start_date + timedelta(days=14)
                self.presentation_deadline = end_date - timedelta(days=1)
            elif start_date > end_date - timedelta(days=7):
                self.passport_deadline = start_date + timedelta(days=1)
                self.materials_deadline = start_date + timedelta(days=5)
                self.presentation_deadline = end_date - timedelta(days=1)
            else:
                self.passport_deadline = start_date
                self.materials_deadline = start_date
                self.presentation_deadline = end_date - timedelta(days=1)


    def __repr__(self):
        return f'<Event {self.name}>'

    def get_event_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'creator_id': self.creator_id,
            'discipline_id': self.discipline_id,
            'group_id': self.group_id,
            'type': self.type,
            'experience': self.experience,
            'money_reward': self.money_reward,
            'participation_points': self.participation_points,
            'victory_points': self.victory_points,
            'importance': self.importance,
            'is_completed': self.is_completed,
            'completion_date': self.completion_date
        }
    
    def get_user_project(self, user_id):
        return Project.query.join(project_students).filter(project_students.c.user_id == user_id, project_students.c.project_id == self.id).first()
    