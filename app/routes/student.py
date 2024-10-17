from flask import Blueprint, render_template, request, redirect, url_for
from ..models.userM import User
from ..extensions import db
from ..models.disciplineM import Discipline

student = Blueprint('student', __name__)

@student.route('/students')
def all_students():
    students = User.query.filter_by(is_teacher=False).all()
    return render_template('teacher/students.html', students=students)

@student.route('/students/<int:discipline_id>')
def students_by_discipline(discipline_id):
    discipline = Discipline.query.get(discipline_id)
    students = User.query.filter_by(discipline_id=discipline_id).all()
    return render_template('teacher/students.html', students=students, discipline=discipline)

@student.route('/student_info/<int:student_id>')
def student_info(student_id):
    student = User.query.get(student_id)
    if student:
        return render_template('teacher/student_info.html', student=student)
    else:
        return 'Ученик не найден'

@student.route('/disciplines')
def disciplines():
    disciplines = Discipline.query.all()
    return render_template('teacher/disciplines.html', disciplines=disciplines)

@student.route('/pashalka')
def pashalka():
    return render_template('student/pashalka.html')