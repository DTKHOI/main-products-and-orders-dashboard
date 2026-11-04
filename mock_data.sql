PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. BẢNG USER (1 Admin id=1 + 20 Staff id=2..21)
-- ==========================================
INSERT OR IGNORE INTO "user" (id, username, email, password_hash, role, phone, avatar_url, language, theme) VALUES
(1, 'TuanKhoi', 'khoiduongtuan25@gmail.com', '@Admin123', 'admin', '0938214007', '', 'en', 'light'),
(2, 'staff_nam01', 'nam.nguyen@store.vn', 'scrypt:32768:8:1$mockhash$staff01', 'staff', '0901000001', '/static/images/avatars/staff1.png', 'vi', 'light'),
(3, 'staff_lan02', 'lan.tran@store.vn', 'scrypt:32768:8:1$mockhash$staff02', 'staff', '0901000002', '/static/images/avatars/staff2.png', 'vi', 'dark'),
(4, 'staff_huy03', 'huy.le@store.vn', 'scrypt:32768:8:1$mockhash$staff03', 'staff', '0901000003', '/static/images/avatars/staff3.png', 'vi', 'light'),
(5, 'staff_mai04', 'mai.pham@store.vn', 'scrypt:32768:8:1$mockhash$staff04', 'staff', '0901000004', '/static/images/avatars/staff4.png', 'en', 'light'),
(6, 'staff_duc05', 'duc.hoang@store.vn', 'scrypt:32768:8:1$mockhash$staff05', 'staff', '0901000005', '/static/images/avatars/staff5.png', 'vi', 'dark'),
(7, 'staff_vy06', 'vy.vu@store.vn', 'scrypt:32768:8:1$mockhash$staff06', 'staff', '0901000006', '/static/images/avatars/staff6.png', 'vi', 'light'),
(8, 'staff_khoa07', 'khoa.dang@store.vn', 'scrypt:32768:8:1$mockhash$staff07', 'staff', '0901000007', '/static/images/avatars/staff7.png', 'en', 'dark'),
(9, 'staff_linh08', 'linh.bui@store.vn', 'scrypt:32768:8:1$mockhash$staff08', 'staff', '0901000008', '/static/images/avatars/staff8.png', 'vi', 'light'),
(10, 'staff_tuan09', 'tuan.do@store.vn', 'scrypt:32768:8:1$mockhash$staff09', 'staff', '0901000009', '/static/images/avatars/staff9.png', 'vi', 'light'),
(11, 'staff_ngoc10', 'ngoc.ho@store.vn', 'scrypt:32768:8:1$mockhash$staff10', 'staff', '0901000010', '/static/images/avatars/staff10.png', 'vi', 'dark'),
(12, 'staff_minh11', 'minh.ngo@store.vn', 'scrypt:32768:8:1$mockhash$staff11', 'staff', '0901000011', '/static/images/avatars/staff11.png', 'en', 'light'),
(13, 'staff_thao12', 'thao.duong@store.vn', 'scrypt:32768:8:1$mockhash$staff12', 'staff', '0901000012', '/static/images/avatars/staff12.png', 'vi', 'light'),
(14, 'staff_son13', 'son.ly@store.vn', 'scrypt:32768:8:1$mockhash$staff13', 'staff', '0901000013', '/static/images/avatars/staff13.png', 'vi', 'dark'),
(15, 'staff_ha14', 'ha.truong@store.vn', 'scrypt:32768:8:1$mockhash$staff14', 'staff', '0901000014', '/static/images/avatars/staff14.png', 'vi', 'light'),
(16, 'staff_phuc15', 'phuc.ha@store.vn', 'scrypt:32768:8:1$mockhash$staff15', 'staff', '0901000015', '/static/images/avatars/staff15.png', 'en', 'light'),
(17, 'staff_trang16', 'trang.dinh@store.vn', 'scrypt:32768:8:1$mockhash$staff16', 'staff', '0901000016', '/static/images/avatars/staff16.png', 'vi', 'dark'),
(18, 'staff_kien17', 'kien.lam@store.vn', 'scrypt:32768:8:1$mockhash$staff17', 'staff', '0901000017', '/static/images/avatars/staff17.png', 'vi', 'light'),
(19, 'staff_yen18', 'yen.mai@store.vn', 'scrypt:32768:8:1$mockhash$staff18', 'staff', '0901000018', '/static/images/avatars/staff18.png', 'vi', 'light'),
(20, 'staff_long19', 'long.trinh@store.vn', 'scrypt:32768:8:1$mockhash$staff19', 'staff', '0901000019', '/static/images/avatars/staff19.png', 'en', 'dark'),
(21, 'staff_chau20', 'chau.luong@store.vn', 'scrypt:32768:8:1$mockhash$staff20', 'staff', '0901000020', '/static/images/avatars/staff20.png', 'vi', 'light');

-- ==========================================
-- 2. BẢNG STAFF (20 nhân viên nam/nữ thuộc Admin id=1)
-- ==========================================
INSERT INTO staff (id, user_id, local_id, admin_id, staff_code, full_name, phone, address, gender, avatar_url) VALUES
(1, 2, 1, 1, 'ST-0001', 'Nguyễn Hoài Nam', '0901000001', '12 Lê Lợi, Quận 1, TP.HCM', 'male', '/static/images/avatars/staff1.png'),
(2, 3, 2, 1, 'ST-0002', 'Trần Ngọc Lan', '0901000002', '45 Nguyễn Huệ, Quận 1, TP.HCM', 'female', '/static/images/avatars/staff2.png'),
(3, 4, 3, 1, 'ST-0003', 'Lê Quốc Huy', '0901000003', '88 Võ Văn Ngân, TP. Thủ Đức, TP.HCM', 'male', '/static/images/avatars/staff3.png'),
(4, 5, 4, 1, 'ST-0004', 'Phạm Thanh Mai', '0901000004', '102 Điện Biên Phủ, Quận Bình Thạnh, TP.HCM', 'female', '/static/images/avatars/staff4.png'),
(5, 6, 5, 1, 'ST-0005', 'Hoàng Minh Đức', '0901000005', '23 Cách Mạng Tháng 8, Quận 3, TP.HCM', 'male', '/static/images/avatars/staff5.png'),
(6, 7, 6, 1, 'ST-0006', 'Vũ Thảo Vy', '0901000006', '56 Nguyễn Thị Minh Khai, Quận 3, TP.HCM', 'female', '/static/images/avatars/staff6.png'),
(7, 8, 7, 1, 'ST-0007', 'Đặng Anh Khoa', '0901000007', '19 Lê Văn Việt, TP. Thủ Đức, TP.HCM', 'male', '/static/images/avatars/staff7.png'),
(8, 9, 8, 1, 'ST-0008', 'Bùi Khánh Linh', '0901000008', '74 Phan Xích Long, Quận Phú Nhuận, TP.HCM', 'female', '/static/images/avatars/staff8.png'),
(9, 10, 9, 1, 'ST-0009', 'Đỗ Anh Tuấn', '0901000009', '310 Cộng Hòa, Quận Tân Bình, TP.HCM', 'male', '/static/images/avatars/staff9.png'),
(10, 11, 10, 1, 'ST-0010', 'Hồ Bảo Ngọc', '0901000010', '65 Quang Trung, Quận Gò Vấp, TP.HCM', 'female', '/static/images/avatars/staff10.png'),
(11, 12, 11, 1, 'ST-0011', 'Ngô Nhật Minh', '0901000011', '140 Lý Thường Kiệt, Quận 10, TP.HCM', 'male', '/static/images/avatars/staff11.png'),
(12, 13, 12, 1, 'ST-0012', 'Dương Phương Thảo', '0901000012', '215 Ba Tháng Hai, Quận 10, TP.HCM', 'female', '/static/images/avatars/staff12.png'),
(13, 14, 13, 1, 'ST-0013', 'Lý Thái Sơn', '0901000013', '92 Nguyễn Trãi, Quận 5, TP.HCM', 'male', '/static/images/avatars/staff13.png'),
(14, 15, 14, 1, 'ST-0014', 'Trương Thu Hà', '0901000014', '18 Trần Hưng Đạo, Quận 5, TP.HCM', 'female', '/static/images/avatars/staff14.png'),
(15, 16, 15, 1, 'ST-0015', 'Hà Gia Phúc', '0901000015', '50 Nguyễn Văn Linh, Quận 7, TP.HCM', 'male', '/static/images/avatars/staff15.png'),
(16, 17, 16, 1, 'ST-0016', 'Đinh Huyền Trang', '0901000016', '128 Nguyễn Thị Thập, Quận 7, TP.HCM', 'female', '/static/images/avatars/staff16.png'),
(17, 18, 17, 1, 'ST-0017', 'Lâm Trung Kiên', '0901000017', '41 Đinh Tiên Hoàng, Quận 1, TP.HCM', 'male', '/static/images/avatars/staff17.png'),
(18, 19, 18, 1, 'ST-0018', 'Mai Hải Yến', '0901000018', '83 Hoàng Văn Thụ, Quận Phú Nhuận, TP.HCM', 'female', '/static/images/avatars/staff18.png'),
(19, 20, 19, 1, 'ST-0019', 'Trịnh Hoàng Long', '0901000019', '175 Xô Viết Nghệ Tĩnh, Quận Bình Thạnh, TP.HCM', 'male', '/static/images/avatars/staff19.png'),
(20, 21, 20, 1, 'ST-0020', 'Lương Minh Châu', '0901000020', '29 Man Thiện, TP. Thủ Đức, TP.HCM', 'female', '/static/images/avatars/staff20.png');

-- ==========================================
-- 3. BẢNG PRODUCT (24 sản phẩm, tồn kho 0..100, 4 danh mục chuẩn)
-- ==========================================
INSERT INTO product (id, admin_id, local_id, sku, name, category, price, stock, image_url, status, created_at) VALUES
(1, 1, 1, 'PRD-0001', 'Tai nghe Bluetooth Sony WH-1000XM5', 'Điện tử', 6500000, 15, '/static/images/products/prd1.jpg', 'active', '2025-02-01 08:30:00'),
(2, 1, 2, 'PRD-0002', 'Chuột không dây Logitech MX Master 3S', 'Điện tử', 2400000, 42, '/static/images/products/prd2.jpg', 'active', '2025-02-01 09:00:00'),
(3, 1, 3, 'PRD-0003', 'Bàn phím cơ Keychron K8 Pro', 'Điện tử', 2600000, 28, '/static/images/products/prd3.jpg', 'active', '2025-02-02 10:15:00'),
(4, 1, 4, 'PRD-0004', 'Sạc dự phòng Anker 20000mAh', 'Điện tử', 950000, 85, '/static/images/products/prd4.jpg', 'active', '2025-02-02 11:00:00'),
(5, 1, 5, 'PRD-0005', 'Loa di động JBL Flip 6', 'Điện tử', 2900000, 0, '/static/images/products/prd5.jpg', 'inactive', '2025-02-03 14:20:00'),
(6, 1, 6, 'PRD-0006', 'Đồng hồ thông minh Apple Watch SE', 'Điện tử', 5800000, 12, '/static/images/products/prd6.jpg', 'active', '2025-02-03 15:45:00'),
(7, 1, 7, 'PRD-0007', 'Áo thun Cotton Compact Unisex', 'Thời trang', 250000, 94, '/static/images/products/prd7.jpg', 'active', '2025-02-04 08:10:00'),
(8, 1, 8, 'PRD-0008', 'Áo sơ mi Oxford dài tay', 'Thời trang', 420000, 63, '/static/images/products/prd8.jpg', 'active', '2025-02-04 09:30:00'),
(9, 1, 9, 'PRD-0009', 'Quần Jeans Slimfit nam', 'Thời trang', 550000, 47, '/static/images/products/prd9.jpg', 'active', '2025-02-05 10:00:00'),
(10, 1, 10, 'PRD-0010', 'Áo khoác Bomber chống nước', 'Thời trang', 680000, 31, '/static/images/products/prd10.jpg', 'active', '2025-02-05 13:20:00'),
(11, 1, 11, 'PRD-0011', 'Chân váy xếp ly dáng dài', 'Thời trang', 350000, 56, '/static/images/products/prd11.jpg', 'active', '2025-02-06 14:50:00'),
(12, 1, 12, 'PRD-0012', 'Áo Hoodie nỉ bông oversize', 'Thời trang', 490000, 72, '/static/images/products/prd12.jpg', 'active', '2025-02-06 16:10:00'),
(13, 1, 13, 'PRD-0013', 'Giày chạy bộ Nike Air Zoom Pegasus', 'Giày dép', 2800000, 19, '/static/images/products/prd13.jpg', 'active', '2025-02-07 08:40:00'),
(14, 1, 14, 'PRD-0014', 'Giày Sneaker Adidas Stan Smith', 'Giày dép', 2100000, 38, '/static/images/products/prd14.jpg', 'active', '2025-02-07 10:25:00'),
(15, 1, 15, 'PRD-0015', 'Giày lười da nam công sở', 'Giày dép', 1200000, 25, '/static/images/products/prd15.jpg', 'active', '2025-02-08 11:30:00'),
(16, 1, 16, 'PRD-0016', 'Dép Sandal quai ngang unisex', 'Giày dép', 320000, 88, '/static/images/products/prd16.jpg', 'active', '2025-02-08 15:00:00'),
(17, 1, 17, 'PRD-0017', 'Giày cao gót mũi nhọn 7cm', 'Giày dép', 750000, 44, '/static/images/products/prd17.jpg', 'active', '2025-02-09 09:15:00'),
(18, 1, 18, 'PRD-0018', 'Giày cổ cao Converse Chuck 70', 'Giày dép', 1900000, 5, '/static/images/products/prd18.jpg', 'active', '2025-02-09 14:00:00'),
(19, 1, 19, 'PRD-0019', 'Thắt lưng da bò khóa tự động', 'Phụ kiện', 450000, 67, '/static/images/products/prd19.jpg', 'active', '2025-02-10 08:20:00'),
(20, 1, 20, 'PRD-0020', 'Ví da mini cầm tay nhiều ngăn', 'Phụ kiện', 380000, 100, '/static/images/products/prd20.jpg', 'active', '2025-02-10 10:45:00'),
(21, 1, 21, 'PRD-0021', 'Kính mát phân cực chống tia UV', 'Phụ kiện', 520000, 53, '/static/images/products/prd21.jpg', 'active', '2025-02-11 13:10:00'),
(22, 1, 22, 'PRD-0022', 'Balo đựng laptop chống sốc 15.6 inch', 'Phụ kiện', 850000, 34, '/static/images/products/prd22.jpg', 'active', '2025-02-11 15:30:00'),
(23, 1, 23, 'PRD-0023', 'Mũ lưỡi trai thêu chữ tối giản', 'Phụ kiện', 180000, 91, '/static/images/products/prd23.jpg', 'active', '2025-02-12 09:00:00'),
(24, 1, 24, 'PRD-0024', 'Tất cổ cao kháng khuẩn (Set 5 đôi)', 'Phụ kiện', 120000, 76, '/static/images/products/prd24.jpg', 'active', '2025-02-12 11:20:00');

-- ==========================================
-- 4. BẢNG ORDER (20 đơn hàng thuộc Admin id=1)
-- ==========================================
INSERT INTO "order" (id, local_id, ord, admin_id, customer_name, customer_phone, customer_email, customer_id, shipping_address, total_amount, status, created_at) VALUES
(1, 1, 'ORD-0001', 1, 'Phạm Văn Hùng', '0912000001', 'hung.pham@gmail.com', 'KH-0001', '15 Lê Thánh Tôn, Quận 1, TP.HCM', 8400000, 'completed', '2025-02-15 09:10:00'),
(2, 2, 'ORD-0002', 1, 'Nguyễn Thị Bích', '0912000002', 'bich.nguyen@gmail.com', 'KH-0002', '28 Nguyễn Đình Chiểu, Quận 3, TP.HCM', 1540000, 'completed', '2025-02-15 11:25:00'),
(3, 3, 'ORD-0003', 1, 'Trần Minh Quân', '0912000003', 'quan.tran@gmail.com', 'KH-0003', '104 Võ Văn Tần, Quận 3, TP.HCM', 3160000, 'completed', '2025-02-16 08:45:00'),
(4, 4, 'ORD-0004', 1, 'Lê Thu Thủy', '0912000004', 'thuy.le@gmail.com', 'KH-0004', '52 Đỗ Xuân Hợp, TP. Thủ Đức, TP.HCM', 5850000, 'processing', '2025-02-16 14:30:00'),
(5, 5, 'ORD-0005', 1, 'Hoàng Gia Bảo', '0912000005', 'bao.hoang@gmail.com', 'KH-0005', '77 Phan Đăng Lưu, Quận Phú Nhuận, TP.HCM', 1290000, 'completed', '2025-02-17 10:05:00'),
(6, 6, 'ORD-0006', 1, 'Vũ Ngọc Anh', '0912000006', 'anh.vu@gmail.com', 'KH-0006', '190 Hoàng Diệu, Quận 4, TP.HCM', 1830000, 'pending', '2025-02-17 16:40:00'),
(7, 7, 'ORD-0007', 1, 'Đặng Quốc Khánh', '0912000007', 'khanh.dang@gmail.com', 'KH-0007', '33 Nguyễn Oanh, Quận Gò Vấp, TP.HCM', 6840000, 'completed', '2025-02-18 09:50:00'),
(8, 8, 'ORD-0008', 1, 'Bùi Thanh Trúc', '0912000008', 'truc.bui@gmail.com', 'KH-0008', '120 Âu Cơ, Quận Tân Bình, TP.HCM', 1660000, 'canceled', '2025-02-18 13:15:00'),
(9, 9, 'ORD-0009', 1, 'Đỗ Đức Thắng', '0912000009', 'thang.do@gmail.com', 'KH-0009', '64 Lê Văn Sỹ, Quận 3, TP.HCM', 2460000, 'completed', '2025-02-19 10:30:00'),
(10, 10, 'ORD-0010', 1, 'Hồ Kim Ngân', '0912000010', 'ngan.ho@gmail.com', 'KH-0010', '210 Tô Hiến Thành, Quận 10, TP.HCM', 2490000, 'processing', '2025-02-19 15:20:00'),
(11, 11, 'ORD-0011', 1, 'Ngô Tuấn Kiệt', '0912000011', 'kiet.ngo@gmail.com', 'KH-0011', '45 Kinh Dương Vương, Quận 6, TP.HCM', 1960000, 'completed', '2025-02-20 08:55:00'),
(12, 12, 'ORD-0012', 1, 'Dương Mỹ Linh', '0912000012', 'linh.duong@gmail.com', 'KH-0012', '89 Lạc Long Quân, Quận 11, TP.HCM', 3000000, 'pending', '2025-02-20 14:10:00'),
(13, 13, 'ORD-0013', 1, 'Lý Văn Tài', '0912000013', 'tai.ly@gmail.com', 'KH-0013', '16 Nguyễn Ảnh Thủ, Quận 12, TP.HCM', 3850000, 'canceled', '2025-02-21 09:30:00'),
(14, 14, 'ORD-0014', 1, 'Trương Tuyết Nhung', '0912000014', 'nhung.truong@gmail.com', 'KH-0014', '302 Điện Biên Phủ, Quận Bình Thạnh, TP.HCM', 2240000, 'completed', '2025-02-21 16:05:00'),
(15, 15, 'ORD-0015', 1, 'Hà Minh Triết', '0912000015', 'triet.ha@gmail.com', 'KH-0015', '58 Huỳnh Tấn Phát, Quận 7, TP.HCM', 8900000, 'completed', '2025-02-22 10:40:00'),
(16, 16, 'ORD-0016', 1, 'Đinh Ngọc Diệp', '0912000016', 'diep.dinh@gmail.com', 'KH-0016', '112 Lũy Bán Bích, Quận Tân Phú, TP.HCM', 1600000, 'processing', '2025-02-22 13:50:00'),
(17, 17, 'ORD-0017', 1, 'Lâm Chí Vỹ', '0912000017', 'vy.lam@gmail.com', 'KH-0017', '75 Kha Vạn Cân, TP. Thủ Đức, TP.HCM', 6120000, 'completed', '2025-02-23 09:15:00'),
(18, 18, 'ORD-0018', 1, 'Mai Phương Thúy', '0912000018', 'thuy.mai@gmail.com', 'KH-0018', '144 Nam Kỳ Khởi Nghĩa, Quận 1, TP.HCM', 3100000, 'pending', '2025-02-23 15:45:00'),
(19, 19, 'ORD-0019', 1, 'Trịnh Quốc Bảo', '0912000019', 'bao.trinh@gmail.com', 'KH-0019', '29 Hoàng Hoa Thám, Quận Tân Bình, TP.HCM', 2100000, 'completed', '2025-02-24 11:00:00'),
(20, 20, 'ORD-0020', 1, 'Lương Thanh Hằng', '0912000020', 'hang.luong@gmail.com', 'KH-0020', '95 Nguyễn Văn Cừ, Quận 5, TP.HCM', 8800000, 'processing', '2025-02-24 17:30:00');

-- ==========================================
-- 5. BẢNG ORDER_ITEMS (46 bản ghi)
-- ==========================================
INSERT INTO order_items (id, order_id, product_id, product_name, product_sku, quantity, unit_price, total_price) VALUES
-- Đơn 1
(1, 1, 1, 'Tai nghe Bluetooth Sony WH-1000XM5', 'PRD-0001', 1, 6500000, 6500000),
(2, 1, 4, 'Sạc dự phòng Anker 20000mAh', 'PRD-0004', 2, 950000, 1900000),
-- Đơn 2
(3, 2, 7, 'Áo thun Cotton Compact Unisex', 'PRD-0007', 3, 250000, 750000),
(4, 2, 9, 'Quần Jeans Slimfit nam', 'PRD-0009', 1, 550000, 550000),
(5, 2, 24, 'Tất cổ cao kháng khuẩn (Set 5 đôi)', 'PRD-0024', 2, 120000, 240000),
-- Đơn 3
(6, 3, 13, 'Giày chạy bộ Nike Air Zoom Pegasus', 'PRD-0013', 1, 2800000, 2800000),
(7, 3, 24, 'Tất cổ cao kháng khuẩn (Set 5 đôi)', 'PRD-0024', 3, 120000, 360000),
-- Đơn 4
(8, 4, 2, 'Chuột không dây Logitech MX Master 3S', 'PRD-0002', 1, 2400000, 2400000),
(9, 4, 3, 'Bàn phím cơ Keychron K8 Pro', 'PRD-0003', 1, 2600000, 2600000),
(10, 4, 22, 'Balo đựng laptop chống sốc 15.6 inch', 'PRD-0022', 1, 850000, 850000),
-- Đơn 5
(11, 5, 8, 'Áo sơ mi Oxford dài tay', 'PRD-0008', 2, 420000, 840000),
(12, 5, 19, 'Thắt lưng da bò khóa tự động', 'PRD-0019', 1, 450000, 450000),
-- Đơn 6
(13, 6, 11, 'Chân váy xếp ly dáng dài', 'PRD-0011', 2, 350000, 700000),
(14, 6, 17, 'Giày cao gót mũi nhọn 7cm', 'PRD-0017', 1, 750000, 750000),
(15, 6, 20, 'Ví da mini cầm tay nhiều ngăn', 'PRD-0020', 1, 380000, 380000),
-- Đơn 7
(16, 7, 6, 'Đồng hồ thông minh Apple Watch SE', 'PRD-0006', 1, 5800000, 5800000),
(17, 7, 21, 'Kính mát phân cực chống tia UV', 'PRD-0021', 2, 520000, 1040000),
-- Đơn 8
(18, 8, 10, 'Áo khoác Bomber chống nước', 'PRD-0010', 1, 680000, 680000),
(19, 8, 12, 'Áo Hoodie nỉ bông oversize', 'PRD-0012', 2, 490000, 980000),
-- Đơn 9
(20, 9, 14, 'Giày Sneaker Adidas Stan Smith', 'PRD-0014', 1, 2100000, 2100000),
(21, 9, 23, 'Mũ lưỡi trai thêu chữ tối giản', 'PRD-0023', 2, 180000, 360000),
-- Đơn 10
(22, 10, 15, 'Giày lười da nam công sở', 'PRD-0015', 1, 1200000, 1200000),
(23, 10, 8, 'Áo sơ mi Oxford dài tay', 'PRD-0008', 2, 420000, 840000),
(24, 10, 19, 'Thắt lưng da bò khóa tự động', 'PRD-0019', 1, 450000, 450000),
-- Đơn 11
(25, 11, 16, 'Dép Sandal quai ngang unisex', 'PRD-0016', 3, 320000, 960000),
(26, 11, 7, 'Áo thun Cotton Compact Unisex', 'PRD-0007', 4, 250000, 1000000),
-- Đơn 12
(27, 12, 18, 'Giày cổ cao Converse Chuck 70', 'PRD-0018', 1, 1900000, 1900000),
(28, 12, 9, 'Quần Jeans Slimfit nam', 'PRD-0009', 2, 550000, 1100000),
-- Đơn 13
(29, 13, 5, 'Loa di động JBL Flip 6', 'PRD-0005', 1, 2900000, 2900000),
(30, 13, 4, 'Sạc dự phòng Anker 20000mAh', 'PRD-0004', 1, 950000, 950000),
-- Đơn 14
(31, 14, 22, 'Balo đựng laptop chống sốc 15.6 inch', 'PRD-0022', 2, 850000, 1700000),
(32, 14, 23, 'Mũ lưỡi trai thêu chữ tối giản', 'PRD-0023', 3, 180000, 540000),
-- Đơn 15
(33, 15, 1, 'Tai nghe Bluetooth Sony WH-1000XM5', 'PRD-0001', 1, 6500000, 6500000),
(34, 15, 2, 'Chuột không dây Logitech MX Master 3S', 'PRD-0002', 1, 2400000, 2400000),
-- Đơn 16
(35, 16, 11, 'Chân váy xếp ly dáng dài', 'PRD-0011', 1, 350000, 350000),
(36, 16, 12, 'Áo Hoodie nỉ bông oversize', 'PRD-0012', 1, 490000, 490000),
(37, 16, 20, 'Ví da mini cầm tay nhiều ngăn', 'PRD-0020', 2, 380000, 760000),
-- Đơn 17
(38, 17, 13, 'Giày chạy bộ Nike Air Zoom Pegasus', 'PRD-0013', 2, 2800000, 5600000),
(39, 17, 21, 'Kính mát phân cực chống tia UV', 'PRD-0021', 1, 520000, 520000),
-- Đơn 18
(40, 18, 3, 'Bàn phím cơ Keychron K8 Pro', 'PRD-0003', 1, 2600000, 2600000),
(41, 18, 7, 'Áo thun Cotton Compact Unisex', 'PRD-0007', 2, 250000, 500000),
-- Đơn 19
(42, 19, 17, 'Giày cao gót mũi nhọn 7cm', 'PRD-0017', 2, 750000, 1500000),
(43, 19, 24, 'Tất cổ cao kháng khuẩn (Set 5 đôi)', 'PRD-0024', 5, 120000, 600000),
-- Đơn 20
(44, 20, 6, 'Đồng hồ thông minh Apple Watch SE', 'PRD-0006', 1, 5800000, 5800000),
(45, 20, 14, 'Giày Sneaker Adidas Stan Smith', 'PRD-0014', 1, 2100000, 2100000),
(46, 20, 19, 'Thắt lưng da bò khóa tự động', 'PRD-0019', 2, 450000, 900000);