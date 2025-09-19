# app/services/product_service.py
from typing import List, Optional
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

class ProductService:
    
    @staticmethod
    def create_product(name: str, price: float, colors: List[str], tags: List[str], 
                      category_name: str, uploader_id: int) -> Product:
        """Create a new product"""
        try:
            # Find category
            category = Category.query.filter_by(name=category_name, is_active=True).first()
            if not category:
                raise ValueError(f"Category '{category_name}' not found")
            
            # Check for duplicate product name (case-insensitive)
            existing_product = Product.query.filter(
                db.func.lower(Product.name) == name.lower(),
                Product.is_active == True
            ).first()
            if existing_product:
                raise ValueError("Product name already exists")
            
            # Create product
            product = Product(
                name=name,
                price=price,
                category_id=category.id,
                uploader_id=uploader_id
            )
            product.colors = colors
            product.tags = tags
            
            db.session.add(product)
            db.session.commit()
            
            return product
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Product creation failed due to database constraint")
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def update_product(product_id: int, name: Optional[str] = None, price: Optional[float] = None,
                      colors: Optional[List[str]] = None, tags: Optional[List[str]] = None,
                      category_name: Optional[str] = None) -> Product:
        """Update an existing product"""
        try:
            product = Product.query.filter_by(id=product_id, is_active=True).first()
            if not product:
                raise ValueError("Product not found")
            
            # Update fields if provided
            if name is not None:
                # Check for duplicate name (excluding current product)
                existing_product = Product.query.filter(
                    db.func.lower(Product.name) == name.lower(),
                    Product.is_active == True,
                    Product.id != product_id
                ).first()
                if existing_product:
                    raise ValueError("Product name already exists")
                product.name = name
            
            if price is not None:
                product.price = price
            
            if colors is not None:
                product.colors = colors
            
            if tags is not None:
                product.tags = tags
            
            if category_name is not None:
                category = Category.query.filter_by(name=category_name, is_active=True).first()
                if not category:
                    raise ValueError(f"Category '{category_name}' not found")
                product.category_id = category.id
            
            db.session.commit()
            return product
            
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def delete_product(product_id: int) -> bool:
        """Soft delete a product"""
        try:
            product = Product.query.filter_by(id=product_id, is_active=True).first()
            if not product:
                raise ValueError("Product not found")
            
            product.is_active = False
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return Product.query.filter_by(id=product_id, is_active=True).first()

    @staticmethod
    def get_all_products() -> List[Product]:
        """Get all active products"""
        return Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()

    @staticmethod
    def get_products_by_category(category_name: str) -> List[Product]:
        """Get products by category name"""
        return Product.query.join(Category).filter(
            Category.name == category_name,
            Product.is_active == True,
            Category.is_active == True
        ).order_by(Product.created_at.desc()).all()

    @staticmethod
    def search_products(query: str) -> List[Product]:
        """Search products by name, tags, or category"""
        return Product.query.join(Category).filter(
            or_(
                Product.name.ilike(f'%{query}%'),
                Product.tags_json.ilike(f'%{query}%'),
                Category.name.ilike(f'%{query}%')
            ),
            Product.is_active == True,
            Category.is_active == True
        ).order_by(Product.created_at.desc()).all()


