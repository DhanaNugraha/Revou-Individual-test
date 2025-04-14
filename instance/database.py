from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
