# app/models/special_items.py

from ..extensions import db
from .itemM import Item

def create_special_items():
    special_items = [
        {
            "name": "Кот Глеб Валерьянович",
            "description": "Загадочный кот, найденный на секретной странице. Говорят, он приносит удачу в программировании.",
            "image": "static/img/special/cat_gleb.jpg",
            "type": "special",
            "category": "magical",
            "price": 0
        },
        {
            "name": "Квантовый Карандаш",
            "description": "Пишет в нескольких измерениях одновременно. Отлично подходит для многопоточного программирования.",
            "image": "static/img/special/quantum_pencil.jpg",
            "type": "special",
            "category": "futuristic",
            "price": 0
        },
        {
            "name": "Кофейная Кружка Бесконечности",
            "description": "Эта кружка никогда не пустеет. Идеальный компаньон для долгих ночей кодинга.",
            "image": "static/img/special/infinite_coffee.jpg",
            "type": "special",
            "category": "magical",
            "price": 0
        },
        {
            "name": "Очки Дополненной Реальности",
            "description": "Позволяют видеть ошибки в коде без компиляции. Работает только по вторникам.",
            "image": "static/img/special/ar_glasses.jpg",
            "type": "special",
            "category": "futuristic",
            "price": 0
        },
        {
            "name": "Резиновая Уточка Дебаггера",
            "description": "Классическая резиновая уточка для дебаггинга. Эта версия actually понимает ваш код.",
            "image": "static/img/special/debug_duck.jpg",
            "type": "special",
            "category": "realistic",
            "price": 0
        },
        {
            "name": "Волшебная Клавиатура",
            "description": "Клавиатура, которая печатает то, что вы думаете. Использовать с осторожностью!",
            "image": "static/img/special/magic_keyboard.jpg",
            "type": "special",
            "category": "magical",
            "price": 0
        },
        {
            "name": "Нейроинтерфейс Программиста",
            "description": "Подключается напрямую к мозгу. Позволяет писать код силой мысли. Побочный эффект: можете начать видеть мир в двоичном коде.",
            "image": "static/img/special/neurointerface.jpg",
            "type": "special",
            "category": "futuristic",
            "price": 0
        },
        {
            "name": "Амулет Чистого Кода",
            "description": "Древний амулет, который защищает от написания плохого кода. Эффективность 60% времени работает каждый раз.",
            "image": "static/img/special/clean_code_amulet.jpg",
            "type": "special",
            "category": "magical",
            "price": 0
        },
        {
            "name": "Настольная Лампа Эдисона",
            "description": "Оригинальная лампа Томаса Эдисона. Позволяет видеть ошибки в коде в темноте.",
            "image": "static/img/special/edison_lamp.jpg",
            "type": "special",
            "category": "realistic",
            "price": 0
        }
    ]

    for item in special_items:
        existing_item = Item.query.filter_by(name=item["name"]).first()
        if not existing_item:
            new_item = Item(
                name=item["name"],
                description=item["description"],
                image=item["image"],
                type=item["type"],
                category=item["category"],
                price=item["price"]
            )
            db.session.add(new_item)
            db.session.commit()
            print(f"Добавлен предмет: {item['name']}")
