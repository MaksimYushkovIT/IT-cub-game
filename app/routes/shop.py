from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models.itemM import Item
from ..models.userM import User
from ..extensions import db

shop_blueprint = Blueprint('shop', __name__)

@shop_blueprint.route('/shop')
@login_required
def shop():
    items = Item.query.all()
    user_items = {item.id: current_user.get_item_count(item.id) for item in items}
    return render_template('shop/shop.html', items=items, user_items=user_items)

from flask import jsonify

@shop_blueprint.route('/buy_item/<int:item_id>', methods=['POST'])
@login_required
def buy_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user.cube_coins >= item.price:
        current_user.cube_coins -= item.price
        
        is_new_item = item not in current_user.items
        current_user.add_item(item)
        
        if is_new_item:
            current_user.add_unread_notification(item)
        
        db.session.commit()
        
        response = {
            'success': True, 
            'message': 'Предмет получен!', 
            'cube_coins': current_user.cube_coins,
            'is_new_item': is_new_item
        }
        
        if is_new_item:
            response['new_item'] = {
                'name': item.name,
                'description': item.description,
                'price': item.price
            }
        
        return jsonify(response)
    else:
        return jsonify({'success': False, 'message': 'Недостаточно куб-коинов для покупки.'})

@shop_blueprint.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    if not current_user.is_teacher and not current_user.is_admin:
        return 'У вас нет доступа к этой странице.'
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        item_type = request.form.get('type')
        category = request.form.get('category')
        
        new_item = Item(
            name=name, 
            description=description, 
            price=price,
            type=item_type,
            category=category
        )
        
        db.session.add(new_item)
        db.session.commit()
        flash('Товар создан успешно!', 'success')
        return redirect(url_for('shop.shop'))
    return render_template('shop/create_item.html')