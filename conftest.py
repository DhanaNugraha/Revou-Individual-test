import pytest
from config.settings import create_app
from instance.database import db as _db
import models
from shared.time import datetime_from_string, now
import os

@pytest.fixture
def test_app():
    config_module = os.environ["FLASK_CONFIG"] = "config.testing"
    app = create_app(config_module)
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


@pytest.fixture
def users_data_inject(test_app):
    users_data = [
        {
            "id": 1,
            "username": "john",
            "email": "john.doe@example.com",
            "password_hash": "testing/password",
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
            "is_vendor": False,
        },
        {
            "id": 2,
            "username": "jane",
            "email": "jane.smith@example.com",
            "password_hash": "testing/password",
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
            "is_vendor": False,
        },
    ]
    with test_app.app_context():
        users_list = []
        for user in users_data:
            user_model = models.User(**user)
            users_list.append(user_model)

        _db.session.add_all(users_list)
        _db.session.commit()

        return users_list
    

@pytest.fixture
def mock_user_data():
    return {
        "username": "eco_buyer",
        "email": "buyer@example.com",
        "password": "sustainable123",
    }

@pytest.fixture
def mock_login_data():
    return {
        "email": "buyer@example.com",
        "password": "sustainable123",
    }

@pytest.fixture
def mock_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDgxMjcxNSwianRpIjoiYTg1NDlkZjctYjJlNS00MWVkLWJlNzktMWY0NmNjMzZiNDk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDQ4MTI3MTUsImNzcmYiOiJiOWNkN2E4NC04YjUyLTQ5ZWEtYjY2ZC1jNTU3ZDQ1MzUzYzEiLCJ1c2VybmFtZSI6ImVjb19idXllciIsImVtYWlsIjoiYnV5ZXJAZXhhbXBsZS5jb20iLCJpc192ZW5kb3IiOmZhbHNlLCJpc19hZG1pbiI6ZmFsc2V9.4c1EcKMgb__oQLqBjptFxjl9_up9hbPXzNuguQZRGQQ"
    }

@pytest.fixture
def mock_update_user_data():
    return {
        "bio": "test update bio",
        "first_name": "test update first name",
        "last_name": "test update last name",
    }

@pytest.fixture
def mock_vendor_data():
    return {
        "username": "eco_seller",
        "email": "seller@example.com",
        "password": "sustainable123",
        "is_vendor": True
    }


@pytest.fixture
def mock_vendor_login_data():
    return {
        "email": "seller@example.com",
        "password": "sustainable123",
    }


@pytest.fixture
def mock_vendor_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDkwMzY4MCwianRpIjoiODczZjM4OTMtMWRjYy00YTRmLThlNTYtYWEzYWFhNTA4N2M1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDQ5MDM2ODAsImNzcmYiOiJhMzU4YTczOS1lOTA3LTQ4YzItOTI3YS00ZGM4MmRmNjhkMjIiLCJ1c2VybmFtZSI6ImVjb19zZWxsZXIiLCJlbWFpbCI6InNlbGxlckBleGFtcGxlLmNvbSIsImlzX3ZlbmRvciI6dHJ1ZSwiaXNfYWRtaW4iOmZhbHNlfQ.wxF4C495DnFjDn3Vq4K7g1VSnCT9Xci8BblYi7ALIkY"
    }

@pytest.fixture
def mock_create_product_data():
    return {
        "name": "testproduct",
        "description": "test product description",
        "price": 25.99,
        "tags": ["eco-friendly", "handmade"],
        "sustainability_attributes": ["organic", "carbon-neutral"],
        "stock_quantity": 100,
        "min_order_quantity": 2,
    }
