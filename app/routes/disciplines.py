from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.disciplineM import Discipline
from ..extensions import db

disciplines_blueprint = Blueprint('disciplines', __name__)

# ...

@disciplines_blueprint.route('/create_discipline', methods=['GET', 'POST'])
@login_required
def create_discipline():
    if not current_user.is_teacher and not current_user.is_admin:
        return 'У вас нет доступа к этой странице.'
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_discipline = Discipline(name=name, description=description)
        db.session.add(new_discipline)
        db.session.commit()
        flash('Дисциплина создана успешно!', 'success')
    return render_template('teacher/create_discipline.html')