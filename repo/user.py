from instance.database import db
from models.user import User
from shared.time import now, date_from_string, datetime_from_string

def user_by_id_repo(user_id):
    return db.one_or_404(
        db.select(User).filter_by(id=user_id),
        description=f"No user with id '{user_id}'.",
    )

def register_user_repo(user_data):
    print("in user repo")
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        is_vendor=user_data.is_vendor,
        # for testing, created_at and updated_at are added
        created_at=datetime_from_string(str(now())),
        updated_at=datetime_from_string(str(now()))
    )

    new_user.password = user_data.password

    db.session.add(new_user)
    db.session.commit()