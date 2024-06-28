from website import db
from datetime import datetime
import pytz


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    picture = db.Column(db.String(255))

    def __repr__(self):
        return f"User <{self.email}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Category <{self.name}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)

    category = db.relationship("Category", backref=db.backref("products", lazy=True))

    def __repr__(self):
        return f"Product <{self.name}>"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Kolkata"))
    )

    user = db.relationship("User", backref=db.backref("cart_items", lazy=True))
    product = db.relationship("Product", backref=db.backref("cart_items", lazy=True))

    def __repr__(self):
        return f"Cart <User: {self.user.email}, Product: {self.product.name}>"
