-- Seed data for Coffee Shop Database
-- Sample data for demo and testing

USE coffee_shop;

-- Insert roles
INSERT INTO roles (name, description) VALUES
('admin', 'Quản trị viên hệ thống'),
('manager', 'Quản lý cửa hàng'),
('staff', 'Nhân viên'),
('customer', 'Khách hàng')
ON DUPLICATE KEY UPDATE name=name;

-- Insert categories
INSERT INTO categories (name, description) VALUES
('Cà phê đen', 'Các loại cà phê đen truyền thống'),
('Cà phê sữa', 'Cà phê pha với sữa'),
('Espresso', 'Cà phê espresso và các biến thể'),
('Cà phê pha máy', 'Cà phê pha bằng máy pha chế'),
('Đồ uống khác', 'Các loại đồ uống khác')
ON DUPLICATE KEY UPDATE name=name;

-- Insert admin user (password: admin123)
-- Password hash for 'admin123' using werkzeug.security.generate_password_hash
INSERT INTO users (username, email, password_hash, full_name, role_id) VALUES
('admin', 'admin@coffeeshop.com', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'Quản trị viên', 1),
('manager', 'manager@coffeeshop.com', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'Quản lý cửa hàng', 2),
('staff', 'staff@coffeeshop.com', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'Nhân viên', 3),
('customer1', 'customer1@example.com', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'Khách hàng 1', 4)
ON DUPLICATE KEY UPDATE username=username;

-- Insert sample products
INSERT INTO products (name, description, price, stock, category_id) VALUES
('Cà phê đen đá', 'Cà phê đen pha đậm đà, thơm ngon', 25000, 100, 1),
('Cà phê đen nóng', 'Cà phê đen nóng, thơm lừng', 25000, 100, 1),
('Cà phê sữa đá', 'Cà phê sữa đá truyền thống', 30000, 100, 2),
('Cà phê sữa nóng', 'Cà phê sữa nóng thơm ngon', 30000, 100, 2),
('Espresso', 'Espresso đậm đà, nguyên chất', 35000, 50, 3),
('Cappuccino', 'Cappuccino với lớp bọt sữa mịn', 45000, 50, 3),
('Latte', 'Latte với sữa tươi thơm ngon', 50000, 50, 3),
('Americano', 'Americano pha loãng từ espresso', 40000, 50, 4),
('Mocha', 'Mocha với chocolate và cà phê', 55000, 50, 4),
('Macchiato', 'Macchiato với lớp sữa đánh', 48000, 50, 3),
('Cà phê phin', 'Cà phê phin truyền thống Việt Nam', 35000, 80, 1),
('Bạc xỉu', 'Bạc xỉu với sữa đặc và cà phê', 40000, 80, 2)
ON DUPLICATE KEY UPDATE name=name;

-- Note: Password hashes need to be generated using Python:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))
-- Replace the hash_here placeholders with actual hashes
