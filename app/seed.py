# app/seed.py
from flask.cli import with_appcontext
import click
from app.extensions import db
from app.services.category_service import CategoryService
from app.services.auth_service import AuthService
from app.services.product_service import ProductService

@click.command("init-db")
@with_appcontext
def init_db():
    """Initialize database with tables and seed data."""
    # Create all tables
    db.create_all()
    
    # Seed default data
    seed_default_data()
    
    click.echo("✅ Database initialized successfully")

@click.command("seed-data")
@with_appcontext
def seed_data():
    """Seed default data."""
    seed_default_data()
    click.echo("✅ Default data seeded successfully")

def seed_default_data():
    """Seed default categories, admin user, and sample products."""
    try:
        # Seed categories
        CategoryService.seed_default_categories()
        
        # Create admin user
        admin = AuthService.create_admin_user()
        
        # Seed sample products if admin exists
        if admin:
            seed_sample_products(admin.id)
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding data: {e}")

def seed_sample_products(admin_id):
    """Seed sample products."""
    sample_products = [
        {
            "name": "iPhone 14 Pro Max",
            "price": 129900,
            "colors": ["Black", "Silver", "Gold", "Deep Purple"],
            "tags": ["Apple", "Flagship", "Premium"],
            "category_name": "Mobiles"
        },
        {
            "name": "Samsung Galaxy S23 Ultra",
            "price": 124999,
            "colors": ["Black", "Green", "Lavender", "Cream"],
            "tags": ["Samsung", "Android", "Camera"],
            "category_name": "Mobiles"
        },
        {
            "name": "MacBook Air M2",
            "price": 114900,
            "colors": ["Space Gray", "Silver", "Starlight", "Midnight"],
            "tags": ["Apple", "Laptop", "M2 Chip"],
            "category_name": "Laptops"
        },
        {
            "name": "Sony WH-1000XM5",
            "price": 29990,
            "colors": ["Black", "Silver"],
            "tags": ["Sony", "Headphones", "Noise Cancelling"],
            "category_name": "Accessories"
        }
    ]
    
    for product_data in sample_products:
        try:
            ProductService.create_product(
                name=product_data["name"],
                price=product_data["price"],
                colors=product_data["colors"],
                tags=product_data["tags"],
                category_name=product_data["category_name"],
                uploader_id=admin_id
            )
        except ValueError:
            # Product already exists, skip
            continue