import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_auth.py -v -s --cov=.

def test_register_user(client, db, mock_user_data ,users_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201
    assert register_user.json["success"] is True

    user = db.session.execute(
        db.select(models.User).filter_by(email=mock_user_data["email"])
    ).scalar_one()

    assert user.id == 3
    assert user.username == mock_user_data["username"]
    assert user.email == mock_user_data["email"]
    assert user.is_vendor is False

def test_register_user_username_validation_error(client, db, mock_user_data, users_data_inject):
    # test < 3 characters username
    mock_user_data["username"] = ""
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test non alphanumeric and underscore characters username
    mock_user_data["username"] = "@----@"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

def test_register_user_password_validation_error(
    client, db, mock_user_data, users_data_inject
):
    # test < 8 characters username
    mock_user_data["password"] = "1234567"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

def test_register_user_email_validation_error(
    client, db, mock_user_data, users_data_inject
):
    # test empty email
    mock_user_data["email"] = ""
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test invalid email pattern
    mock_user_data["email"] = "invalid_email_pattern"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test consecutive dots in email
    mock_user_data["email"] = "a@bc..com"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test email too long
    mock_user_data["email"] = "a" * 256 + "@example.com"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

def test_register_user_duplicates(
    client, db, mock_user_data, users_data_inject
):
    # test email already exist
    mock_user_data["email"] = "john.doe@example.com"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 500
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view create user repo"

    # test username already exist
    mock_user_data["username"] = "john"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 500
    assert register_user.json["success"] is False




# register ->
# validation error
# conflict error (email exist)
# success



# schemas\auth.py                   31      7    100%
# views\auth.py                     16      5    81%






