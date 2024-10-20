from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from ..models.itemM import Item
from ..models.userM import User
from ..extensions import db
from ..decorators import admin_required, teacher_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

items = Blueprint('items', __name__)

@items.route('/add_item_to_user', methods=['POST'])
@login_required
def add_item_to_user():
    data = request.json
    user_id = data.get('user_id')
    item_id = data.get('item_id')
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)

    # Если user_id не указан, используем текущего пользователя
    if not user_id:
        user = current_user
    else:
        # Проверяем, имеет ли текущий пользователь права на добавление предметов другим пользователям
        if not current_user.is_admin and not current_user.is_teacher:
            return jsonify({'success': False, 'message': 'У вас нет прав на это действие'}), 403
        user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404

    # Находим предмет по id или имени
    if item_id:
        item = Item.query.get(item_id)
    elif item_name:
        item = Item.query.filter_by(name=item_name).first()
    else:
        return jsonify({'success': False, 'message': 'Необходимо указать item_id или item_name'}), 400

    if not item:
        return jsonify({'success': False, 'message': 'Предмет не найден'}), 404

    # Проверяем, есть ли у пользователя уже этот предмет (если это уникальный предмет)
    if item.unique and item in user.items:
        return jsonify({'success': False, 'message': f'У пользователя уже есть предмет "{item.name}"'}), 400

    # Добавляем предмет пользователю
    for _ in range(quantity):
        user.items.append(item)
        user.add_unread_notification(item)  # Создаем уведомление для каждого добавленного предмета

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Предмет "{item.name}" успешно добавлен пользователю {user.username}',
        'user_id': user.id,
        'item_id': item.id,
        'quantity': quantity
    })

@items.route('/remove_item_from_user', methods=['POST'])
@login_required
def remove_item_from_user():
    data = request.json
    user_id = data.get('user_id')
    item_id = data.get('item_id')
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)

    # Если user_id не указан, используем текущего пользователя
    if not user_id:
        user = current_user
    else:
        # Проверяем, имеет ли текущий пользователь права на удаление предметов у других пользователей
        if not current_user.is_admin and not current_user.is_teacher:
            return jsonify({'success': False, 'message': 'У вас нет прав на это действие'}), 403
        user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404

    # Находим предмет по id или имени
    if item_id:
        item = Item.query.get(item_id)
    elif item_name:
        item = Item.query.filter_by(name=item_name).first()
    else:
        return jsonify({'success': False, 'message': 'Необходимо указать item_id или item_name'}), 400

    if not item:
        return jsonify({'success': False, 'message': 'Предмет не найден'}), 404

    # Проверяем, есть ли у пользователя достаточное количество предметов
    user_items = [i for i in user.items if i.id == item.id]
    if len(user_items) < quantity:
        return jsonify({'success': False, 'message': 'У пользователя недостаточно предметов для удаления'}), 400

    # Удаляем предметы у пользователя
    for _ in range(quantity):
        user.items.remove(item)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Предмет "{item.name}" успешно удален у пользователя {user.username}',
        'user_id': user.id,
        'item_id': item.id,
        'quantity': quantity
    })

@items.route('/get_user_items', methods=['GET'])
@login_required
def get_user_items():
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    
    if user_id:
        # Проверяем права на просмотр инвентаря других пользователей
        if not current_user.is_admin and not current_user.is_teacher and int(user_id) != current_user.id:
            return jsonify({'success': False, 'message': 'У вас нет прав на просмотр инвентаря этого пользователя'}), 403
        user = User.query.get(user_id)
    else:
        user = current_user

    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404

    # Базовый запрос
    query = db.session.query(Item, func.count(Item.id).label('quantity'))\
        .join(User.items)\
        .filter(User.id == user.id)\
        .group_by(Item.id)

    # Фильтрация по категории, если указана
    if category:
        query = query.filter(Item.category == category)

    # Выполняем запрос и формируем результат
    items_data = query.all()
    
    items_list = [{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'category': item.category,
        'image_url': item.image_url,
        'quantity': quantity
    } for item, quantity in items_data]

    return jsonify({
        'success': True,
        'user_id': user.id,
        'username': user.username,
        'items': items_list
    })

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from ..models.itemM import Item
from ..models.userM import User
from ..extensions import db
from sqlalchemy.exc import IntegrityError

items = Blueprint('items', __name__)

@items.route('/buy_item', methods=['POST'])
@login_required
def buy_item():
    data = request.json
    item_id = data.get('item_id')
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found'}), 404
    
    if current_user.cube_coins < item.price:
        return jsonify({'success': False, 'message': 'Not enough cube coins'}), 400
    
    current_user.cube_coins -= item.price
    current_user.items.append(item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Item purchased successfully', 'new_balance': current_user.cube_coins})

@items.route('/receive_item', methods=['POST'])
@login_required
def receive_item():
    data = request.json
    item_id = data.get('item_id')
    item_name = data.get('item_name')
    quantity = data.get('quantity', 1)
    user_id = data.get('user_id')  # Опционально, для администраторов и учителей

    # Проверка прав доступа, если указан user_id
    if user_id and user_id != current_user.id:
        if not current_user.is_admin and not current_user.is_teacher:
            return jsonify({'success': False, 'message': 'У вас нет прав на это действие'}), 403
        user = User.query.get(user_id)
    else:
        user = current_user

    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404

    # Находим предмет по id или имени
    if item_id:
        item = Item.query.get(item_id)
    elif item_name:
        item = Item.query.filter_by(name=item_name).first()
    else:
        return jsonify({'success': False, 'message': 'Необходимо указать item_id или item_name'}), 400

    if not item:
        return jsonify({'success': False, 'message': 'Предмет не найден'}), 404

    try:
        # Начинаем транзакцию
        db.session.begin_nested()

        # Добавляем предметы пользователю
        for _ in range(quantity):
            user.items.append(item)
            user.add_unread_notification(item)  # Создаем уведомление для каждого полученного предмета

        # Сохраняем изменения
        db.session.commit()

    except IntegrityError:
        # Если произошла ошибка, откатываем транзакцию
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Произошла ошибка при получении предмета'}), 500

    return jsonify({
        'success': True,
        'message': f'Успешно получен предмет "{item.name}" в количестве {quantity}',
        'user_id': user.id,
        'username': user.username,
        'item_id': item.id,
        'item_name': item.name,
        'quantity': quantity,
        'new_item': {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'image_url': item.image_url
        }
    })



@items.route('/view_inventory', methods=['GET'])
@login_required
def view_inventory():
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    
    if user_id and str(user_id) != str(current_user.id):
        if not current_user.is_admin and not current_user.is_teacher:
            return jsonify({'success': False, 'message': 'У вас нет прав на просмотр инвентаря этого пользователя'}), 403
        user = User.query.get(user_id)
    else:
        user = current_user

    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'}), 404

    # Базовый запрос
    query = db.session.query(Item, func.count(Item.id).label('quantity'))\
        .join(User.items)\
        .filter(User.id == user.id)\
        .group_by(Item.id)

    # Фильтрация по категории, если указана
    if category:
        query = query.filter(Item.category == category)

    # Выполняем запрос и формируем результат
    items_data = query.all()
    
    inventory = [{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'category': item.category,
        'image_url': item.image,
        'quantity': quantity
    } for item, quantity in items_data]

    return jsonify({
        'success': True,
        'message': 'Инвентарь успешно загружен',
        'user_id': user.id,
        'username': user.username,
        'inventory': inventory
    })