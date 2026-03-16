from flask import Flask, render_template, send_from_directory
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.database.db import db
from config import config
import os

# Initialize extensions
login_manager = LoginManager()
csrf = CSRFProtect()

def register_cli(app):
    @app.cli.command('init-db')
    @with_appcontext
    def init_db_command():
        """Initialize database with roles and sample data"""
        from app.models.user import User, Role
        from app.models.product import Product, Category

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
                    role_id=admin_role.id
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
            {'name': 'Cà phê hộp', 'description': 'Cà phê đóng gói dạng hộp các hãng'},
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
        category_map = {c.name: c.id for c in Category.query.all()}
        products_data = [
            {
                'name': 'Cà phê đen đá',
                'description': 'Cà phê đen pha đậm đà, thơm ngon',
                'price': 25000,
                'stock': 100,
                'category_name': 'Cà phê đen'
            },
            {
                'name': 'Cà phê đen nóng',
                'description': 'Cà phê đen nóng, thơm lừng',
                'price': 25000,
                'stock': 100,
                'category_name': 'Cà phê đen'
            },
            {
                'name': 'Cà phê sữa đá',
                'description': 'Cà phê sữa đá truyền thống',
                'price': 30000,
                'stock': 100,
                'category_name': 'Cà phê sữa'
            },
            {
                'name': 'Cà phê sữa nóng',
                'description': 'Cà phê sữa nóng thơm ngon',
                'price': 30000,
                'stock': 100,
                'category_name': 'Cà phê sữa'
            },
            {
                'name': 'Espresso',
                'description': 'Espresso đậm đà, nguyên chất',
                'price': 35000,
                'stock': 50,
                'category_name': 'Espresso'
            },
            {
                'name': 'Cappuccino',
                'description': 'Cappuccino với lớp bọt sữa mịn',
                'price': 45000,
                'stock': 50,
                'category_name': 'Espresso'
            },
            {
                'name': 'Latte',
                'description': 'Latte với sữa tươi thơm ngon',
                'price': 50000,
                'stock': 50,
                'category_name': 'Espresso'
            },
            {
                'name': 'Americano',
                'description': 'Americano pha loãng từ espresso',
                'price': 40000,
                'stock': 50,
                'category_name': 'Cà phê pha máy'
            },
            {
                'name': 'Mocha',
                'description': 'Mocha với chocolate và cà phê',
                'price': 55000,
                'stock': 50,
                'category_name': 'Cà phê pha máy'
            },
            {
                'name': 'Macchiato',
                'description': 'Macchiato với lớp sữa đánh',
                'price': 48000,
                'stock': 50,
                'category_name': 'Espresso'
            },
            # Cà phê hộp - các hãng
            {
                'name': 'Trung Nguyên G7 (Hộp 16 gói)',
                'description': 'Cà phê hòa tan Trung Nguyên G7, hộp 16 gói, thơm đậm đà',
                'price': 65000,
                'stock': 80,
                'category_name': 'Cà phê hộp',
                'image_url': 'images/coffee-boxes/coffee-box-trung-nguyen.svg'
            },
            {
                'name': 'Nestlé Nescafé (Hộp 20 gói)',
                'description': 'Cà phê hòa tan Nestlé Nescafé, hộp 20 gói',
                'price': 72000,
                'stock': 60,
                'category_name': 'Cà phê hộp',
                'image_url': 'images/coffee-boxes/coffee-box-nescafe.svg'
            },
            {
                'name': 'Vinacafe (Hộp 20 gói)',
                'description': 'Cà phê hòa tan Vinacafe truyền thống, hộp 20 gói',
                'price': 58000,
                'stock': 70,
                'category_name': 'Cà phê hộp',
                'image_url': 'images/coffee-boxes/coffee-box-vinacafe.svg'
            },
            {
                'name': 'Highlands Coffee (Hộp 12 gói)',
                'description': 'Cà phê sữa đá Highlands hộp 12 gói, tiện lợi',
                'price': 89000,
                'stock': 50,
                'category_name': 'Cà phê hộp',
                'image_url': 'images/coffee-boxes/coffee-box-highlands.svg'
            },
            {
                'name': 'Cà phê Phúc Long (Hộp 15 gói)',
                'description': 'Cà phê hòa tan Phúc Long, hộp 15 gói',
                'price': 75000,
                'stock': 45,
                'category_name': 'Cà phê hộp',
                'image_url': 'images/coffee-boxes/coffee-box-phuclong.svg'
            },
            {
                'name': 'Cà phê Wake Up 339 (Hộp 20 gói)',
                'description': 'Cà phê hòa tan Wake Up 339, hộp 20 gói',
                'price': 55000,
                'stock': 65,
                'category_name': 'Cà phê hộp',
                'image_url': 'images/coffee-boxes/coffee-box-wakeup.svg'
            },
        ]

        for prod_data in products_data:
            product = Product.query.filter_by(name=prod_data['name']).first()
            if not product:
                category_id = category_map.get(prod_data['category_name'])
                if not category_id:
                    print(f"! Skip product '{prod_data['name']}' (missing category)")
                    continue
                product = Product(
                    name=prod_data['name'],
                    description=prod_data['description'],
                    price=prod_data['price'],
                    stock=prod_data['stock'],
                    category_id=category_id,
                    image_url=prod_data.get('image_url')
                )
                db.session.add(product)

        db.session.commit()
        print("✓ Sample products created")
        print("\n✓ Database initialization completed!")
        print("\nDefault login credentials:")
        print("  Username: admin")
        print("  Password: admin123")

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'
    login_manager.login_message_category = 'info'
    # csrf.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(dashboard_bp)
    
    # Register custom filters
    @app.template_filter('format_currency')
    def format_currency(value):
        """Format number with thousand separator (dot) and currency symbol"""
        try:
            return "{:,.0f}đ".format(float(value)).replace(',', '.')
        except (ValueError, TypeError):
            return f"{value}đ"
    
    # Favicon (nhiều trình duyệt tự gọi /favicon.ico)
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.static_folder, 'images'),
            'favicon.svg',
            mimetype='image/svg+xml'
        )
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Register user loader
    @login_manager.user_loader
    def load_user(user_id):
        """Load user for Flask-Login"""
        from app.models.user import User
        return User.query.get(int(user_id))

    register_cli(app)

    return app
