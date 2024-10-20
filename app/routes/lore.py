from flask import Blueprint, render_template, jsonify, request, abort, redirect, url_for, flash
from ..models.loreM import Lore
from ..models.userM import User
from ..extensions import db
from flask_login import login_required, current_user
from ..decorators import teacher_required
from sqlalchemy.exc import IntegrityError

lore = Blueprint('lore', __name__)

@lore.route('/lore')
def lore_index():
    lores = Lore.query.all()
    return render_template('lore/lore.html', lores=lores)

@lore.route('/lore/<category>')
def lore_category(category):
    lores = Lore.query.filter_by(category=category).all()
    return render_template('lore/lore.html', lores=lores, category=category)

@lore.route('/lore/<int:lore_id>')
def lore_detail(lore_id):
    lore = Lore.query.get_or_404(lore_id)
    return render_template('lore/lore_detail.html', lore=lore)

@lore.route('/api/lore/categories')
def lore_categories():
    categories = ['правила', 'мир', 'факультеты', 'преподаватели']
    return jsonify({'categories': categories})

@lore.route('/api/lore/articles/<category>')
def lore_articles(category):
    lores = Lore.query.filter_by(category=category).all()
    articles = [{'id': lore.id, 'title': lore.title} for lore in lores]
    return jsonify({'articles': articles})

@lore.route('/api/lore/article/<int:article_id>')
def lore_article_content(article_id):
    lore = Lore.query.get_or_404(article_id)
    return jsonify({'content': lore.text})

@lore.route('/lore/category/<category>')
def lore_category_list(category):
    lores = Lore.query.filter_by(category=category).all()
    return render_template('lore/lore_category.html', lores=lores, category=category)

@lore.route('/lore/article/<int:article_id>')
def lore_article(article_id):
    lore = Lore.query.get_or_404(article_id)
    return render_template('lore/lore_article.html', lore=lore)

from flask_login import current_user, login_required

@lore.route('/create_lore', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_lore():
    if not current_user.is_authenticated:
        flash('Пожалуйста, войдите в систему для создания лора.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        category = request.form['category']
        
        new_lore = Lore(
            title=title,
            text=text,
            category=category,
            author_id=current_user.id,  # Убедитесь, что это поле заполнено
            status='draft'
        )
        
        db.session.add(new_lore)
        try:
            db.session.commit()
            flash('Лор успешно создан!', 'success')
            return redirect(url_for('lore.lore'))
        except IntegrityError:
            db.session.rollback()
            flash('Произошла ошибка при создании лора. Пожалуйста, попробуйте еще раз.', 'error')
    
    return render_template('lore/create_lore.html')