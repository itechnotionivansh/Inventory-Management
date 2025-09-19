# app/models/category.py
from datetime import datetime
from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship to products
    products = db.relationship('Product', back_populates='category', lazy='dynamic')

    @property
    def product_count(self):
        return self.products.filter_by(is_active=True).count()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'productCount': self.product_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Category {self.name}>"