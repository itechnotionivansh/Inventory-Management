# app/models/product.py
from datetime import datetime
from app.extensions import db
import json

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    colors_json = db.Column(db.Text)  # Store colors as JSON string
    tags_json = db.Column(db.Text)    # Store tags as JSON string
    rating_rate = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    category = db.relationship('Category', back_populates='products')
    uploader = db.relationship('User', foreign_keys=[uploader_id], back_populates='uploaded_products')

    @property
    def colors(self):
        return json.loads(self.colors_json) if self.colors_json else []

    @colors.setter
    def colors(self, value):
        self.colors_json = json.dumps(value) if value else None

    @property
    def tags(self):
        return json.loads(self.tags_json) if self.tags_json else []

    @tags.setter
    def tags(self, value):
        self.tags_json = json.dumps(value) if value else None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name if self.category else None,
            'price': float(self.price),
            'colors': self.colors,
            'tags': self.tags,
            'rating': {
                'rate': self.rating_rate,
                'count': self.rating_count
            },
            'uploader': self.uploader.name if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Product {self.name}>"