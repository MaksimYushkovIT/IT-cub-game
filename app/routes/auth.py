from flask import Blueprint,jsonify, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.userM import User
from ..models.itemM import Item
from ..extensions import db
from functools import wraps
from ..forms.loginform import LoginForm
from flask_login import login_user, current_user, LoginManager
from ..models.disciplineM import Discipline
from ..models.groupM import Group  # Импортируйте модель Group

auth = Blueprint('auth', __name__)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите в систему, чтобы получить доступ к этой странице.'

# Загрузка пользователя по user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        patronymic = request.form.get('patronymic')
        group = request.form.get('group')
        teacher_id = request.form.get('teacher_id')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Проверка на то, что пользователь уже существует в базе данных
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('Пользователь с таким email или никнеймом уже существует.', 'danger')
            return redirect(url_for('auth.register'))

        # Проверка на то, что пароли совпадают
        if password != confirm_password:
            flash('Пароли не совпадают. Попробуйте еще раз.', 'danger')
            return redirect(url_for('auth.register'))

        # Проверка на то, что данные из формы правильно передаются в функцию
        if not username or not last_name or not first_name or not patronymic or not group or not teacher_id or not email or not password:
            flash('Пожалуйста, заполните все поля.', 'danger')
            return redirect(url_for('auth.register'))

        # Создание нового пользователя
        new_user = User(
            username=username,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            group=group,
            teacher_id=teacher_id,
            email=email,
            password=generate_password_hash(password),
            status='новичок',
            level=1,
            cube_coins=0,
            experience=0,
            position='ученик',
            is_teacher=False,
            is_admin=False
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Вы можете войти в систему.', 'success')
        return redirect(url_for('auth.login'))
    else:
        try:
            teachers = User.query.filter_by(is_teacher=True).all()
        except Exception as e:
            teachers = []
            print(f"Ошибка при получении педагогов: {e}")

        return render_template('auth/register.html', teachers=teachers)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему, чтобы получить доступ к этой странице.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function

@auth.route('/profile')
@login_required
def own_profile():
    return redirect(url_for('auth.view_profile', user_id=current_user.id))

@auth.route('/logout')
@login_required
def logout():
    if 'user_id' in session:
        session.clear()
        flash('Вы вышли из системы', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Вы не авторизованы', 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Пользователь не найден', 'danger')
            return redirect(url_for('auth.login'))

        if user and user.check_password(password):
            login_user(user)
            session['user_id'] = user.id
            print("User ID stored in session:", session.get('user_id'))
            print("Current user:", current_user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('post.index'))
        else:
            flash('Неправильный email или пароль.', 'error')

    return render_template('auth/login.html', form=form)

@auth.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        username = request.form.get('username')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        patronymic = request.form.get('patronymic')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка на существование пользователя с таким же email или username
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('Пользователь с таким email или username уже существует.', 'danger')
            return redirect(url_for('auth.register_teacher'))

        # Проверка на правильность пароля
        if not password:
            flash('Пароль не может быть пустым.', 'danger')
            return redirect(url_for('auth.register_teacher'))

        # Создание нового пользователя
        new_user = User(
            username=username,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            email=email,
            password=generate_password_hash(password),
            is_teacher=True
        )

        # Добавление нового пользователя в базу данных
        db.session.add(new_user)

        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register_teacher.html')

@auth.route('/profile/<int:user_id>')
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return render_template('auth/admin_profile.html', user=user)
    elif user.is_teacher:
        return render_template('auth/teacher_profile.html', user=user)
    else:
        return render_template('auth/student_profile.html', user=user)

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    groups = Group.query.all()
    if request.method == 'POST':
        if current_user.is_admin:
            current_user.username = request.form.get('username', current_user.username)
            current_user.contact_info = request.form.get('contact_info', current_user.contact_info)
        elif current_user.is_teacher:
            current_user.username = request.form.get('username', current_user.username)
            current_user.last_name = request.form.get('last_name', current_user.last_name)
            current_user.first_name = request.form.get('first_name', current_user.first_name)
            current_user.patronymic = request.form.get('patronymic', current_user.patronymic)
            current_user.birthday = request.form.get('birthday', current_user.birthday)
            current_user.avatar = request.form.get('avatar', current_user.avatar)
            current_user.bio = request.form.get('bio', current_user.bio)
            current_user.pedstage = request.form.get('pedstage', current_user.pedstage)
            current_user.contact_info = request.form.get('contact_info', current_user.contact_info)
            current_user.telegram_link = request.form.get('telegram_link', current_user.telegram_link)
            current_user.discord_link = request.form.get('discord_link', current_user.discord_link)
        else:
            # Код для редактирования профиля ученика остается прежним
            current_user.username = request.form.get('username', current_user.username)
            current_user.last_name = request.form.get('last_name', current_user.last_name)
            current_user.first_name = request.form.get('first_name', current_user.first_name)
            current_user.patronymic = request.form.get('patronymic', current_user.patronymic)
            current_user.birthday = request.form.get('birthday', current_user.birthday)
            current_user.avatar = request.form.get('avatar', current_user.avatar)
            current_user.bio = request.form.get('bio', current_user.bio)
            current_user.contact_info = request.form.get('contact_info', current_user.contact_info)
            current_user.telegram_link = request.form.get('telegram_link', current_user.telegram_link)
            current_user.discord_link = request.form.get('discord_link', current_user.discord_link)
            current_user.status = request.form.get('status', current_user.status)
            current_user.level = request.form.get('level', current_user.level)
            current_user.cube_coins = request.form.get('cube_coins', current_user.cube_coins)
            current_user.experience = request.form.get('experience', current_user.experience)
            current_user.registered_at = request.form.get('registered_at', current_user.registered_at)
            current_user.role = request.form.get('role', current_user.role)
            assigned_teacher_id = request.form.get('assigned_teacher_id')
            new_group_name = request.form.get('group')
            if assigned_teacher_id:
                current_user.assigned_teacher_id = assigned_teacher_id
            else:
                current_user.assigned_teacher_id = None
            if new_group_name:
                new_group = Group.query.filter_by(name=new_group_name).first()
                if new_group:
                    if new_group not in current_user.groups:
                        current_user.groups = [new_group]
            
            current_user.telegram_link = request.form.get('telegram_link', current_user.telegram_link)
            current_user.discord_link = request.form.get('discord_link', current_user.discord_link)
        
        db.session.commit()
        flash('Ваш профиль был обновлен!', 'success')
        return redirect(url_for('auth.own_profile'))
    
    return render_template('auth/edit_profile.html', user=current_user, groups=groups)

@auth.route('/get_unread_notifications')
@login_required
def get_unread_notifications():
    notifications = current_user.get_unread_notifications()
    notification_data = []
    for notification in notifications:
        item = Item.query.get(notification.item_id)
        notification_data.append({
            'name': item.name,
            'description': item.description,
            'price': item.price
        })
    current_user.clear_unread_notifications()
    return jsonify(notification_data)