from flask import Blueprint, redirect, render_template, url_for, request, jsonify, abort, flash
from ..extensions import db
from ..models.postM import Post
from ..models.commentM import Comment
from datetime import datetime
from ..models.userM import User
from ..models.projectsM import Project
from flask import url_for
from flask_login import current_user, login_required

post = Blueprint('post', __name__)

from ..models.userM import User
from flask import redirect, url_for
from flask_login import current_user

@post.route('/index')
@post.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('other.how'))
    posts = Post.query.all()
    user_events = [event.id for event in current_user.events] if current_user.is_authenticated else []
    teachers = User.query.filter_by(is_teacher=True).all()
    return render_template("student/index.html", posts=posts, user_events=user_events, teachers=teachers)

@post.route('/post/new', methods=['GET'])
def new_post():
    return render_template("post/create-post.html")

# Создание нового поста
@post.route('/post/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        new_post = Post(
            title=request.form['title'],
            description=request.form['description'],
            content=request.form['content'],
            author_id=current_user.id,
            created_at=datetime.utcnow(),
            published_at=datetime.utcnow(),
            cover_image=request.form['cover_image'],
            moderation_status='approved' if current_user.is_teacher or current_user.is_admin else 'pending'
        )
        if not current_user.is_admin and not current_user.is_teacher:
            post.moderation_status = 'pending'
        db.session.add(new_post)
        db.session.commit()
        flash('Пост создан успешно', 'success')
        return redirect(url_for('post.index'))
    return render_template('/post/create_post.html')

# Получение всех постов
@post.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'cover_image': post.cover_image,
        'content': post.content,
        'author': post.author,
        'created_at': post.created_at,
        'published_at': post.published_at,
        'subject': post.subject,  # Добавлено поле subject
        'is_completed': post.is_completed,  # Добавлено поле is_completed
        'completion_date': post.completion_date,  # Добавлено поле completion_date
        'importance': post.importance,  # Добавлено поле importance
        'experience_points': post.experience_points,  # Добавлено поле experience_points
        'money_reward': post.money_reward,  # Добавлено поле money_reward
        'participation_points': post.participation_points,  # Добавлено поле participation_points
        'victory_points': post.victory_points,  # Добавлено поле victory_points
    } for post in posts]), 200

# Получение поста по ID
@post.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'cover_image': post.cover_image,
        'content': post.content,
        'author': post.author,
        'created_at': post.created_at,
        'published_at': post.published_at,
        'subject': post.subject,  # Добавлено поле subject
        'is_completed': post.is_completed,  # Добавлено поле is_completed
        'completion_date': post.completion_date,  # Добавлено поле completion_date
        'importance': post.importance,  # Добавлено поле importance
        'experience_points': post.experience_points,  # Добавлено поле experience_points
        'money_reward': post.money_reward,  # Добавлено поле money_reward
        'participation_points': post.participation_points,  # Добавлено поле participation_points
        'victory_points': post.victory_points,  # Добавлено поле victory_points
    }), 200

# Обновление поста
@post.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author_id and not current_user.is_admin and not current_user.is_teacher:
        abort(403)  # Запрещаем редактирование, если пользователь не автор и не админ
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.description = request.form['description']
        post.content = request.form['content']
        post.cover_image = request.form['cover_image']
        post.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Пост успешно обновлен', 'success')
        return redirect(url_for('post.view_post', post_id=post.id))
    
    return render_template('post/edit_post.html', post=post)

# Удаление поста
@post.route('/post/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Пост был успешно удален!', 'success')  # Сообщение об успехе
    else:
        flash('Пост не найден!', 'error')  # Сообщение об ошибке
    return redirect(url_for('post.index'))  # Перенаправление на главную страницу новостей

@post.route('/leave_post/<int:post_id>', methods=['POST'])
@login_required
def leave_post(post_id):
    post = Post.query.get_or_404(post_id)
    event = post.event
    if event and current_user in event.users:
        event.users.remove(current_user)
        # Удаляем пользователя из проекта
        project = Project.query.filter_by(event_id=event.id).filter(Project.project_students.any(id=current_user.id)).first()
        if project:
            project.project_students.remove(current_user)
            if not project.project_students:
                db.session.delete(project)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'success'})
        else:
            return redirect(url_for('post.index'))
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': 'Вы не участник этого события.'})
        else:
            flash('Вы не участник этого события.', 'error')
            return redirect(url_for('post.index'))

@post.route('/post/view/<int:post_id>')
def view_post(post_id):
    post = Post.query.get(post_id)
    if post:
        teachers = User.query.filter_by(is_teacher=True). all()
        return render_template('post/post.html', post=post, teachers=teachers)
    return abort(404)
    
@post.route('/post/<int:post_id>/add_comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get(post_id)
    if post:
        comment_text = request.form.get('comment')
        if comment_text and comment_text.strip():  # Проверяем, что текст комментария не пустой
            new_comment = Comment(text=comment_text, author=current_user, post=post)
            db.session.add(new_comment)
            db.session.commit()
            flash('Комментарий добавлен успешно!', 'success')
        else:
            flash('Комментарий не может быть пустым!', 'error')
    return redirect(url_for('post.view_post', post_id=post_id))

from flask_login import current_user, login_required

@post.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    try:
        if current_user in post.liked_by:
            post.liked_by.remove(current_user)
            status = 'unliked'
        else:
            post.liked_by.append(current_user)
            status = 'liked'
        
        # Пересчитываем количество лайков
        post.likes = len(post.liked_by)
        
        db.session.commit()
        print(f"Post {post_id} {status} by user {current_user.id}. Total likes: {post.likes}")  # Лог для отладки
        return jsonify({'status': status, 'likes': post.likes})
    except Exception as e:
        db.session.rollback()
        print(f"Error liking post {post_id}: {str(e)}")  # Лог для отладки
        return jsonify({'status': 'error', 'message': str(e)}), 500

@post.route('/join_post/<int:post_id>', methods=['POST'])
@login_required
def join_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.is_authenticated:
        if current_user not in post.event.users:
            post.event.users.append(current_user)
            db.session.commit()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'status': 'success'})
            else:
                flash('Вы успешно присоединились к событию!', 'success')
                return redirect(url_for('post.view_post', post_id=post.id))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'status': 'already_joined'})
            else:
                flash('Вы уже присоединились к этому событию!', 'info')
                return redirect(url_for('post.view_post', post_id=post.id))
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'error'}), 401
    else:
        flash('Вы должны войти в систему, чтобы присоединиться к событию!', 'error')
        return redirect(url_for('auth.login'))

    
@post.route('/approve_post/<int:post_id>', methods=['POST'])
@login_required
def approve_post(post_id):
    if not current_user.is_teacher and not current_user.is_admin:
        flash('У вас нет доступа к этому действию', 'error')
        return redirect(url_for('post.index'))
    post = Post.query.get_or_404(post_id)
    post.moderation_status = 'approved'
    db.session.commit()
    flash('Пост одобрен', 'success')
    return redirect(url_for('post.index'))

@post.route('/reject_post/<int:post_id>', methods=['POST'])
@login_required
def reject_post(post_id):
    if not current_user.is_teacher and not current_user.is_admin:
        flash('У вас нет доступа к этому действию', 'error')
        return redirect(url_for('post.index'))
    post = Post.query.get_or_404(post_id)
    post.moderation_status = 'rejected'
    db.session.commit()
    flash('Пост отклонен', 'success')
    return redirect(url_for('post.index'))

@post.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user.is_teacher or current_user.is_admin:
        post_id = comment.post_id
        db.session.delete(comment)
        db.session.commit()
        flash('Комментарий был успешно удален!', 'success')
    else:
        flash('У вас нет прав для удаления этого комментария.', 'error')
    return redirect(url_for('post.view_post', post_id=post_id))