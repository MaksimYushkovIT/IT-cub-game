import os
class Config(object):
    USER = os.environ.get('POSTGRES_USER', ' myi')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', '0864')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT','5532')
    DB = os.environ.get('POSTGRES_DB', 'mydb')


    SQLALCHEMY_DATABASE_URI= f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = 'dsad314134234biu4t3t43wadw'
    SQLALCHEMY_TRACK_MODIFICATIONS = True