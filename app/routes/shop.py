from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models.itemM import Item
from ..models.userM import User
from ..extensions import db
from ..decorators import admin_required

shop_blueprint = Blueprint('shop', __name__)

@shop_blueprint.route('/shop')
@login_required
def shop():
    items = Item.query.all()
    user_items = {item.id: current_user.get_item_count(item.id) for item in items}
    return render_template('shop/shop.html', items=items, user_items=user_items)



# ... (другие существующие маршруты)

@shop_blueprint.route('/create_item', methods=['GET', 'POST'])
@login_required
@admin_required
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = int(request.form['price'])
        type = request.form['type']
        category = request.form['category']
        
        new_item = Item(name=name, description=description, price=price, type=type, category=category)
        
        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Новый предмет успешно создан!', 'success')
            return redirect(url_for('shop.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании предмета: {str(e)}', 'error')
    
    return render_template('shop/create_item.html')

from flask import jsonify