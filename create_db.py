from app.db import DB
from app.app import create_app
from app.models import seed_test_data

if __name__ == "__main__":
    DB.app = create_app()
    DB.create_all()
    DB.seed_test_data()