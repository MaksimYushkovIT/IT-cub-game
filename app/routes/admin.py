from flask import Blueprint, render_template, redirect, url_for, flash
from ..models.userM import User
from ..models.disciplineM import Discipline
from flask_login import login_required
from ..decorators import admin_required
from ..extensions import db

admin = Blueprint('admin', __name__)

@admin.route('/teachers')
@login_required
@admin_required
def teachers_list():
    teachers = User.query.filter_by(is_teacher=True).all()
    disciplines = Discipline.query.all()
    
    for discipline in disciplines:
        discipline.student_count = User.query.filter_by(discipline_id=discipline.id, is_teacher=False).count()
    
    return render_template('admin/teachers_list.html', teachers=teachers, disciplines=disciplines)

@admin.route('/delete_teacher/<int:teacher_id>', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Преподаватель успешно удален', 'success')
    return redirect(url_for('admin.teachers_list'))

