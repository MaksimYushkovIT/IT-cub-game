from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..decorators import teacher_required
from ..models.achievementM import Achievement
from ..extensions import db
from ..models.eventM import Event

achievements = Blueprint('achievements', __name__)

@achievements.route('/create_achievement', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_achievement():
    events = Event.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        achievement_type = request.form.get('type')
        
        new_achievement = Achievement(name=name, description=description, category=category, type=achievement_type)
        db.session.add(new_achievement)
        db.session.commit()
        
        flash('Достижение успешно создано!', 'success')
        return render_template('achivements/create_achievements.html', events=events)
    
    return render_template('achivements/create_achievements.html')