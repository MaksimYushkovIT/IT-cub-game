from ..extensions import db
from datetime import datetime

project_students = db.Table('project_students',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

project_teachers = db.Table('project_teachers',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название файла
    path = db.Column(db.String(200), nullable=False)  # Путь к файлу
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания файла
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # ID проекта, к которому относится файл
      # Связь с проектом

    def __repr__(self):
        return f'<File {self.name}>'

    def get_file_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'created_at': self.created_at,
            'project_id': self.project_id
        }

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='в работе')
    grade = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    passport_link = db.Column(db.String(200), nullable=True)
    materials_link = db.Column(db.String(200), nullable=True)
    presentation_link = db.Column(db.String(200), nullable=True)
    
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    event = db.relationship('Event', back_populates='event_projects')
    project_students = db.relationship('User', secondary=project_students, back_populates='student_projects')
    project_teachers = db.relationship('User', secondary=project_teachers, back_populates='teacher_projects')

    def __repr__(self):
        return f'<Project {self.name}>'

    def get_project_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'event_id': self.event_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status,
            'grade': self.grade,
            'feedback': self.feedback,
            'category': self.category
        }

    def get_event(self):
        return self.event

    def get_students(self):
        return self.students

    def get_files(self):
        return self.files