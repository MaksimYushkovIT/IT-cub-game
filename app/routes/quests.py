from ..models.userM import User
from ..models.eventM import Event
from ..extensions import db
from flask_login import current_user, login_required
from datetime import datetime
from ..models.postM import Post
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ..models.projectsM import Project
from ..decorators import teacher_required
from werkzeug.utils import secure_filename
import os

quests = Blueprint('quests', __name__)

@quests.route('/quests')
@login_required
def index():
    events = Event.query.filter(Event.users.contains(current_user)).all()
    return render_template('quests/index.html', events=events, current_time=datetime.now())

@quests.route('/quests/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        event = Event(
            name=request.form['name'],
            description=request.form['description'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date'],
            creator_id=current_user.id,
            type=request.form['type'],
            experience=request.form.get('experience', 0),
            money_reward=request.form.get('money_reward', 0),
            participation_points=request.form.get('participation_points', 0),
            victory_points=request.form.get('victory_points', 0),
            importance=request.form['importance'],
            is_completed=False,
            completion_date=None
        )
        db.session.add(event)
        db.session.commit()

        # Создание нового поста
        post = Post(
            title=event.name,
            description=event.description,
            cover_image='',  # Вы можете добавить изображение по умолчанию
            content=event.description,
            author_id=current_user.id,
            category='event',  # или любая другая подходящая категория
            published_at=datetime.now(),
            moderation_status='pending',  # Пост будет ожидать модерации
            event_id=event.id  # связываем пост с событием
        )
        db.session.add(post)
        db.session.commit()

        flash('Квест успешно создан и отправлен на модерацию', 'success')
        return redirect(url_for('quests.index'))
    return render_template('quests/create.html')

@quests.route('/quests/<int:event_id>')
def show(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('quests/show.html', event=event)

@quests.route('/quests/<int:event_id>/edit', methods=['GET', 'POST'])
def edit(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.name = request.form['name']
        event.description = request.form['description']
        event.start_date = request.form['start_date']
        event.end_date = request.form['end_date']
        db.session.commit()
        return redirect(url_for('quests.index'))
    return render_template('quests/edit.html', event=event)

@quests.route('/join/<int:event_id>', methods=['POST'])
def join(event_id):
    event = Event.query.get(event_id)
    if event:
        if current_user not in event.users:
            event.users.append(current_user)
            db.session.commit()
            flash('Вы успешно присоединились к квесту!')
        else:
            flash('Вы уже присоединились к этому квесту!')
    return redirect(url_for('quests.index'))

@quests.route('/leave/<int:event_id>', methods=['POST'])
def leave(event_id):
    event = Event.query.get(event_id)
    if event:
        if current_user in event.users:
            event.users.remove(current_user)
            db.session.commit()
            flash('Вы успешно покинули квест!')
        else:
            flash('Вы не присоединились к этому квесту!')
    return redirect(url_for('quests.index'))

@quests.route('/create_project/<int:event_id>', methods=['GET', 'POST'])
@login_required
def create_project(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        passport_link = request.form.get('passport_link')
        materials_link = request.form.get('materials_link')
        presentation_link = request.form.get('presentation_link')
        
        new_project = Project(
            name=name,
            description=description,
            status=status,
            event_id=event.id,
            passport_link=passport_link,
            materials_link=materials_link,
            presentation_link=presentation_link
        )
        new_project.project_students.append(current_user)
        
        db.session.add(new_project)
        db.session.commit()
        
        flash('Проект успешно создан!', 'success')
        return redirect(url_for('quests.index'))
    
    current_time = datetime.now()
    return render_template('quests/create_project.html', event=event, current_time=current_time)

@quests.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Проверка, является ли текущий пользователь участником проекта
    if current_user not in project.project_students:
        flash('У вас нет доступа к этому проекту', 'error')
        return redirect(url_for('quests.index'))

    if request.method == 'POST':
        # Обновление основной информации о проекте
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        project.status = request.form.get('status')

        # Обработка загрузки файлов
        for file_type in ['passport', 'materials', 'presentation']:
            if file_type in request.files:
                file = request.files[file_type]
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    setattr(project, f'{file_type}_link', file_path)

        db.session.commit()
        flash('Проект успешно обновлен', 'success')
        return redirect(url_for('quests.index'))

    return render_template('quests/edit_project.html', project=project)

@quests.route('/reward_participants/<int:event_id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def reward_participants(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        # наградите участников
        pass
    return render_template('quests/reward_participants.html', event=event)