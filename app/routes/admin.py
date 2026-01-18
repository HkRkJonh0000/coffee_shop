from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.database.db import db
from app.models.product import Product, Category
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User, Role
from app.utils.decorators import admin_required, manager_required, staff_required
from app.utils.helpers import paginate_query, format_currency
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@staff_required
def dashboard():
    """Admin dashboard with statistics"""
    # Statistics
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Orders by status
    orders_by_status = db.session.query(
        Order.status,
        func.count(Order.id)
    ).group_by(Order.status).all()
    
    # Revenue by day (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    # Use DATE() function for MySQL compatibility
    revenue_by_day = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(Order.created_at >= seven_days_ago)\
     .group_by(func.date(Order.created_at))\
     .order_by(func.date(Order.created_at))\
     .all()
    
    # Low stock products
    low_stock_products = Product.query.filter(Product.stock < 10).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         orders_by_status=orders_by_status,
                         revenue_by_day=revenue_by_day,
                         low_stock_products=low_stock_products)

@admin_bp.route('/products')
@login_required
@staff_required
def products():
    """Product management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    
    query = Product.query
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    query = query.order_by(Product.created_at.desc())
    pagination = paginate_query(query, page)
    
    categories = Category.query.all()
    
    return render_template('admin/products.html',
                         products=pagination.items,
                         pagination=pagination,
                         categories=categories,
                         search=search,
                         category_id=category_id)

@admin_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
@staff_required
def create_product():
    """Create new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        
        if not all([name, price, category_id]):
            flash('Vui lòng điền đầy đủ thông tin bắt buộc.', 'danger')
            return redirect(url_for('admin.create_product'))
        
        try:
            product = Product(
                name=name,
                description=description,
                price=float(price),
                stock=int(stock) if stock else 0,
                category_id=int(category_id)
            )
            db.session.add(product)
            db.session.commit()
            flash('Tạo sản phẩm thành công!', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', categories=categories)

@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_product(id):
    """Edit product"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id'))
        product.is_active = bool(request.form.get('is_active'))
        
        try:
            db.session.commit()
            flash('Cập nhật sản phẩm thành công!', 'success')
            return redirect(url_for('admin.products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', product=product, categories=categories)

@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
@staff_required
def delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Xóa sản phẩm thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return redirect(url_for('admin.products'))

@admin_bp.route('/orders')
@login_required
@staff_required
def orders():
    """Order management page"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(Order.created_at.desc())
    pagination = paginate_query(query, page)
    
    return render_template('admin/orders.html',
                         orders=pagination.items,
                         pagination=pagination,
                         status=status)

@admin_bp.route('/orders/<int:id>')
@login_required
@staff_required
def order_detail(id):
    """Order detail page"""
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/<int:id>/update-status', methods=['POST'])
@login_required
@staff_required
def update_order_status(id):
    """Update order status"""
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if not order.can_update_status(new_status):
        flash('Không thể cập nhật trạng thái đơn hàng.', 'danger')
        return redirect(url_for('admin.order_detail', id=id))
    
    order.status = new_status
    try:
        db.session.commit()
        flash('Cập nhật trạng thái đơn hàng thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return redirect(url_for('admin.order_detail', id=id))

@admin_bp.route('/users')
@login_required
@manager_required
def users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    role_id = request.args.get('role', type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.username.contains(search),
                User.email.contains(search),
                User.full_name.contains(search)
            )
        )
    
    if role_id:
        query = query.filter_by(role_id=role_id)
    
    query = query.order_by(User.created_at.desc())
    pagination = paginate_query(query, page)
    
    roles = Role.query.all()
    
    return render_template('admin/users.html',
                         users=pagination.items,
                         pagination=pagination,
                         roles=roles,
                         role_id=role_id,
                         search=search)

@admin_bp.route('/categories')
@login_required
@staff_required
def categories():
    """Category management"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/create', methods=['POST'])
@login_required
@staff_required
def create_category():
    """Create category"""
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('Vui lòng nhập tên danh mục.', 'danger')
        return redirect(url_for('admin.categories'))
    
    if Category.query.filter_by(name=name).first():
        flash('Danh mục đã tồn tại.', 'danger')
        return redirect(url_for('admin.categories'))
    
    try:
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Tạo danh mục thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return redirect(url_for('admin.categories'))
