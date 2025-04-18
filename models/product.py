from instance.database import db
from .base import BaseModel

#------------------- assosiation tables for many to many relationship----------------------
product_tag_association = db.Table(
    "product_tag_association",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("product_tags.id")),
)

product_sustainability_association = db.Table(
    "product_sustainability_association",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
    db.Column("sustainability_attribute_id", db.Integer, db.ForeignKey("sustainability_attributes.id")),
)

# -------------------------------------------------------

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
    stock_quantity = db.Column(db.Integer, nullable=False)
    min_order_quantity = db.Column(db.Integer, default=1)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    review_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    images = db.relationship("ProductImage", backref="product", lazy=True)
    sustainability_attributes = db.relationship(
        "SustainabilityAttribute", secondary=product_sustainability_association, backref="product", lazy=True
    )
    tags = db.relationship("ProductTag", secondary=product_tag_association, backref="product", lazy=True)
    reviews = db.relationship("ProductReview", backref="product", lazy=True)
    cart_items = db.relationship("CartItem", backref="product", lazy=True)
    order_items = db.relationship("OrderItem", backref="product", lazy=True)


class ProductImage(db.Model, BaseModel):
    __tablename__ = "product_images"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)




