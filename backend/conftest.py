import pytest
import os
import sqlite3
from app import create_app
from app.database import init_db, DB_PATH

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        init_db(app)
        yield app
        
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)