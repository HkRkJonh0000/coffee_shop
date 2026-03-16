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
('Cà phê hộp', 'Cà phê đóng gói dạng hộp các hãng'),
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

-- Insert sample products (name, description, price, stock, category_id, image_url)
INSERT INTO products (name, description, price, stock, category_id, image_url) VALUES
('Cà phê đen đá', 'Pha phin truyền thống, hạt Robusta Đắk Lắk rang vừa. Đắng nhẹ, hậu vị chocolate đen, uống sảng khoái ngày nóng.', 25000, 100, 1, NULL),
('Cà phê đen nóng', 'Phin nóng đậm, dùng cùng loại hạt với bản đá. Hương thơm nồng hơn, phù hợp sáng sớm hoặc chiều mưa.', 25000, 100, 1, NULL),
('Cà phê sữa đá', 'Đen đá + sữa đặc, tỷ lệ 6:4. Ngọt vừa, không gắt, ai cũng uống được. Best seller của quán (nếu có quán thật).', 30000, 100, 2, NULL),
('Cà phê sữa nóng', 'Bản nóng của sữa đá, ngọt ấm. Có người bảo uống buổi tối dễ mất ngủ, nhưng mình thấy ok mà.', 30000, 100, 2, NULL),
('Espresso', '1 shot 30ml, chiết xuất 25-30 giây. Đắng đậm, crema mỏng. Dành cho người uống đen không đường.', 35000, 50, 3, NULL),
('Cappuccino', 'Espresso + sữa nóng + bọt sữa (tỷ lệ 1:1:1). Bọt mịn nếu đánh sữa đúng nhiệt độ 65°C. Ngọt tự nhiên từ sữa.', 45000, 50, 3, NULL),
('Latte', 'Espresso + nhiều sữa hơn Cappuccino, ít bọt. Dịu, uống dễ, phù hợp người mới thử cà phê ý.', 50000, 50, 3, NULL),
('Americano', 'Espresso pha thêm nước nóng (tỷ lệ 1:2). Nhạt hơn đen phin, nhưng giữ được hương cà phê rang sáng.', 40000, 50, 4, NULL),
('Mocha', 'Latte + chocolate đen 70%. Ngọt vừa, đắng nhẹ. Kiểu uống "an toàn" nhất nếu chưa quen cà phê đắng.', 55000, 50, 4, NULL),
('Macchiato', 'Espresso + 1 muỗng sữa bọt. Đắng chủ đạo, sữa chỉ để giảm gắt. Uống nhanh trước khi bọt xẹp.', 48000, 50, 3, NULL),
('Cà phê phin', 'Phin truyền thống kiểu miền Nam, hạt vối rang kỹ. Pha lâu (~5 phút), uống chậm. Hợp với bánh mì buổi sáng.', 35000, 80, 1, NULL),
('Bạc xỉu', 'Ngược với sữa đá: nhiều sữa, ít cà phê (tỷ lệ 7:3). Ngọt, sánh, ít caffeine. Mình hay uống chiều muộn.', 40000, 80, 2, NULL),
('Trung Nguyên G7 (Hộp 16 gói)', 'G7 3in1 hộp 16 gói. Pha nhanh, vị quen thuộc. Mình hay mua về pha sáng khi lười xuống quán. Ngọt có sẵn, không cần đường.', 65000, 80, 5, 'images/coffee-boxes/coffee-box-trung-nguyen.svg'),
('Nestlé Nescafé (Hộp 20 gói)', 'Nescafé 3in1 hộp 20 gói. Vị nhẹ hơn G7, bớt ngọt. Bạn mình bảo vị này giống cà phê văn phòng. Giá rẻ, đủ dùng cả tháng.', 72000, 60, 5, 'images/coffee-boxes/coffee-box-nescafe.svg'),
('Vinacafe (Hộp 20 gói)', 'Vinacafe hòa tan hộp 20 gói. Hương hơi khét (kiểu rang kỹ), đắng rõ. Bố mình hay uống loại này.', 58000, 70, 5, 'images/coffee-boxes/coffee-box-vinacafe.svg'),
('Highlands Coffee (Hộp 12 gói)', 'Highlands sữa đá hòa tan 12 gói. Ngọt nhiều, sánh. Uống lạnh mới ngon, nóng thì hơi ngán. Giá hơi cao so với mấy loại khác.', 89000, 50, 5, 'images/coffee-boxes/coffee-box-highlands.svg'),
('Cà phê Phúc Long (Hộp 15 gói)', 'Phúc Long hòa tan hộp 15 gói. Vị cân bằng giữa G7 và Highlands. Hương thơm ổn, không quá ngọt. Mình hay mua làm quà.', 75000, 45, 5, 'images/coffee-boxes/coffee-box-phuclong.svg'),
('Cà phê Wake Up 339 (Hộp 20 gói)', 'Wake Up 339 hộp 20 gói. Đắng rõ, ngọt ít. Packaging đơn giản. Giá rẻ nhất trong các loại hòa tan, phù hợp sinh viên.', 55000, 65, 5, 'images/coffee-boxes/coffee-box-wakeup.svg')
ON DUPLICATE KEY UPDATE name=name;

-- Note: Password hashes need to be generated using Python:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))
-- Replace the hash_here placeholders with actual hashes
