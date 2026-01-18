from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.database.db import db
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Home page - redirect based on user role"""
    if current_user.is_authenticated:
        if current_user.is_admin() or current_user.is_manager() or current_user.is_staff():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('products.index'))
    return redirect(url_for('products.index'))

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    if current_user.is_admin() or current_user.is_manager() or current_user.is_staff():
        return redirect(url_for('admin.dashboard'))
    
    # Customer dashboard
    recent_orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.created_at.desc())\
        .limit(5)\
        .all()
    
    total_orders = Order.query.filter_by(user_id=current_user.id).count()
    total_spent = db.session.query(func.sum(Order.total_amount))\
        .filter_by(user_id=current_user.id)\
        .scalar() or 0
    
    return render_template('customer/dashboard.html',
                         recent_orders=recent_orders,
                         total_orders=total_orders,
                         total_spent=total_spent)
