import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import create_app

@pytest.fixture(scope="session")
def app():
    # Creamos la app en modo testing
    app = create_app({"TESTING": True})
    app.config.update({"TESTING": True})
    yield app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
