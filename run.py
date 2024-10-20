import os
import sys


# Добавляем директорию проекта в путь поиска модулей
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

from app import create_app
from app.extensions import db, migrate

from dotenv import load_dotenv
load_dotenv(os.path.join(project_dir, '.env'))

app = create_app()

if __name__ == '__main__':
    app.run()