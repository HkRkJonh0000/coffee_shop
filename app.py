"""
Coffee Shop Management System
Main application entry point
"""
import os
from app import create_app
from app.database.db import db
from app.models.user import User, Role
from app.models.product import Product, Category
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect

app = create_app(os.getenv('FLASK_ENV', 'development'))

# csrf = CSRFProtect()
@app.cli.command('init-db')
def init_db():
    """Initialize database with roles and sample data"""
    db.create_all()
    
    # Create roles
    roles_data = [
        {'name': 'admin', 'description': 'Quản trị viên hệ thống'},
        {'name': 'manager', 'description': 'Quản lý cửa hàng'},
        {'name': 'staff', 'description': 'Nhân viên'},
        {'name': 'customer', 'description': 'Khách hàng'}
    ]
    
    for role_data in roles_data:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Role(**role_data)
            db.session.add(role)
    
    db.session.commit()
    print("✓ Roles created")
    
    # Create admin user
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@coffeeshop.com',
                full_name='Quản trị viên',
                role_id= admin_role.id
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (username: admin, password: admin123)")
    
    # Create sample categories
    categories_data = [
        {'name': 'Cà phê đen', 'description': 'Các loại cà phê đen truyền thống'},
        {'name': 'Cà phê sữa', 'description': 'Cà phê pha với sữa'},
        {'name': 'Espresso', 'description': 'Cà phê espresso và các biến thể'},
        {'name': 'Cà phê pha máy', 'description': 'Cà phê pha bằng máy pha chế'},
        {'name': 'Đồ uống khác', 'description': 'Các loại đồ uống khác'}
    ]
    
    for cat_data in categories_data:
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print("✓ Categories created")
    
    # Create sample products
    products_data = [
        {'name': 'Cà phê đen đá', 'description': 'Cà phê đen pha đậm đà, thơm ngon', 'price': 25000, 'stock': 100, 'category_id': 1},
        {'name': 'Cà phê đen nóng', 'description': 'Cà phê đen nóng, thơm lừng', 'price': 25000, 'stock': 100, 'category_id': 1},
        {'name': 'Cà phê sữa đá', 'description': 'Cà phê sữa đá truyền thống', 'price': 30000, 'stock': 100, 'category_id': 2},
        {'name': 'Cà phê sữa nóng', 'description': 'Cà phê sữa nóng thơm ngon', 'price': 30000, 'stock': 100, 'category_id': 2},
        {'name': 'Espresso', 'description': 'Espresso đậm đà, nguyên chất', 'price': 35000, 'stock': 50, 'category_id': 3},
        {'name': 'Cappuccino', 'description': 'Cappuccino với lớp bọt sữa mịn', 'price': 45000, 'stock': 50, 'category_id': 3},
        {'name': 'Latte', 'description': 'Latte với sữa tươi thơm ngon', 'price': 50000, 'stock': 50, 'category_id': 3},
        {'name': 'Americano', 'description': 'Americano pha loãng từ espresso', 'price': 40000, 'stock': 50, 'category_id': 4},
        {'name': 'Mocha', 'description': 'Mocha với chocolate và cà phê', 'price': 55000, 'stock': 50, 'category_id': 4},
        {'name': 'Macchiato', 'description': 'Macchiato với lớp sữa đánh', 'price': 48000, 'stock': 50, 'category_id': 3},
    ]
    
    for prod_data in products_data:
        product = Product.query.filter_by(name=prod_data['name']).first()
        if not product:
            product = Product(**prod_data)
            db.session.add(product)
    
    db.session.commit()
    print("✓ Sample products created")
    print("\n✓ Database initialization completed!")
    print("\nDefault login credentials:")
    print("  Username: admin")
    print("  Password: admin123")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
