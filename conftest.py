import pytest
from middleware.before_request import auth_middleware
from config.settings import create_app
from instance.database import db as _db
from shared.time import now_testing, testing_datetime
import os

@pytest.fixture
def test_app():
    config_module = os.environ["FLASK_CONFIG"] = "config.testing"
    app = create_app(config_module)
    auth_middleware(app)
    with app.app_context():
        _db.create_all()
        _db.session.rollback()

    yield app

    with app.app_context():
        _db.session.rollback()
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(test_app):
    with test_app.app_context():
        yield _db

@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client  
    # print("Tearing down the test client")

