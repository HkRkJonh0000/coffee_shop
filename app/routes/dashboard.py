from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.database.db import db
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

def get_blog_posts():
    """Static blog posts for landing page"""
    return [
        {
            'slug': 'bi-quyet-chon-hat-ca-phe-ngon-cho-nguoi-moi',
            'title': 'Bí quyết chọn hạt cà phê ngon cho người mới',
            'excerpt': 'Chọn đúng hạt là bước đầu để có ly cà phê chất lượng. Dưới đây là những tiêu chí dễ áp dụng...',
            'category': 'Hạt cà phê',
            'read_time': '5 phút đọc',
            'date': 'Thứ 2, 10/02/2026',
            'icon': 'bi-bag-heart',
            'content': [
                'Khi mới bắt đầu, hãy ưu tiên hạt có hương thơm rõ ràng, độ rang vừa và nguồn gốc minh bạch.',
                'Nếu bạn thích vị cân bằng, hãy chọn blend có tỷ lệ Arabica cao; nếu cần vị đậm, Robusta sẽ phù hợp hơn.',
                'Bảo quản hạt trong hũ kín, tránh ánh sáng và ẩm để giữ hương thơm lâu nhất.'
            ]
        },
        {
            'slug': 'can-bang-vi-dang-chua-ngot-trong-pha-che',
            'title': 'Cân bằng vị đắng - chua - ngọt trong pha chế',
            'excerpt': 'Hương vị hài hòa đến từ tỷ lệ chiết xuất đúng. Hãy thử 3 bước đơn giản sau để cải thiện...',
            'category': 'Pha chế',
            'read_time': '7 phút đọc',
            'date': 'Thứ 4, 12/02/2026',
            'icon': 'bi-cup-hot',
            'content': [
                'Vị chua thường đến từ chiết xuất thiếu, vị đắng đến từ chiết xuất quá mức.',
                'Điều chỉnh độ xay và thời gian chiết xuất để đạt cân bằng mong muốn.',
                'Luôn nếm thử và ghi chú để cải thiện dần theo khẩu vị của bạn.'
            ]
        },
        {
            'slug': 'cold-brew-cach-u-lanh-giu-tron-huong-thom',
            'title': 'Cold Brew: cách ủ lạnh giữ trọn hương thơm',
            'excerpt': 'Cold Brew tạo vị dịu, ít chua và dễ uống. Cùng khám phá cách ủ chuẩn trong 12-18 giờ...',
            'category': 'Hướng dẫn',
            'read_time': '6 phút đọc',
            'date': 'Thứ 6, 14/02/2026',
            'icon': 'bi-snow',
            'content': [
                'Dùng bột cà phê xay thô, tỷ lệ 1:8 đến 1:10 với nước lạnh.',
                'Ủ trong tủ lạnh từ 12-18 giờ, sau đó lọc kỹ bằng giấy lọc.',
                'Cold Brew ngon nhất khi dùng trong 3 ngày và bảo quản lạnh.'
            ]
        },
        {
            'slug': 'thoi-quen-uong-ca-phe-tot-cho-suc-khoe',
            'title': 'Thói quen uống cà phê tốt cho sức khỏe',
            'excerpt': 'Uống đúng thời điểm và liều lượng giúp tỉnh táo mà không ảnh hưởng giấc ngủ...',
            'category': 'Sức khỏe',
            'read_time': '4 phút đọc',
            'date': 'Chủ nhật, 16/02/2026',
            'icon': 'bi-heart-pulse',
            'content': [
                'Uống cà phê sau khi thức dậy 1-2 giờ để tối ưu hóa hiệu quả tỉnh táo.',
                'Giữ lượng tiêu thụ vừa phải (1-2 ly/ngày) để tránh mất ngủ.',
                'Kết hợp uống nước để cân bằng cơ thể và tránh mất nước.'
            ]
        },
        {
            'slug': 'cau-chuyen-tu-hat-den-ly-tai-coffee-shop',
            'title': 'Câu chuyện từ hạt đến ly tại Brewly',
            'excerpt': 'Chúng tôi lựa chọn hạt từ vùng cao, rang theo mẻ nhỏ để giữ trọn hương vị...',
            'category': 'Câu chuyện',
            'read_time': '8 phút đọc',
            'date': 'Thứ 3, 18/02/2026',
            'icon': 'bi-journal-text',
            'content': [
                'Chúng tôi làm việc với các nông hộ để tuyển chọn hạt chất lượng cao.',
                'Quy trình rang mẻ nhỏ giúp kiểm soát chất lượng và giữ hương tốt nhất.',
                'Mỗi ly cà phê là kết quả của sự tận tâm trong từng bước.'
            ]
        },
        {
            'slug': '5-mon-uong-duoc-yeu-thich-nhat-thang-nay',
            'title': '5 món uống được yêu thích nhất tháng này',
            'excerpt': 'Danh sách những sản phẩm được khách hàng đánh giá cao về hương vị và độ cân bằng...',
            'category': 'Sản phẩm',
            'read_time': '3 phút đọc',
            'date': 'Thứ 5, 20/02/2026',
            'icon': 'bi-star',
            'content': [
                'Top lựa chọn tháng này gồm: Cà phê sữa đá, Americano, Latte, Cappuccino và Cold Brew.',
                'Mỗi món đều có điểm mạnh riêng về hương vị và mức độ dễ uống.',
                'Bạn có thể thử theo sở thích: đậm, cân bằng hoặc thơm ngậy.'
            ]
        }
    ]

@dashboard_bp.route('/')
def index():
    """Home page - blog style landing"""
    posts = get_blog_posts()

    latest_products = Product.query.filter_by(is_active=True)\
        .order_by(Product.created_at.desc())\
        .limit(6)\
        .all()

    show_admin_link = current_user.is_authenticated and (
        current_user.is_admin() or current_user.is_manager() or current_user.is_staff()
    )

    return render_template(
        'home.html',
        posts=posts,
        latest_products=latest_products,
        show_admin_link=show_admin_link
    )

@dashboard_bp.route('/blog/<slug>')
def blog_detail(slug):
    """Blog detail page"""
    posts = get_blog_posts()
    post = next((item for item in posts if item['slug'] == slug), None)
    if not post:
        abort(404)

    related_posts = [item for item in posts if item['slug'] != slug][:3]
    return render_template('blog_detail.html', post=post, related_posts=related_posts)

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

@dashboard_bp.route('/about')
def about():
    """About us page"""
    return render_template('about.html')
