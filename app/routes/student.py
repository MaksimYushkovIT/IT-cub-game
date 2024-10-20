from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..models.userM import User
from ..models.groupM import Group
from ..extensions import db
from flask_login import current_user, login_required
from ..models.disciplineM import Discipline
from ..decorators import teacher_required
from ..models.itemM import Item
from ..models.achievementM import Achievement

student = Blueprint('student', __name__)

@student.route('/disciplines')
@login_required
def disciplines():
    disciplines = Discipline.query.all()
    return render_template('teacher/disciplines.html', disciplines=disciplines)


@student.route('/student_info/<int:student_id>')
def student_info(student_id):
    student = User.query.get(student_id)
    if student:
        return render_template('teacher/student_info.html', student=student)
    else:
        return 'Ученик не найден'

@student.route('/pashalka')
def pashalka():
    return render_template('student/pashalka.html')

from flask import Blueprint, render_template, request
from flask_login import login_required
from ..models.userM import User
from ..models.disciplineM import Discipline
from ..models.groupM import Group

@student.route('/students/<int:discipline_id>')
@login_required
def students_by_discipline(discipline_id):
    groups = Group.query.all()
    teachers = User.query.filter_by(is_teacher=True).all()
    filters = {}
    if request.args.get('group'):
        filters['group_id'] = request.args.getlist('group')
    if request.args.get('teacher'):
        filters['teacher_id'] = request.args.getlist('teacher')
    if request.args.get('min_level'):
        filters['level__gte'] = int(request.args.get('min_level'))
    if request.args.get('max_level'):
        filters['level__lte'] = int(request.args.get('max_level'))
    if request.args.get('position'):
        filters['position'] = request.args.getlist('position')

    if discipline_id == 0:  # 0 будет означать "Все дисциплины"
        students = User.query.filter_by(is_teacher=False)
        discipline = {"name": "Все дисциплины"}
    else:
        discipline = Discipline.query.get_or_404(discipline_id)
        students = User.query.filter_by(is_teacher=False, discipline_id=discipline_id)

    if 'group_id' in filters:
        students = students.filter(User.groups.any(Group.id.in_(filters['group_id'])))
    if 'teacher_id' in filters:
        students = students.filter(User.teacher_id.in_(filters['teacher_id']))
    if 'level__gte' in filters:
        students = students.filter(User.level >= filters['level__gte'])
    if 'level__lte' in filters:
        students = students.filter(User.level <= filters['level__lte'])
    if 'position' in filters:
        students = students.filter(User.position.in_(filters['position']))

    sort = request.args.get('sort', 'last_name')
    if sort == 'last_name':
        students = students.order_by(User.last_name)
    elif sort == 'first_name':
        students = students.order_by(User.first_name)
    elif sort == 'level':
        students = students.order_by(User.level)

    students = students.all()

    return render_template('teacher/students.html', discipline=discipline, groups=groups, teachers=teachers, students=students)

@student.route('/reward_students', methods=['POST'])
@login_required
@teacher_required
def reward_students():
    data = request.json
    if not data or 'students' not in data:
        return jsonify({'status': 'error', 'message': 'Некорректные данные запроса'}), 400

    try:
        students = User.query.filter(User.id.in_(data['students'])).all()
        if not students:
            return jsonify({'status': 'error', 'message': 'Студенты не найдены'}), 404

        for student in students:
            if 'experience' in data:
                experience = int(data['experience'])
                student.add_experience(experience)
            if 'gold' in data:
                student.cube_coins += int(data['gold'])
            if 'item' in data and data['item']:
                item = Item.query.get(data['item'])
                if item:
                    student.items.append(item)
            if 'achievement' in data and data['achievement']:
                achievement = Achievement.query.get(data['achievement'])
                if achievement:
                    student.achievements.append(achievement)

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Ученики успешно награждены',
            'rewarded_students': len(students)
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Произошла ошибка при награждении учеников: {str(e)}'
        }), 500