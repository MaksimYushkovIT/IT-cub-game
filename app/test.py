from .extensions import db
from app.models.disciplineM import Discipline
from app.models.userM import User
from app.models.postM import Post
from app.models.loreM import Lore
from app.models.achievementM import Achievement
from app.models.itemM import Item
from app.models.commentM import Comment
from app.models.factionM import Faction, Rank
from app.models.groupM import  Group
from app.models.eventM import Event
from app.models.projectsM import Project, File
from datetime import datetime, timedelta
from werkzeug.security import  generate_password_hash
def populate_db():
    # Создаем дисциплину
    discipline = Discipline.query.filter_by(name='Программирование').first()
    if not discipline:
        try:
            discipline = Discipline(
                name='Программирование',  # Название дисциплины
                description='Описание дисциплины',  # Описание дисциплины
                created_at=datetime.utcnow(),  # Дата создания дисциплины
                updated_at=datetime.utcnow()  # Дата обновления дисциплины
            )
            db.session.add(discipline)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка добавления дисциплины: {e}")

    discipline = Discipline.query.filter_by(name='VR/AR').first()
    if not discipline:
        try:
            discipline = Discipline(
                name='VR/AR',  # Название дисциплины
                description='Описание дисциплины',  # Описание дисциплины
                created_at=datetime.utcnow(),  # Дата создания дисциплины
                updated_at=datetime.utcnow()  # Дата обновления дисциплины
            )
            db.session.add(discipline)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка добавления дисциплины: {e}")

    # Создаем учителя
    teacher = User.query.filter_by(username='teacher').first()
    if not teacher:
        teacher = User(
            username='teacher',
            email='teacher@teacher.ru',
            last_name='teacher',
            first_name='teacher',
            patronymic='teacher',
            is_teacher=True,
            discipline_id=discipline.id
        )
        teacher.password = generate_password_hash('teacher')
        db.session.add(teacher)
        db.session.commit()

    # Создаем студента
    student = User.query.filter_by(username='student').first()
    if not student:
        student = User(
            username='student',
            email='student@student.ru',
            last_name='student',
            first_name='student',
            patronymic='student',
            discipline_id=discipline.id,
            teacher_id=teacher.id
        )
        student.password = generate_password_hash('student')
        db.session.add(student)
        db.session.commit()

        # Создаем админа
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@admin.ru',
            last_name='Администратор',
            first_name='Администратор',
            patronymic='Администратор',
            is_admin=True
        )
        admin.password = generate_password_hash('admin')
        db.session.add(admin)
        db.session.commit()

    # Создаем пост
    post = Post.query.filter_by(title='Большие вызовы').first()
    if not post:
    
        post = Post(
            title='Большие вызовы',  # Название поста
            description='Уникальная образовательная программа для молодых специалистов и студентов',  # Описание поста
            cover_image='https://steamuserimages-a.akamaihd.net/ugc/958593318905316969/EBB82A15DCE1A3CC8D5CE1A7875680844E838B98/?imw=512&amp;imh=367&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true',  # Ссылка на фото обложки
            content='<!DOCTYPE html>...</html>',  # Основной текст поста
            author_id=teacher.id,  # Используйте объект teacher, а не его идентификатор
            published_at=datetime.now(),  # Дата публикации
            moderation_status='moderated',  # Статус модерации поста
            moderator=teacher,  # Используйте объект teacher, а не его идентификатор
            likes=0,  # Количество лайков
            category='образование',  # Категория поста
            created_at=datetime.utcnow(),  # Дата создания поста
            event_id=None,  # ID события (если есть, иначе None)
            lore_id=None  # ID лора (если есть, иначе None)
        )
        db.session.add(post)
        db.session.commit()

    # Создаем лор
    lore = Lore.query.filter_by(title='Большие вызовы').first()
    if not lore:
        lore = Lore(
            title='Большие вызовы',  # Заголовок лора
            text='Уникальная образовательная программа для молодых специалистов и студентов',  # Текст лора
            category='образование',  # Категория лора
            author_id=teacher.id,
            status='published',  # Статус лора
            views=0,  # Количество просмотров
            rating=0,  # Рейтинг лора
            image='https://steamuserimages-a.akamaihd.net/ugc/958593318905316969/EBB82A15DCE1A3CC8D5CE1A7875680844E838B98/?imw=512&amp;imh=367&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true',  # Изображение лора
            slug='bolshie-vyzovy'  # Slug лора
        )
        db.session.add(lore)
        db.session.commit()

    # Создаем достижение
    achievement = Achievement.query.filter_by(name='Участник программы').first()
    if not achievement:
       # Create an achievement
        achievement = Achievement(
            name='Участник программы',  # Название достижения
            description='Участник образовательной программы',  # Описание достижения
            category='образование',  # Категория достижения
            type='участник',  # Тип достижения
            created_at=datetime.utcnow(),  # Дата создания достижения
            updated_at=datetime.utcnow(),  # Дата обновления достижения
            avatar='https://steamuserimages-a.akamaihd.net/ugc/958593318905316969/EBB82A15DCE1A3CC8D5CE1A7875680844E838B98/?imw=512&amp;imh=367&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true',  # Аватар достижения
            event_id=None  # ID события (если есть, иначе None)
        )
        db.session.add(achievement)
        db.session.commit()

    # Создаем предмет
    item = Item.query.filter_by(name='Книга по программированию').first()
    if not item:
        item = Item(
            name='Книга по программированию',  # Название предмета
            description='Книга по программированию на Python',  # Описание предмета
            type='книга',  # Тип предмета
            category='образование',  # Категория предмета
            price=100,  # Цена предмета
            image='https://example.com/book_image.jpg',  # Изображение предмета
            created_at=datetime.utcnow(),  # Дата создания предмета
            updated_at=datetime.utcnow(),  # Дата обновления предмета
            achievement_id=achievement.id,  # ID достижения (если есть, иначе None)
        )
        db.session.add(item)
        db.session.commit()

    # Создаем комментарий
    comment = Comment.query.filter_by(text='Хорошая книга!').first()
    if not comment:
        comment = Comment(
            text='Хорошая книга!',
            user_id=student.id,
            post_id=post.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(comment)
        db.session.commit()

    # Создаем фракцию
    faction = Faction.query.filter_by(name='Фракция').first()
    if not faction:
        faction = Faction(
            name='Фракция',
            description='Описание фракции',
            leader_id=teacher.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(faction)
        db.session.commit()

    # Создаем ранг
    rank = Rank.query.filter_by(name='Ранг').first()
    if not rank:
        rank = Rank(
            name='Ранг',
            description='Описание ранга',
            faction_id=faction.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session .add(rank)
        db.session.commit()
    
    group = Group.query.filter_by(name='Группа 1').first()
    if not group:
        group = Group(
            name='Группа 1',
            description='Описание группы 1'
        )
        db.session.add(group)
        db.session.commit()
    
    event = Event.query.filter_by(name='Событие 1').first()
    if not event:
        event = Event(
            name='Событие 1',
            description='Описание события 1',
            start_date=datetime.now(),
            end_date=datetime.now(),
            creator_id=teacher.id,
            type='мероприятие',
            importance='средняя'  # Важность мероприятия
        )
        db.session.add(event)
        db.session.commit()
    
    project = Project.query.filter_by(name='Проект 1').first()
    if not project:
        project = Project(
            name='Проект 1',
            description='Описание проекта 1',
            event_id=event.id
        )
    db.session.add(project)
    db.session.commit()

    file = File.query.filter_by(name='Файл 1').first()
    if not file:
        file = File(
            name='Файл 1',
            path='путь к файлу 1',
            project_id=project.id
        )
        db.session.add(file)
        db.session.commit()
