import os

class Config(object):
    USER = os.environ.get('POSTGRES_USER', 'myi')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', '0864')
    HOST = os.environ.get('POSTGRES_HOST', '172.18.0.2')
    PORT = os.environ.get('POSTGRES_PORT', '54321')
    DB = os.environ.get('POSTGRES_DB', 'mydb')
    print("Данные подключения к базе данных:")
    print(f"Пользователь: {USER}")
    print(f"Пароль: {PASSWORD}")
    print(f"Хост: {HOST}")
    print(f"Порт: {PORT}")
    print(f"База данных: {DB}")
    

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@172.18.0.2:5432/{DB}'
    print(f"Строка подключения: {SQLALCHEMY_DATABASE_URI}")
    SECRET_KEY = 'dsad314134234biu4t3t43wadw'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

print(f"SQLALCHEMY_DATABASE_URI: {Config.SQLALCHEMY_DATABASE_URI}")