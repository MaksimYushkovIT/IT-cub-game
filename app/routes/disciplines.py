from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.disciplineM import Discipline
from ..models.groupM import Group
from ..extensions import db
from ..decorators import admin_required

disciplines_blueprint = Blueprint('disciplines', __name__)

# ...

from ..models.factionM import Faction

from ..models.factionM import Faction

@disciplines_blueprint.route('/create_discipline', methods=['GET', 'POST'])
@login_required
def create_discipline():
    if not current_user.is_teacher and not current_user.is_admin:
        return 'У вас нет доступа к этой странице.'
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        faction_id = request.form.get('faction_id')
        new_discipline = Discipline(name=name, description=description, faction_id=faction_id)
        db.session.add(new_discipline)
        db.session.commit()
        flash('Дисциплина создана успешно!', 'success')
        return redirect(url_for('disciplines.list_disciplines'))
    factions = Faction.query.all()
    return render_template('teacher/create_discipline.html', factions=factions)

@disciplines_blueprint.route('/create_group/<int:discipline_id>', methods=['GET', 'POST'])
@login_required
def create_group(discipline_id):
    if not current_user.is_teacher and not current_user.is_admin:
        return 'У вас нет доступа к этой странице.'
    
    discipline = Discipline.query.get_or_404(discipline_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Название группы обязательно', 'error')
            return render_template('teacher/create_group.html', discipline=discipline)
        
        new_group = Group(
            name=name,
            description=description,
            discipline_id=discipline.id
        )
        
        try:
            db.session.add(new_group)
            db.session.commit()
            flash('Группа успешно создана!', 'success')
            return redirect(url_for('disciplines.list_disciplines'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании группы: {str(e)}', 'error')
    
    return render_template('teacher/create_group.html', discipline=discipline)

@disciplines_blueprint.route('/disciplines')
@login_required
def list_disciplines():
    disciplines = Discipline.query.all()
    return render_template('disciplines/list.html', disciplines=disciplines)

@disciplines_blueprint.route('/edit_discipline/<int:discipline_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_discipline(discipline_id):
    discipline = Discipline.query.get_or_404(discipline_id)
    
    if request.method == 'POST':
        discipline.name = request.form['name']
        discipline.description = request.form['description']
        discipline.faction_id = request.form['faction_id']
        
        try:
            db.session.commit()
            flash('Дисциплина успешно обновлена!', 'success')
            return redirect(url_for('disciplines.list_disciplines'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении дисциплины: {str(e)}', 'error')
    
    factions = Faction.query.all()
    return render_template('disciplines/edit_discipline.html', discipline=discipline, factions=factions)

@disciplines_blueprint.route('/delete_discipline/<int:discipline_id>', methods=['POST'])
@login_required
@admin_required
def delete_discipline(discipline_id):
    discipline = Discipline.query.get_or_404(discipline_id)
    
    try:
        db.session.delete(discipline)
        db.session.commit()
        flash('Дисциплина успешно удалена!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении дисциплины: {str(e)}', 'error')
    
    return redirect(url_for('disciplines.list_disciplines'))