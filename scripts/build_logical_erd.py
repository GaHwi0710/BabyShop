import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/BabyShop")
DB_DIR = ROOT / "database"

# 25 Bảng chuẩn với cấu trúc và kiểu dữ liệu chính xác từ schema.sql & hình ảnh
TABLES = {
    # --- PHÂN HỆ 1: MASTER DATA (Hàng 1) ---
    "VaiTro": {
        "cat": "master", "x": 90, "y": 100, "w": 210,
        "fields": [
            ("MaVT", "INTEGER", True, False),
            ("TenVT", "VARCHAR", False, False)
        ]
    },
    "NhanVien": {
        "cat": "master", "x": 350, "y": 100, "w": 250,
        "fields": [
            ("MaNV", "INTEGER", True, False),
            ("MaVT", "INTEGER", False, True),
            ("HoTen", "VARCHAR(100)", False, False),
            ("ChucVu", "VARCHAR(50)", False, False),
            ("SDT", "VARCHAR(15)", False, False),
            ("TrangThai", "VARCHAR(20)", False, False)
        ]
    },
    "LoaiHang": {
        "cat": "master", "x": 650, "y": 100, "w": 230,
        "fields": [
            ("MaLoai", "INTEGER", True, False),
            ("TenLoai", "VARCHAR(100)", False, False),
            ("MoTa", "TEXT", False, False)
        ]
    },
    "SanPham": {
        "cat": "master", "x": 930, "y": 100, "w": 260,
        "fields": [
            ("MaSP", "INTEGER", True, False),
            ("MaLoai", "INTEGER", False, True),
            ("TenSP", "VARCHAR(100)", False, False),
            ("DonViTinh", "VARCHAR(50)", False, False),
            ("GiaNhap", "DECIMAL(10,2)", False, False),
            ("GiaBan", "DECIMAL(10,2)", False, False),
            ("HanSuDung", "DATE", False, False),
            ("TrangThai", "VARCHAR(20)", False, False)
        ]
    },
    "TonKho": {
        "cat": "master", "x": 1240, "y": 100, "w": 220,
        "fields": [
            ("MaSP", "INTEGER", True, True),
            ("SoLuongTon", "INTEGER", False, False),
            ("NgayCapNhat", "DATE", False, False)
        ]
    },
    "NhaCungCap": {
        "cat": "master", "x": 1510, "y": 100, "w": 240,
        "fields": [
            ("MaNCC", "INTEGER", True, False),
            ("TenNCC", "VARCHAR(100)", False, False),
            ("SDT", "VARCHAR(15)", False, False),
            ("DiaChi", "VARCHAR(200)", False, False),
            ("Email", "VARCHAR(100)", False, False)
        ]
    },
    "KhachHang": {
        "cat": "master", "x": 1800, "y": 100, "w": 240,
        "fields": [
            ("MaKH", "INTEGER", True, False),
            ("HoTen", "VARCHAR(100)", False, False),
            ("SDT", "VARCHAR(15)", False, False),
            ("Email", "VARCHAR(100)", False, False),
            ("DiaChi", "VARCHAR(200)", False, False),
            ("DiemTichLuy", "INTEGER", False, False)
        ]
    },

    # --- PHÂN HỆ 2: MUA HÀNG & NHẬP KHO (Cột 1) ---
    "DonDat_Hang": {
        "cat": "purchase", "x": 90, "y": 420, "w": 250,
        "fields": [
            ("MaDDH", "INTEGER", True, False),
            ("MaNCC", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayDat", "DATE", False, False),
            ("TrangThai", "VARCHAR(20)", False, False),
            ("TongTien", "DECIMAL(10,2)", False, False)
        ]
    },
    "CT_DonDathang": {
        "cat": "purchase", "x": 90, "y": 640, "w": 250,
        "fields": [
            ("MaDDH", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuong", "INTEGER", False, False),
            ("DonGia", "DECIMAL(10,2)", False, False),
            ("ThanhTien", "DECIMAL(10,2)", False, False)
        ]
    },
    "PhieuNhap": {
        "cat": "purchase", "x": 390, "y": 420, "w": 250,
        "fields": [
            ("MaPN", "INTEGER", True, False),
            ("MaDDH", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayNhap", "DATE", False, False),
            ("TrangThai", "VARCHAR(30)", False, False),
            ("TongTien", "DECIMAL(10,2)", False, False)
        ]
    },
    "CT_PhieuNhap": {
        "cat": "purchase", "x": 390, "y": 640, "w": 250,
        "fields": [
            ("MaPN", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuong", "INTEGER", False, False),
            ("DonGia", "DECIMAL(10,2)", False, False),
            ("ThanhTien", "(10,2)", False, False)
        ]
    },
    "CongNo": {
        "cat": "purchase", "x": 90, "y": 860, "w": 260,
        "fields": [
            ("MaCN", "INTEGER", True, False),
            ("MaNCC", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayPhatSinh", "DATE", False, False),
            ("SoTien", "DECIMAL(10,2)", False, False),
            ("SoTienDaTra", "DECIMAL(10,2)", False, False),
            ("SoTienConLai", "DECIMAL(10,2)", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },

    # --- PHÂN HỆ 3: BÁN HÀNG & HÓA ĐƠN & THU TIỀN (Cột 2) ---
    "DonHang": {
        "cat": "sales", "x": 730, "y": 420, "w": 250,
        "fields": [
            ("MaDH", "INTEGER", True, False),
            ("MaKH", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayDat", "DATE", False, False),
            ("TongTien", "DECIMAL(10,2)", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },
    "CT_DonHang": {
        "cat": "sales", "x": 730, "y": 640, "w": 250,
        "fields": [
            ("MaDH", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuong", "INTEGER", False, False),
            ("DonGia", "DECIMAL(10,2)", False, False),
            ("GiamGia", "DECIMAL(10,2)", False, False),
            ("ThanhTien", "DECIMAL(10,2)", False, False)
        ]
    },
    "HoaDon": {
        "cat": "sales", "x": 1030, "y": 420, "w": 250,
        "fields": [
            ("MaHD", "INTEGER", True, False),
            ("MaDH", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayLap", "DATE", False, False),
            ("TongTien", "DECIMAL(10,2)", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },
    "CT_HoaDon": {
        "cat": "sales", "x": 1030, "y": 640, "w": 250,
        "fields": [
            ("MaHD", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuong", "INTEGER", False, False),
            ("DonGia", "DECIMAL(10,2)", False, False),
            ("GiamGia", "DECIMAL(10,2)", False, False),
            ("ThanhTien", "DECIMAL(10,2)", False, False)
        ]
    },
    "ThanhToan": {
        "cat": "sales", "x": 1030, "y": 860, "w": 250,
        "fields": [
            ("MaTT", "INTEGER", True, False),
            ("MaHD", "INTEGER", False, True),
            ("PhuongThuc", "VARCHAR(50)", False, False),
            ("SoTien", "DECIMAL(10,2)", False, False),
            ("NgayThanhToan", "DATE", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },

    # --- PHÂN HỆ 4: KHO VẬN, KIỂM KÊ & ĐỔI TRẢ (Cột 3) ---
    "PhieuXuat": {
        "cat": "warehouse", "x": 1370, "y": 420, "w": 240,
        "fields": [
            ("MaPX", "INTEGER", True, False),
            ("MaDH", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayXuat", "DATE", False, False),
            ("LyDoXuat", "VARCHAR(200)", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },
    "CT_PhieuXuat": {
        "cat": "warehouse", "x": 1370, "y": 640, "w": 240,
        "fields": [
            ("MaPX", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuong", "INTEGER", False, False),
            ("DonGia", "DECIMAL(10,2)", False, False),
            ("ThanhTien", "DECIMAL(10,2)", False, False)
        ]
    },
    "KiemKe": {
        "cat": "warehouse", "x": 1650, "y": 420, "w": 240,
        "fields": [
            ("MaKK", "INTEGER", True, False),
            ("MaNV", "INTEGER", False, True),
            ("NgayKiemKe", "DATE", False, False),
            ("GhiChu", "TEXT", False, False)
        ]
    },
    "CT_KiemKe": {
        "cat": "warehouse", "x": 1650, "y": 640, "w": 240,
        "fields": [
            ("MaKK", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuongHeThong", "INTEGER", False, False),
            ("SoLuongThucTe", "INTEGER", False, False),
            ("ChenhLech", "INTEGER", False, False)
        ]
    },
    "PhieuTraHang": {
        "cat": "warehouse", "x": 1930, "y": 420, "w": 240,
        "fields": [
            ("MaPTH", "INTEGER", True, False),
            ("MaDH", "INTEGER", False, True),
            ("MaKH", "INTEGER", False, True),
            ("MaNV", "INTEGER", False, True),
            ("NgayTra", "DATE", False, False),
            ("LyDo", "TEXT", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },
    "CT_PhieuTraHang": {
        "cat": "warehouse", "x": 1930, "y": 640, "w": 240,
        "fields": [
            ("MaPTH", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("SoLuong", "INTEGER", False, False),
            ("DonGia", "DECIMAL(10,2)", False, False),
            ("ThanhTien", "DECIMAL(10,2)", False, False),
            ("LyDo", "TEXT", False, False)
        ]
    },

    # --- PHÂN HỆ 5: KHUYẾN MÃI & CHIẾT KHẤU (Cột 4) ---
    "KhuyenMai": {
        "cat": "promo", "x": 2250, "y": 420, "w": 250,
        "fields": [
            ("MaKM", "INTEGER", True, False),
            ("TenKM", "VARCHAR(100)", False, False),
            ("NgayBatDau", "DATE", False, False),
            ("NgayKetThuc", "DATE", False, False),
            ("PhanTramGiam", "(5,2)", False, False),
            ("DieuKienApDung", "VARCHAR(200)", False, False),
            ("TrangThai", "VARCHAR(30)", False, False)
        ]
    },
    "CT_KhuyenMai": {
        "cat": "promo", "x": 2250, "y": 660, "w": 250,
        "fields": [
            ("MaKM", "INTEGER", True, True),
            ("MaSP", "INTEGER", True, True),
            ("GiaTriGiam", "DECIMAL(10,2)", False, False)
        ]
    }
}

# Kích thước từng khối & toạ độ cổng nối
for name, t in TABLES.items():
    t["h"] = 32 + len(t["fields"]) * 22
    t["cx"] = t["x"] + t["w"] / 2
    t["cy"] = t["y"] + t["h"] / 2
    t["top"] = (t["cx"], t["y"])
    t["bottom"] = (t["cx"], t["y"] + t["h"])
    t["left"] = (t["x"], t["cy"])
    t["right"] = (t["x"] + t["w"], t["cy"])

# Các liên kết với điểm bẻ góc trực quan, chuẩn xác, triệt tiêu giao cắt chéo
RELATIONS = [
    # 1. Master Data Links
    {"from": "VaiTro", "to": "NhanVien", "p1": "right", "p2": "left", "label": "1 - n (MaVT)", "color": "#0284c7"},
    {"from": "LoaiHang", "to": "SanPham", "p1": "right", "p2": "left", "label": "1 - n (MaLoai)", "color": "#16a34a"},
    {"from": "SanPham", "to": "TonKho", "p1": "right", "p2": "left", "label": "1 - 1 (MaSP)", "color": "#16a34a"},

    # 2. Header -> Detail Pairs (Đường thẳng đứng 1-n không bao giờ cắt chéo!)
    {"from": "DonDat_Hang", "to": "CT_DonDathang", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#d97706"},
    {"from": "PhieuNhap", "to": "CT_PhieuNhap", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#d97706"},
    {"from": "DonHang", "to": "CT_DonHang", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#ec4899"},
    {"from": "HoaDon", "to": "CT_HoaDon", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#ec4899"},
    {"from": "PhieuXuat", "to": "CT_PhieuXuat", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#06b6d4"},
    {"from": "KiemKe", "to": "CT_KiemKe", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#06b6d4"},
    {"from": "PhieuTraHang", "to": "CT_PhieuTraHang", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#06b6d4"},
    {"from": "KhuyenMai", "to": "CT_KhuyenMai", "p1": "bottom", "p2": "top", "label": "1 - n", "color": "#8b5cf6"},

    # 3. Luồng chứng từ ngang
    {"from": "DonDat_Hang", "to": "PhieuNhap", "p1": "right", "p2": "left", "label": "1 - n (MaDDH)", "color": "#d97706"},
    {"from": "DonHang", "to": "HoaDon", "p1": "right", "p2": "left", "label": "1 - 1 (MaDH)", "color": "#ec4899"},
    {"from": "HoaDon", "to": "ThanhToan", "p1": "bottom", "p2": "top", "waypoints": [(1155, 780), (1155, 860)], "label": "1 - n (MaHD)", "color": "#ec4899"},

    # 4. Xuất kho & Đổi trả từ Đơn hàng
    {"from": "DonHang", "to": "PhieuXuat", "p1": "right", "p2": "left", "waypoints": [(1000, 480), (1000, 390), (1340, 390), (1340, 480)], "label": "1 - n (MaDH)", "color": "#06b6d4"},
    {"from": "DonHang", "to": "PhieuTraHang", "p1": "right", "p2": "left", "waypoints": [(1000, 520), (1000, 380), (1910, 380), (1910, 480)], "label": "1 - n (MaDH)", "color": "#06b6d4"},

    # 5. Đối tác liên kết chứng từ
    {"from": "NhaCungCap", "to": "DonDat_Hang", "p1": "bottom", "p2": "top", "waypoints": [(1630, 270), (215, 270)], "label": "1 - n (MaNCC)", "color": "#0284c7"},
    {"from": "NhaCungCap", "to": "CongNo", "p1": "bottom", "p2": "right", "waypoints": [(1630, 310), (70, 310), (70, 930)], "label": "1 - n (MaNCC)", "color": "#0284c7"},
    {"from": "KhachHang", "to": "DonHang", "p1": "bottom", "p2": "top", "waypoints": [(1920, 290), (855, 290)], "label": "1 - n (MaKH)", "color": "#0284c7"},
    {"from": "KhachHang", "to": "PhieuTraHang", "p1": "bottom", "p2": "top", "waypoints": [(1920, 300), (2050, 300)], "label": "1 - n (MaKH)", "color": "#0284c7"},

    # 6. SanPham liên kết chi tiết qua Highway Bus Channel (y = 610)
    {"from": "SanPham", "to": "CT_DonDathang", "p1": "bottom", "p2": "left", "waypoints": [(1060, 320), (50, 320), (50, 680)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_PhieuNhap", "p1": "bottom", "p2": "top", "waypoints": [(1060, 330), (515, 330)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_DonHang", "p1": "bottom", "p2": "top", "waypoints": [(1060, 340), (855, 340), (855, 620), (810, 620)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_HoaDon", "p1": "bottom", "p2": "top", "waypoints": [(1060, 340), (1155, 340), (1155, 620), (1110, 620)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_PhieuXuat", "p1": "bottom", "p2": "top", "waypoints": [(1060, 350), (1490, 350), (1490, 620), (1450, 620)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_KiemKe", "p1": "bottom", "p2": "top", "waypoints": [(1060, 350), (1770, 350), (1770, 620), (1730, 620)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_PhieuTraHang", "p1": "bottom", "p2": "top", "waypoints": [(1060, 360), (2050, 360), (2050, 620), (2010, 620)], "label": "MaSP", "color": "#16a34a"},
    {"from": "SanPham", "to": "CT_KhuyenMai", "p1": "bottom", "p2": "top", "waypoints": [(1060, 360), (2375, 360), (2375, 640)], "label": "MaSP", "color": "#16a34a"},

    # 7. NhanVien liên kết qua Staff Bus Channel (y = 280)
    {"from": "NhanVien", "to": "DonDat_Hang", "p1": "bottom", "p2": "top", "waypoints": [(475, 290), (260, 290), (260, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "PhieuNhap", "p1": "bottom", "p2": "top", "waypoints": [(475, 290), (515, 290), (515, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "DonHang", "p1": "bottom", "p2": "top", "waypoints": [(475, 280), (780, 280), (780, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "HoaDon", "p1": "bottom", "p2": "top", "waypoints": [(475, 280), (1080, 280), (1080, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "PhieuXuat", "p1": "bottom", "p2": "top", "waypoints": [(475, 280), (1420, 280), (1420, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "KiemKe", "p1": "bottom", "p2": "top", "waypoints": [(475, 280), (1700, 280), (1700, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "PhieuTraHang", "p1": "bottom", "p2": "top", "waypoints": [(475, 280), (1980, 280), (1980, 420)], "label": "MaNV", "color": "#64748b"},
    {"from": "NhanVien", "to": "CongNo", "p1": "bottom", "p2": "left", "waypoints": [(475, 300), (40, 300), (40, 930)], "label": "MaNV", "color": "#64748b"},
]


def generate_clean_svg():
    width = 2580
    height = 1140

    # Zone containers config
    zones = [
        {"name": "1. MASTER DATA (DANH MỤC DỮ LIỆU NỀN TẢNG)", "x": 60, "y": 50, "w": 2470, "h": 270, "color": "#f8fafc", "border": "#cbd5e1"},
        {"name": "2. MUA HÀNG & NHẬP KHO", "x": 60, "y": 380, "w": 610, "h": 720, "color": "#fffbeb", "border": "#fde68a"},
        {"name": "3. BÁN HÀNG, HÓA ĐƠN & THU TIỀN", "x": 700, "y": 380, "w": 610, "h": 720, "color": "#fdf2f8", "border": "#fbcfe8"},
        {"name": "4. KHO VẬN, KIỂM KÊ & ĐỔI TRẢ", "x": 1340, "y": 380, "w": 860, "h": 720, "color": "#ecfeff", "border": "#a5f3fc"},
        {"name": "5. KHUYẾN MÃI & CHIẾT KHẤU", "x": 2230, "y": 380, "w": 300, "h": 720, "color": "#f5f3ff", "border": "#ddd6fe"},
    ]

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#ffffff; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">',
        '<defs>',
        '  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">',
        '    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" stroke-width="0.8"/>',
        '  </pattern>',
        '  <!-- Crow foot markers -->',
        '  <marker id="crow" viewBox="0 0 24 24" refX="22" refY="12" markerWidth="14" markerHeight="14" orient="auto">',
        '    <path d="M 2 4 L 22 12 L 2 20 M 2 12 L 22 12" fill="none" stroke="#334155" stroke-width="1.8" />',
        '    <circle cx="6" cy="12" r="3.5" fill="#fff" stroke="#334155" stroke-width="1.6" />',
        '  </marker>',
        '  <marker id="one" viewBox="0 0 16 16" refX="2" refY="8" markerWidth="12" markerHeight="12" orient="auto">',
        '    <line x1="6" y1="2" x2="6" y2="14" stroke="#334155" stroke-width="1.8" />',
        '    <line x1="12" y1="2" x2="12" y2="14" stroke="#334155" stroke-width="1.8" />',
        '  </marker>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="url(#grid)"/>',
        '<!-- FUNCTIONAL ZONE CONTAINERS -->'
    ]

    for z in zones:
        svg_lines.append(f'<g id="zone_{z["name"][:3]}">')
        svg_lines.append(f'  <rect x="{z["x"]}" y="{z["y"]}" width="{z["w"]}" height="{z["h"]}" rx="12" fill="{z["color"]}" stroke="{z["border"]}" stroke-width="1.5" />')
        svg_lines.append(f'  <rect x="{z["x"]}" y="{z["y"]}" width="{z["w"]}" height="32" rx="12" fill="{z["border"]}" opacity="0.4" />')
        svg_lines.append(f'  <text x="{z["x"]+16}" y="{z["y"]+21}" font-size="12" font-weight="bold" fill="#334155" letter-spacing="0.5">{z["name"]}</text>')
        svg_lines.append('</g>')

    svg_lines.append('<!-- BUS CHANNELS & RELATIONSHIP LINES -->')

    for rel in RELATIONS:
        t1 = TABLES[rel["from"]]
        t2 = TABLES[rel["to"]]
        p1 = t1[rel["p1"]]
        p2 = t2[rel["p2"]]
        color = rel.get("color", "#475569")

        points = [p1]
        if "waypoints" in rel:
            points.extend(rel["waypoints"])
        else:
            if rel["p1"] in ["bottom", "top"] and rel["p2"] in ["bottom", "top"]:
                mid_y = (p1[1] + p2[1]) / 2
                points.append((p1[0], mid_y))
                points.append((p2[0], mid_y))
            elif rel["p1"] in ["left", "right"] and rel["p2"] in ["left", "right"]:
                mid_x = (p1[0] + p2[0]) / 2
                points.append((mid_x, p1[1]))
                points.append((mid_x, p2[1]))
            else:
                if rel["p1"] in ["left", "right"]:
                    points.append((p2[0], p1[1]))
                else:
                    points.append((p1[0], p2[1]))
        points.append(p2)

        d_str = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
        for pt in points[1:]:
            d_str += f" L {pt[0]:.1f} {pt[1]:.1f}"

        svg_lines.append(
            f'<path d="{d_str}" fill="none" stroke="{color}" stroke-width="1.4" '
            f'marker-start="url(#one)" marker-end="url(#crow)"/>'
        )

        # Label nếu có
        if rel.get("label"):
            mid_pt = points[len(points)//2]
            svg_lines.append(
                f'<rect x="{mid_pt[0]-24}" y="{mid_pt[1]-9}" width="48" height="18" rx="4" fill="#ffffff" stroke="{color}" stroke-width="1" />'
                f'<text x="{mid_pt[0]}" y="{mid_pt[1]+3}" font-size="9.5" font-weight="bold" text-anchor="middle" fill="{color}">{rel["label"]}</text>'
            )

    svg_lines.append('<!-- 25 TABLE BOXES -->')

    cat_colors = {
        "master": ("#0284c7", "#f0f9ff"),
        "purchase": ("#d97706", "#fffbeb"),
        "sales": ("#db2777", "#fdf2f8"),
        "warehouse": ("#0891b2", "#ecfeff"),
        "promo": ("#7c3aed", "#f5f3ff")
    }

    for name, t in TABLES.items():
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        c_hdr, c_bg = cat_colors.get(t["cat"], ("#334155", "#ffffff"))
        col1_w = int(w * 0.48)

        svg_lines.append(f'<!-- Table: {name} -->')
        svg_lines.append(f'<g id="tbl_{name}" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.06))">')
        # Thân bảng
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>')
        # Tiêu đề bảng
        svg_lines.append(f'  <path d="M {x} {y+6} Q {x} {y} {x+6} {y} L {x+w-6} {y} Q {x+w} {y} {x+w} {y+6} L {x+w} {y+30} L {x} {y+30} Z" fill="{c_hdr}"/>')
        svg_lines.append(f'  <text x="{x + w/2}" y="{y + 20}" font-size="12" font-weight="bold" text-anchor="middle" fill="#ffffff">{name}</text>')
        # Đường kẻ dọc phân cách tên trường và kiểu dữ liệu
        svg_lines.append(f'  <line x1="{x + col1_w}" y1="{y + 30}" x2="{x + col1_w}" y2="{y + h}" stroke="#e2e8f0" stroke-width="1.0"/>')

        for idx, (fname, ftype, is_pk, is_fk) in enumerate(t["fields"]):
            row_y = y + 30 + (idx * 22)
            if idx > 0:
                svg_lines.append(f'  <line x1="{x}" y1="{row_y}" x2="{x + w}" y2="{row_y}" stroke="#f1f5f9" stroke-width="0.8"/>')

            # Icon hoặc ký hiệu PK / FK
            badge = ""
            if is_pk and is_fk:
                badge = "🔑🔗 "
            elif is_pk:
                badge = "🔑 "
            elif is_fk:
                badge = "🔗 "

            f_weight = "bold" if is_pk else "normal"
            f_color = "#0f172a" if is_pk else "#334155"

            # Tên trường
            svg_lines.append(f'  <text x="{x + 8}" y="{row_y + 15}" font-size="11" font-weight="{f_weight}" fill="{f_color}">{badge}{fname}</text>')
            # Kiểu dữ liệu
            svg_lines.append(f'  <text x="{x + col1_w + 8}" y="{row_y + 15}" font-size="10.5" font-family="monospace" fill="#64748b">{ftype}</text>')

        svg_lines.append('</g>')

    svg_lines.append('</svg>')
    return "\n".join(svg_lines)


def generate_clean_drawio_xml():
    xml = [
        '<mxfile host="app.diagrams.net" modified="2026-10-07T17:50:00.000Z" agent="Antigravity" version="21.0.0" type="device">',
        '  <diagram id="BabyShopERD_Logical" name="ERD_25_Bang_Logic_Toan_Dien">',
        '    <mxGraphModel dx="2600" dy="1400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2600" pageHeight="1400" background="#ffffff">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>'
    ]

    cell_id = 100
    table_cell_ids = {}

    for name, t in TABLES.items():
        cell_id += 1
        t_id = str(cell_id)
        table_cell_ids[name] = t_id

        field_rows = ""
        for fn, ft, is_pk, is_fk in t["fields"]:
            badge = "[PK] " if is_pk else ("[FK] " if is_fk else "")
            field_rows += f"<tr><td style='border:1px solid #ddd;padding:3px 6px;'><b>{badge}{fn}</b></td><td style='border:1px solid #ddd;padding:3px 6px;color:#666;'>{ft}</td></tr>"

        html_val = f"&lt;table style='width:100%;border-collapse:collapse;font-size:11px;'&gt;&lt;tr&gt;&lt;th colspan='2' style='background:#1e293b;color:#fff;border:1px solid #333;padding:5px;'&gt;{name}&lt;/th&gt;&lt;/tr&gt;{field_rows}&lt;/table&gt;"

        xml.append(
            f'        <mxCell id="{t_id}" value="{html_val}" style="text;html=1;whiteSpace=wrap;overflow=hidden;rounded=1;shadow=0;strokeColor=#cbd5e1;fillColor=#ffffff;" vertex="1" parent="1">'
        )
        xml.append(
            f'          <mxGeometry x="{t["x"]}" y="{t["y"]}" width="{t["w"]}" height="{t["h"]}" as="geometry"/>'
        )
        xml.append('        </mxCell>')

    for rel in RELATIONS:
        cell_id += 1
        edge_id = str(cell_id)
        src_id = table_cell_ids[rel["from"]]
        trg_id = table_cell_ids[rel["to"]]

        xml.append(
            f'        <mxCell id="{edge_id}" value="{rel.get("label", "")}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;strokeColor={rel.get("color", "#334155")};strokeWidth=1.5;" edge="1" parent="1" source="{src_id}" target="{trg_id}">'
        )
        xml.append('          <mxGeometry relative="1" as="geometry"/>')
        xml.append('        </mxCell>')

    xml.extend([
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>'
    ])
    return "\n".join(xml)


def main():
    svg_content = generate_clean_svg()
    drawio_content = generate_clean_drawio_xml()

    # 1. Ghi SVG
    for p in [ROOT / "so_do_erd_chuan.svg", DB_DIR / "so_do_erd_chuan.svg"]:
        p.write_text(svg_content, encoding="utf-8")
    print(f"✅ Đã ghi SVG: {ROOT / 'so_do_erd_chuan.svg'}")

    # 2. Ghi Drawio
    for p in [ROOT / "so_do_erd_chuan.drawio", DB_DIR / "so_do_erd_chuan.drawio"]:
        p.write_text(drawio_content, encoding="utf-8")
    print(f"✅ Đã ghi Draw.io: {ROOT / 'so_do_erd_chuan.drawio'}")

    # 3. Ghi HTML
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ Đồ ERD Logic Chuẩn Hóa - Baby Shop Management</title>
  <style>
    body {{
      margin: 0;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial, sans-serif;
      background: #f1f5f9;
    }}
    .header {{
      background: #ffffff;
      padding: 14px 24px;
      border-radius: 12px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border: 1px solid #e2e8f0;
    }}
    .btn {{
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .btn-svg {{ background: #10b981; color: white; }}
    .btn-svg:hover {{ background: #059669; }}
    .btn-png {{ background: #0284c7; color: white; }}
    .btn-png:hover {{ background: #0369a1; }}
    .canvas-container {{
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      padding: 12px;
      overflow: auto;
      border: 1px solid #e2e8f0;
    }}
    svg {{
      min-width: 1600px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1 style="margin:0; font-size:17px; color:#0f172a; font-weight:700;">SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 25 BẢNG CƠ SỞ DỮ LIỆU CHUẨN HÓA</h1>
      <p style="margin:4px 0 0; font-size:12px; color:#64748b;">Bố cục 5 Phân hệ kiến trúc rõ ràng • Ghép đôi Header - Detail theo trục dọc • Tuyệt đối không giao cắt chồng chéo</p>
    </div>
    <div style="display:flex; gap:10px;">
      <a href="so_do_erd_chuan.svg" download class="btn btn-svg">📥 Tải SVG Vector</a>
      <a href="so_do_erd_chuan.png" download class="btn btn-png">🖼️ Tải PNG Siêu Nét</a>
    </div>
  </div>
  <div class="canvas-container">
    {svg_content}
  </div>
</body>
</html>"""

    for p in [ROOT / "so_do_erd_chuan.html", DB_DIR / "so_do_erd_chuan.html"]:
        p.write_text(html_content, encoding="utf-8")
    print(f"✅ Đã ghi HTML: {ROOT / 'so_do_erd_chuan.html'}")

    # 4. Xuất PNG chất lượng cao
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    png_path = ROOT / "so_do_erd_chuan.png"
    html_target = ROOT / "so_do_erd_chuan.html"

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--window-size=2650,1250",
        f"--screenshot={png_path}",
        str(html_target.resolve().as_uri())
    ]
    try:
        subprocess.run(cmd, check=True, timeout=15)
        print(f"✅ Đã xuất PNG sắc nét: {png_path} ({png_path.stat().st_size} bytes)")
        (DB_DIR / "so_do_erd_chuan.png").write_bytes(png_path.read_bytes())
    except Exception as e:
        print(f"Lỗi chụp màn hình: {e}")


if __name__ == "__main__":
    main()
