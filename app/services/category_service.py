# app/services/category_service.py
from typing import List, Optional
from app.extensions import db
from app.models.category import Category
from sqlalchemy.exc import IntegrityError

class CategoryService:
    
    @staticmethod
    def create_category(name: str) -> Category:
        """Create a new category"""
        try:
            # Check for duplicate category name (case-insensitive)
            existing_category = Category.query.filter(
                db.func.lower(Category.name) == name.lower(),
                Category.is_active == True
            ).first()
            if existing_category:
                raise ValueError("Category name already exists")
            
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            
            return category
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Category creation failed due to database constraint")
        except Exception as e:
            db.session.rollback()
            raise

    # @staticmethod
    # def update_category(category_id: int, name: str) -> Category:
    #     """Update an existing category"""
    #     try:
    #         category = Category.query.filter_by(id=category_id, is_active=True).first()
    #         if not category:
    #             raise ValueError("Category not found")
            
    #         # Check for duplicate name (excluding current category)
    #         existing_category = Category.query.filter(
    #             db.func.lower(Category.name) == name.lower(),
    #             Category.is_active == True,
    #             Category.id != category_id
    #         ).first()
    #         if existing_category:
    #             raise ValueError("Category name already exists")
            
    #         category.name = name
    #         db.session.commit()
            
    #         return category
            
    #     except Exception as e:
    #         db.session.rollback()
    #         raise

    @staticmethod
    def delete_category(category_id: int) -> bool:
        """Soft delete a category and its products"""
        try:
            category = Category.query.filter_by(id=category_id, is_active=True).first()
            if not category:
                raise ValueError("Category not found")
            
            # Soft delete category and its products
            category.is_active = False
            for product in category.products:
                product.is_active = False
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def get_category_by_id(category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return Category.query.filter_by(id=category_id, is_active=True).first()

    @staticmethod
    def get_category_by_name(name: str) -> Optional[Category]:
        """Get category by name"""
        return Category.query.filter_by(name=name, is_active=True).first()

    @staticmethod
    def get_all_categories() -> List[Category]:
        """Get all active categories"""
        return Category.query.filter_by(is_active=True).order_by(Category.name).all()

    @staticmethod
    def seed_default_categories():
        """Seed default categories"""
        default_categories = ["Mobiles", "Laptops", "Accessories"]
        
        for category_name in default_categories:
            existing = Category.query.filter_by(name=category_name).first()
            if not existing:
                category = Category(name=category_name)
                db.session.add(category)
        
        try:
            db.session.commit()
            print("✅ Default categories seeded")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding categories: {e}")