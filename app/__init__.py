from flask import Flask
from config import Config
from .extensions import db, migrate
from .models import userM, groupM, achievementM,factionM, commentM, disciplineM, itemM, loreM, postM, eventM
from .models.userM import User
from .routes.auth import auth
from .routes.post import post
from .routes.shop import shop_blueprint
from .routes.lore import lore
from .routes.achievements import  achievements
from .routes.quests import quests
from .routes.admin import admin
from .routes.faction import faction_blueprint
from .routes.disciplines import disciplines_blueprint
from .routes.student import student
from .routes.others import other
from .routes.items import items
from .forms import loginform, itemform
from flask_login import LoginManager
import app.test as test
import app.models.special_items as spec




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.register_blueprint(other)
    app.register_blueprint(achievements)
    app.register_blueprint(admin)
    app.register_blueprint(post)
    app.register_blueprint(items)
    app.register_blueprint(auth)
    app.register_blueprint(shop_blueprint)
    app.register_blueprint(lore)
    app.register_blueprint(student)
    app.register_blueprint(quests)
    app.register_blueprint(disciplines_blueprint)
    app.register_blueprint(faction_blueprint)
    print(f"SQLALCHEMY_DATABASE_URI in app config: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db.init_app(app)
    migrate.init_app(app, db)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    with app.app_context():
        db.create_all()
        test.populate_db()
        spec.create_special_items()

    
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    return app