from instance.database import db
from .base import BaseModel
from shared import time
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_image_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    is_vendor = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    # Relationships
    addresses = db.relationship("UserAddress", backref="user", lazy=True)
    payment_methods = db.relationship("UserPaymentMethod", backref="user", lazy=True)
    products = db.relationship("Product", backref="vendor", lazy=True)
    orders = db.relationship("Order", backref="customer", lazy=True)
    reviews_written = db.relationship("ProductReview", backref="reviewer", lazy=True)
    # uselist false for one to one. lazy joined to get cart with user.cart
    cart = db.relationship("ShoppingCart", backref="user",  uselist=False, lazy="joined" )

    @property
    def password(self):
        raise AttributeError(
            "Password hash may not be viewed. It is not a readable attribute."
        )

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def update_last_login(self):
        self.last_login = time.now()
        db.session.commit()


class UserAddress(db.Model, BaseModel):
    __tablename__ = "user_addresses"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    address_line1 = db.Column(db.String(100), nullable=False)
    address_line2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    is_default = db.Column(db.Boolean, default=False)


class UserPaymentMethod(db.Model, BaseModel):
    __tablename__ = "user_payment_methods"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    payment_type = db.Column(
        db.String(20), nullable=False
    )  # 'credit_card', 'paypal', 'bank_transfer'
    provider = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.Date)
    is_default = db.Column(db.Boolean, default=False)
