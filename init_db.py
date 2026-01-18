import os
from app import create_app
from app.database.db import db
from app.models.user import User, Role
from app.models.product import Product, Category
from werkzeug.security import generate_password_hash


def init_database():
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created")

        # ===== ROLES =====
        roles_data = [
            ('admin', 'Quản trị viên hệ thống'),
            ('manager', 'Quản lý cửa hàng'),
            ('staff', 'Nhân viên'),
            ('customer', 'Khách hàng')
        ]

        for name, desc in roles_data:
            if not Role.query.filter_by(name=name).first():
                db.session.add(Role(name=name, description=desc))

        db.session.commit()

        # ===== ADMIN USER =====
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role and not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@coffeeshop.com',
                full_name='Quản trị viên',
                role_id=admin_role.id,
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created")

        # ===== CATEGORIES =====
        categories = [
            ('Cà phê đen', 'Các loại cà phê đen truyền thống'),
            ('Cà phê sữa', 'Cà phê pha với sữa'),
            ('Espresso', 'Espresso và biến thể'),
            ('Cà phê pha máy', 'Pha bằng máy'),
            ('Đồ uống khác', 'Khác')
        ]

        for name, desc in categories:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name, description=desc))

        db.session.commit()

        category_map = {
            c.name: c.id for c in Category.query.all()
        }

        # ===== PRODUCTS =====
        products = [
            ('Cà phê đen đá', 25000, 'Cà phê đen'),
            ('Cà phê sữa đá', 30000, 'Cà phê sữa'),
            ('Espresso', 35000, 'Espresso'),
            ('Latte', 50000, 'Espresso'),
        ]

        for name, price, cat_name in products:
            if not Product.query.filter_by(name=name).first():
                db.session.add(Product(
                    name=name,
                    price=price,
                    stock=100,
                    category_id=category_map[cat_name]
                ))

        db.session.commit()

        print("\n✓ Database initialized successfully")
        print("Login: admin / admin123")


if __name__ == '__main__':
    init_database()
