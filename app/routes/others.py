from flask import Blueprint, render_template, jsonify
from datetime import datetime
from flask_login import login_required, current_user
from ..models.itemM import Item
from ..extensions import db
from random import choice

other = Blueprint('other', __name__)

@other.route('/how')
def how():
    return render_template('abouthus/how.html')

@other.route('/team')
def team():
    return render_template('abouthus/team.html')

@other.route('/about')
def about():
    return render_template('abouthus/about.html')

from datetime import datetime

@other.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

@other.route('/pashalka')
@login_required
def pashalka():
    return render_template('student/pashalka.html')

@other.route('/get_cat_item', methods=['POST'])
@login_required
def get_cat_item():
    # Получаем все специальные предметы
    special_items = Item.query.filter_by(type='special').all()
    
    if not special_items:
        return jsonify({'success': False, 'message': 'К сожалению, специальные предметы закончились!'})
    
    # Выбираем случайный предмет из списка специальных предметов
    random_item = choice(special_items)
    
    # Проверяем, есть ли у пользователя уже этот предмет
    if random_item in current_user.items:
        return jsonify({'success': False, 'message': f'У вас уже есть {random_item.name}. Попробуйте еще раз!'})
    
    # Добавляем предмет пользователю
    current_user.items.append(random_item)
    db.session.commit()
    
    # Создаем уведомление о новом предмете
    current_user.add_unread_notification(random_item)
    
    return jsonify({
        'success': True,
        'message': f'Вы получили {random_item.name}! Проверьте свой инвентарь.',
        'item_name': random_item.name,
        'item_description': random_item.description
    })