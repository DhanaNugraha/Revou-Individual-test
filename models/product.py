from instance.database import db
from .base import BaseModel


class ProductCategory(db.Model, BaseModel):
    __tablename__ = "product_categories"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"))

    # Self-referential relationship
    subcategories = db.relationship(
        "ProductCategory",
        backref=db.backref("parent", remote_side="ProductCategory.id"),
    )


class SustainabilityAttribute(db.Model, BaseModel):
    __tablename__ = "sustainability_attributes"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(255))


class ProductTag(db.Model, BaseModel):
    __tablename__ = "product_tags"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


class Product(db.Model, BaseModel):
    __tablename__ = "products"

    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    unit_type = db.Column(db.String(20), nullable=False)  # 'piece', 'kg', 'liter', etc.
    stock_quantity = db.Column(db.Integer, nullable=False)
    min_order_quantity = db.Column(db.Integer, default=1)
    is_organic = db.Column(db.Boolean, default=False)
    is_locally_produced = db.Column(db.Boolean, default=False)
    production_location = db.Column(db.String(100))
    carbon_footprint = db.Column(db.Numeric(10, 2))  # in kg CO2 equivalent
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    review_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    images = db.relationship("ProductImage", backref="product", lazy=True)
    sustainability_attributes = db.relationship(
        "ProductSustainability", backref="product", lazy=True
    )
    tags = db.relationship("ProductTagMapping", backref="product", lazy=True)
    reviews = db.relationship("ProductReview", backref="product", lazy=True)
    cart_items = db.relationship("CartItem", backref="product", lazy=True)
    order_items = db.relationship("OrderItem", backref="product", lazy=True)


class ProductImage(db.Model, BaseModel):
    __tablename__ = "product_images"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)


class ProductSustainability(db.Model, BaseModel):
    __tablename__ = "product_sustainability"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    attribute_id = db.Column(
        db.Integer, db.ForeignKey("sustainability_attributes.id"), primary_key=True
    )
    certification_number = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)


class ProductTagMapping(db.Model, BaseModel):
    __tablename__ = "product_tag_mapping"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("product_tags.id"), primary_key=True)
