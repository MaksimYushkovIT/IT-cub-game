from app import create_app
from app import test, spec

app = create_app()

with app.app_context():
    test.populate_db()
    spec.create_special_items()