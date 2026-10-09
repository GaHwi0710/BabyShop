import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/BabyShop")
DB_DIR = ROOT / "database"

# 32 Collections đầy đủ của MongoDB baby_shop_management
# Mỗi trường có: (Tên trường, Kiểu dữ liệu)
TABLES = {
    # === CỘT 1: NGƯỜI DÙNG & HỆ THỐNG ===
    "Users": {
        "col": 1,
        "fields": [
            ("_id", "ObjectId"),
            ("username", "String"),
            ("fullName", "String"),
            ("role", "String"),
            ("status", "String"),
            ("passwordHash", "String"),
            ("email", "String"),
            ("phone", "String"),
            ("CCCD", "String"),
            ("createdAt", "Date")
        ]
    },
    "VaiTro": {
        "col": 1,
        "fields": [
            ("_id", "ObjectId"),
            ("MaVaiTro", "Number"),
            ("TenVaiTro", "String"),
            ("MaKey", "String"),
            ("LaVaiTroHeThong", "Boolean"),
            ("QuyenHan", "Object")
        ]
    },
    "NhanVien": {
        "col": 1,
        "fields": [
            ("_id", "ObjectId"),
            ("MaNV", "String"),
            ("HoTen", "String"),
            ("ChucVu", "String"),
            ("PhongBan", "String"),
            ("SDT", "String"),
            ("Email", "String"),
            ("username", "String"),
            ("MaVaiTro", "Number"),
            ("TrangThai", "String")
        ]
    },
    "Counters": {
        "col": 1,
        "fields": [
            ("_id", "String"),
            ("seq", "Number")
        ]
    },
    "AuditLogs": {
        "col": 1,
        "fields": [
            ("_id", "ObjectId"),
            ("timestamp", "Date"),
            ("userId", "String"),
            ("username", "String"),
            ("action", "String"),
            ("module", "String"),
            ("entity", "String"),
            ("description", "String")
        ]
    },
    "_metadata": {
        "col": 1,
        "fields": [
            ("_id", "String"),
            ("key", "String"),
            ("value", "Object"),
            ("appliedAt", "Date")
        ]
    },

    # === CỘT 2: ĐỐI TÁC, DANH MỤC & HÀNG HÓA ===
    "LoaiHang": {
        "col": 2,
        "fields": [
            ("_id", "ObjectId"),
            ("MaLoai", "String"),
            ("TenLoai", "String"),
            ("MoTa", "String"),
            ("TrangThai", "String")
        ]
    },
    "NhaCungCap": {
        "col": 2,
        "fields": [
            ("_id", "ObjectId"),
            ("MaNCC", "String"),
            ("TenNCC", "String"),
            ("NguoiLienHe", "String"),
            ("SDT", "String"),
            ("DiaChi", "String"),
            ("Email", "String")
        ]
    },
    "KhachHang": {
        "col": 2,
        "fields": [
            ("_id", "ObjectId"),
            ("MaKH", "String"),
            ("HoTen", "String"),
            ("SDT", "String"),
            ("Email", "String"),
            ("DiaChi", "String"),
            ("DiemTichLuy", "Number"),
            ("CapThanhVien", "String")
        ]
    },
    "SanPham": {
        "col": 2,
        "fields": [
            ("_id", "ObjectId"),
            ("MaSP", "String"),
            ("TenSP", "String"),
            ("MaLoai", "ObjectId"),
            ("DonViTinh", "String"),
            ("GiaNhap", "Number"),
            ("GiaBan", "Number"),
            ("HanSuDung", "String"),
            ("stock", "Number"),
            ("TrangThai", "String")
        ]
    },
    "TonKho": {
        "col": 2,
        "fields": [
            ("_id", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuongTon", "Number"),
            ("SoLuong", "Number"),
            ("NgayCapNhat", "String"),
            ("updatedAt", "Date")
        ]
    },

    # === CỘT 3: MUA HÀNG & NHẬP KHO ===
    "DonDatHang": {
        "col": 3,
        "fields": [
            ("_id", "ObjectId"),
            ("MaDDH", "String"),
            ("MaNCC", "ObjectId"),
            ("MaNV", "ObjectId"),
            ("NgayDat", "String"),
            ("TongTien", "Number"),
            ("TrangThai", "String"),
            ("NguoiLap", "String")
        ]
    },
    "CT_DonDatHang": {
        "col": 3,
        "fields": [
            ("_id", "ObjectId"),
            ("MaDDH", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },
    "PhieuNhap": {
        "col": 3,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPN", "String"),
            ("MaDDH", "ObjectId"),
            ("MaNCC", "ObjectId"),
            ("MaNV", "ObjectId"),
            ("NgayNhap", "String"),
            ("TongTien", "Number"),
            ("TrangThai", "String")
        ]
    },
    "CT_PhieuNhap": {
        "col": 3,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPN", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },

    # === CỘT 4: BÁN HÀNG, HÓA ĐƠN & XUẤT KHO ===
    "DonHang": {
        "col": 4,
        "fields": [
            ("_id", "ObjectId"),
            ("MaDH", "String"),
            ("MaKH", "ObjectId"),
            ("MaNV", "ObjectId"),
            ("NgayDat", "String"),
            ("TongTien", "Number"),
            ("TienGiam", "Number"),
            ("ThanhTien", "Number"),
            ("TrangThai", "String")
        ]
    },
    "CT_DonHang": {
        "col": 4,
        "fields": [
            ("_id", "ObjectId"),
            ("MaDH", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },
    "HoaDon": {
        "col": 4,
        "fields": [
            ("_id", "ObjectId"),
            ("MaHD", "String"),
            ("MaDH", "ObjectId"),
            ("MaKH", "ObjectId"),
            ("NgayLap", "String"),
            ("TongTien", "Number"),
            ("SoTienDaTra", "Number"),
            ("ConNo", "Number"),
            ("TrangThai", "String")
        ]
    },
    "CT_HoaDon": {
        "col": 4,
        "fields": [
            ("_id", "ObjectId"),
            ("MaHD", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },
    "PhieuXuat": {
        "col": 4,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPX", "String"),
            ("MaDH", "ObjectId"),
            ("MaNV", "ObjectId"),
            ("NgayXuat", "String"),
            ("TongTien", "Number"),
            ("TrangThai", "String")
        ]
    },
    "CT_PhieuXuat": {
        "col": 4,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPX", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },

    # === CỘT 5: KIỂM KÊ, CÂN BẰNG & ĐỔI TRẢ ===
    "KiemKe": {
        "col": 5,
        "fields": [
            ("_id", "ObjectId"),
            ("MaKK", "String"),
            ("NgayKiemKe", "String"),
            ("NguoiKiemKe", "String"),
            ("TrangThai", "String"),
            ("GhiChu", "String")
        ]
    },
    "CT_KiemKe": {
        "col": 5,
        "fields": [
            ("_id", "ObjectId"),
            ("MaKK", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuongHeThong", "Number"),
            ("SoLuongThucTe", "Number"),
            ("ChenhLech", "Number"),
            ("LyDo", "String")
        ]
    },
    "DieuChinhKho": {
        "col": 5,
        "fields": [
            ("_id", "ObjectId"),
            ("MaDC", "String"),
            ("MaKK", "ObjectId"),
            ("NgayDieuChinh", "String"),
            ("NguoiThucHien", "String"),
            ("LyDo", "String")
        ]
    },
    "PhieuTraHang": {
        "col": 5,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPTH", "String"),
            ("MaDH", "ObjectId"),
            ("MaHD", "ObjectId"),
            ("MaKH", "ObjectId"),
            ("MaNV", "ObjectId"),
            ("NgayTra", "String"),
            ("LyDo", "String"),
            ("TrangThai", "String")
        ]
    },
    "CT_PhieuTraHang": {
        "col": 5,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPTH", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },

    # === CỘT 6: TÀI CHÍNH, QUỸ & KHUYẾN MÃI ===
    "CongNo": {
        "col": 6,
        "fields": [
            ("_id", "ObjectId"),
            ("MaCN", "String"),
            ("MaPN", "ObjectId"),
            ("MaNCC", "ObjectId"),
            ("MaHD", "ObjectId"),
            ("MaKH", "ObjectId"),
            ("LoaiCongNo", "String"),
            ("SoTien", "Number"),
            ("SoTienDaTra", "Number"),
            ("SoTienConLai", "Number"),
            ("TrangThai", "String")
        ]
    },
    "ThanhToan": {
        "col": 6,
        "fields": [
            ("_id", "ObjectId"),
            ("MaTT", "String"),
            ("MaHD", "ObjectId"),
            ("SoTien", "Number"),
            ("PhuongThuc", "String"),
            ("NgayThanhToan", "String"),
            ("TrangThai", "String")
        ]
    },
    "PhieuThu": {
        "col": 6,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPT", "String"),
            ("NgayLap", "String"),
            ("NguoiNopTien", "String"),
            ("LyDo", "String"),
            ("SoTien", "Number"),
            ("ChungTuGoc", "String"),
            ("TrangThai", "String")
        ]
    },
    "PhieuChi": {
        "col": 6,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPC", "String"),
            ("NgayLap", "String"),
            ("NguoiNhanTien", "String"),
            ("LyDo", "String"),
            ("SoTien", "Number"),
            ("ChungTuGoc", "String"),
            ("TrangThai", "String")
        ]
    },
    "KhuyenMai": {
        "col": 6,
        "fields": [
            ("_id", "ObjectId"),
            ("MaKM", "String"),
            ("TenKM", "String"),
            ("LoaiKM", "String"),
            ("GiaTriGiam", "Number"),
            ("PhanTramGiam", "Number"),
            ("NgayBatDau", "String"),
            ("NgayKetThuc", "String"),
            ("TrangThai", "String")
        ]
    },
    "CT_KhuyenMai": {
        "col": 6,
        "fields": [
            ("_id", "ObjectId"),
            ("MaKM", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("createdAt", "Date")
        ]
    }
}

# Cấu hình kích thước & khoảng cách chuẩn
TABLE_W = 250
HEADER_H = 26
ROW_H = 19
COL_GAP = 60
START_X = 50
START_Y = 60

COL_X = {
    1: START_X,
    2: START_X + 1 * (TABLE_W + COL_GAP),
    3: START_X + 2 * (TABLE_W + COL_GAP),
    4: START_X + 3 * (TABLE_W + COL_GAP),
    5: START_X + 4 * (TABLE_W + COL_GAP),
    6: START_X + 5 * (TABLE_W + COL_GAP)
}

col_y = {1: START_Y, 2: START_Y, 3: START_Y, 4: START_Y, 5: START_Y, 6: START_Y}

# Tính toán vị trí từng bảng và vị trí chính xác của từng trường (field anchor)
for name, t in TABLES.items():
    c = t["col"]
    t["w"] = TABLE_W
    t["x"] = COL_X[c]
    t["y"] = col_y[c]
    t["h"] = HEADER_H + len(t["fields"]) * ROW_H
    col_y[c] += t["h"] + 18  # Cách nhau 18px trong cùng cột

    t["field_y"] = {}
    for idx, (fname, ftype) in enumerate(t["fields"]):
        # Tọa độ Y trung tâm của từng dòng trường
        t["field_y"][fname] = t["y"] + HEADER_H + idx * ROW_H + ROW_H / 2


# Danh sách quan hệ chính xác nối từ trường nguồn sang trường đích
# Mỗi quan hệ gồm: (Bảng nguồn, Trường nguồn, Bảng đích, Trường đích, Kiểu quan hệ)
RELATIONS = [
    # Cột 1
    {"src": "VaiTro", "src_f": "MaVaiTro", "dst": "NhanVien", "dst_f": "MaVaiTro", "type": "1:n"},
    {"src": "Users", "src_f": "username", "dst": "NhanVien", "dst_f": "username", "type": "1:1"},
    {"src": "Users", "src_f": "_id", "dst": "AuditLogs", "dst_f": "userId", "type": "1:n"},

    # Cột 2
    {"src": "LoaiHang", "src_f": "_id", "dst": "SanPham", "dst_f": "MaLoai", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "TonKho", "dst_f": "MaSP", "type": "1:1"},

    # Cột 2 -> Cột 3
    {"src": "NhaCungCap", "src_f": "_id", "dst": "DonDatHang", "dst_f": "MaNCC", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_DonDatHang", "dst_f": "MaSP", "type": "1:n"},
    {"src": "DonDatHang", "src_f": "_id", "dst": "CT_DonDatHang", "dst_f": "MaDDH", "type": "1:n"},
    {"src": "DonDatHang", "src_f": "_id", "dst": "PhieuNhap", "dst_f": "MaDDH", "type": "1:n"},
    {"src": "PhieuNhap", "src_f": "_id", "dst": "CT_PhieuNhap", "dst_f": "MaPN", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_PhieuNhap", "dst_f": "MaSP", "type": "1:n"},

    # Cột 2 -> Cột 4 (Bán hàng)
    {"src": "KhachHang", "src_f": "_id", "dst": "DonHang", "dst_f": "MaKH", "type": "1:n"},
    {"src": "DonHang", "src_f": "_id", "dst": "CT_DonHang", "dst_f": "MaDH", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_DonHang", "dst_f": "MaSP", "type": "1:n"},
    {"src": "DonHang", "src_f": "_id", "dst": "HoaDon", "dst_f": "MaDH", "type": "1:1"},
    {"src": "HoaDon", "src_f": "_id", "dst": "CT_HoaDon", "dst_f": "MaHD", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_HoaDon", "dst_f": "MaSP", "type": "1:n"},
    {"src": "DonHang", "src_f": "_id", "dst": "PhieuXuat", "dst_f": "MaDH", "type": "1:n"},
    {"src": "PhieuXuat", "src_f": "_id", "dst": "CT_PhieuXuat", "dst_f": "MaPX", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_PhieuXuat", "dst_f": "MaSP", "type": "1:n"},

    # Cột 4 -> Cột 5 (Kho vận & Đổi trả)
    {"src": "KiemKe", "src_f": "_id", "dst": "CT_KiemKe", "dst_f": "MaKK", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_KiemKe", "dst_f": "MaSP", "type": "1:n"},
    {"src": "KiemKe", "src_f": "_id", "dst": "DieuChinhKho", "dst_f": "MaKK", "type": "1:1"},
    {"src": "DonHang", "src_f": "_id", "dst": "PhieuTraHang", "dst_f": "MaDH", "type": "1:n"},
    {"src": "PhieuTraHang", "src_f": "_id", "dst": "CT_PhieuTraHang", "dst_f": "MaPTH", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_PhieuTraHang", "dst_f": "MaSP", "type": "1:n"},

    # Cột 6 (Tài chính & Khuyến mãi)
    {"src": "PhieuNhap", "src_f": "_id", "dst": "CongNo", "dst_f": "MaPN", "type": "1:1"},
    {"src": "HoaDon", "src_f": "_id", "dst": "CongNo", "dst_f": "MaHD", "type": "1:1"},
    {"src": "HoaDon", "src_f": "_id", "dst": "ThanhToan", "dst_f": "MaHD", "type": "1:n"},
    {"src": "HoaDon", "src_f": "MaHD", "dst": "PhieuThu", "dst_f": "ChungTuGoc", "type": "1:n"},
    {"src": "PhieuNhap", "src_f": "MaPN", "dst": "PhieuChi", "dst_f": "ChungTuGoc", "type": "1:n"},
    {"src": "KhuyenMai", "src_f": "_id", "dst": "CT_KhuyenMai", "dst_f": "MaKM", "type": "1:n"},
    {"src": "SanPham", "src_f": "_id", "dst": "CT_KhuyenMai", "dst_f": "MaSP", "type": "1:n"}
]


def generate_svg():
    width = START_X + 6 * (TABLE_W + COL_GAP) + 20
    height = max(col_y.values()) + 40

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#ffffff; font-family: Arial, Helvetica, sans-serif;">',
        '<defs>',
        '  <!-- Mũi tên tam giác đen đặc chuẩn bản vẽ kỹ thuật -->',
        '  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
        '    <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#000000" />',
        '  </marker>',
        '  <!-- Ký hiệu vạch vuông 1 đầu nguồn -->',
        '  <marker id="src-bar" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="5" markerHeight="5" orient="auto">',
        '    <line x1="2" y1="1" x2="2" y2="9" stroke="#000000" stroke-width="2.5" />',
        '  </marker>',
        '</defs>',
        '<!-- Header Title Banner -->',
        '<text x="50%" y="34" font-size="18" font-weight="bold" text-anchor="middle" fill="#000000">Sơ đồ cơ sở dữ liệu MongoDB hoàn thiện thực tế (32 Collections)</text>',
        '<!-- RELATIONSHIP LINES -->'
    ]

    # Vẽ các đường nối chính xác từ trường nguồn sang trường đích
    for rel in RELATIONS:
        t_src = TABLES[rel["src"]]
        t_dst = TABLES[rel["dst"]]
        src_f = rel["src_f"]
        dst_f = rel["dst_f"]

        y1 = t_src["field_y"].get(src_f, t_src["y"] + 35)
        y2 = t_dst["field_y"].get(dst_f, t_dst["y"] + 35)

        # Nếu đích ở bên phải nguồn: xuất phát từ mép phải nguồn sang mép trái đích
        if t_dst["col"] > t_src["col"]:
            x1 = t_src["x"] + t_src["w"]
            x2 = t_dst["x"]
            mid_x = (x1 + x2) / 2
            path_d = f"M {x1} {y1} L {mid_x} {y1} L {mid_x} {y2} L {x2} {y2}"
            label_x = x2 - 28
            label_y = y2 - 4
        elif t_dst["col"] == t_src["col"]:
            # Cùng cột (Header nối Detail hoặc nối xuống dưới)
            if y2 > y1:
                x1 = t_src["x"] + t_src["w"]
                x2 = t_dst["x"] + t_dst["w"]
                mid_x = x1 + 18
                path_d = f"M {x1} {y1} L {mid_x} {y1} L {mid_x} {y2} L {x2} {y2}"
                label_x = mid_x + 4
                label_y = (y1 + y2) / 2
            else:
                x1 = t_src["x"]
                x2 = t_dst["x"]
                mid_x = x1 - 18
                path_d = f"M {x1} {y1} L {mid_x} {y1} L {mid_x} {y2} L {x2} {y2}"
                label_x = mid_x - 30
                label_y = (y1 + y2) / 2
        else:
            # Đích ở bên trái nguồn
            x1 = t_src["x"]
            x2 = t_dst["x"] + t_dst["w"]
            mid_x = (x1 + x2) / 2
            path_d = f"M {x1} {y1} L {mid_x} {y1} L {mid_x} {y2} L {x2} {y2}"
            label_x = x2 + 6
            label_y = y2 - 4

        svg.append(f'<path d="{path_d}" fill="none" stroke="#000000" stroke-width="1.1" marker-start="url(#src-bar)" marker-end="url(#arrow)"/>')

        # Nhãn điều kiện nhỏ, tinh tế ngay sát đầu mũi tên
        cond_text = f"{rel['type']}"
        svg.append(f'<text x="{label_x}" y="{label_y}" font-size="8.5" font-family="monospace" font-weight="bold" fill="#000000">{cond_text}</text>')

    svg.append('<!-- 32 TABLE BOXES -->')

    # Vẽ từng bảng chuẩn phong cách ảnh mẫu
    for name, t in TABLES.items():
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        col1_w = int(w * 0.54)

        svg.append(f'<!-- Table: {name} -->')
        svg.append(f'<g id="tbl_{name}">')
        # Thân bảng viền đen nền trắng
        svg.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>')
        # Header đen đặc
        svg.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{HEADER_H}" fill="#000000" stroke="#000000" stroke-width="1.6"/>')
        # Tiêu đề bảng chữ trắng in đậm
        svg.append(f'  <text x="{x + w/2}" y="{y + 18}" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#ffffff">{name}</text>')
        # Đường kẻ dọc phân cách tên trường và kiểu dữ liệu
        svg.append(f'  <line x1="{x + col1_w}" y1="{y + HEADER_H}" x2="{x + col1_w}" y2="{y + h}" stroke="#000000" stroke-width="1.0"/>')

        for idx, (fname, ftype) in enumerate(t["fields"]):
            row_y = y + HEADER_H + idx * ROW_H
            # Đường kẻ ngang giữa các dòng
            if idx > 0:
                svg.append(f'  <line x1="{x}" y1="{row_y}" x2="{x + w}" y2="{row_y}" stroke="#000000" stroke-width="0.6"/>')

            # Tên trường
            f_weight = "bold" if fname == "_id" else "normal"
            svg.append(f'  <text x="{x + 8}" y="{row_y + 13.5}" font-size="11" font-weight="{f_weight}" fill="#000000">{fname}</text>')
            # Kiểu dữ liệu
            svg.append(f'  <text x="{x + col1_w + 8}" y="{row_y + 13.5}" font-size="10.5" fill="#000000">{ftype}</text>')

        svg.append('</g>')

    svg.append('</svg>')
    return "\n".join(svg)


def generate_drawio():
    xml = [
        '<mxfile host="app.diagrams.net" modified="2026-10-07T18:00:00.000Z" agent="Antigravity" version="26.0.0" type="device">',
        '  <diagram id="BabyShop_Clean_32" name="MongoDB_32_Collections_Clean">',
        '    <mxGraphModel dx="2600" dy="1600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2400" pageHeight="1600" background="#ffffff">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>'
    ]

    field_cell_map = {}

    for name, t in TABLES.items():
        tbl_id = f"tbl_{name}"
        t_x = t["x"]
        t_y = t["y"]
        t_w = t["w"]
        t_h = t["h"]
        c1_w = int(t_w * 0.54)
        c2_w = t_w - c1_w

        # Container bảng chuẩn Draw.io (shape=table; childLayout=tableLayout)
        tbl_style = (
            f"shape=table;startSize={HEADER_H};container=1;collapsible=0;childLayout=tableLayout;"
            f"fixedRows=1;rowLines=1;fontStyle=1;align=center;resizeLast=1;"
            f"strokeColor=#000000;fillColor=#000000;fontColor=#ffffff;fontSize=12;"
        )
        xml.append(f'        <mxCell id="{tbl_id}" value="{name}" style="{tbl_style}" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{t_x}" y="{t_y}" width="{t_w}" height="{t_h}" as="geometry"/>')
        xml.append('        </mxCell>')

        for idx, (fn, ft) in enumerate(t["fields"]):
            row_id = f"{tbl_id}_r{idx}"
            field_cell_map[(name, fn)] = row_id
            row_y = HEADER_H + idx * ROW_H

            # Dòng dữ liệu (tableRow) - có port kết nối 2 phía đông tây (trái/phải)
            row_style = (
                "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;"
                "fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
                "top=0;left=0;right=0;bottom=1;"
            )
            xml.append(f'        <mxCell id="{row_id}" value="" style="{row_style}" vertex="1" parent="{tbl_id}">')
            xml.append(f'          <mxGeometry y="{row_y}" width="{t_w}" height="{ROW_H}" as="geometry"/>')
            xml.append('        </mxCell>')

            # Cột 1: Tên trường (Field Name) - click đúp sửa trực tiếp
            fn_bold = 1 if fn == "_id" else 0
            c1_style = (
                f"shape=partialRectangle;connectable=0;fillColor=#ffffff;top=0;left=0;bottom=0;right=1;"
                f"overflow=hidden;align=left;spacingLeft=8;fontStyle={fn_bold};strokeColor=#000000;fontColor=#000000;fontSize=11;"
            )
            c1_id = f"{row_id}_c1"
            xml.append(f'        <mxCell id="{c1_id}" value="{fn}" style="{c1_style}" vertex="1" parent="{row_id}">')
            xml.append(f'          <mxGeometry width="{c1_w}" height="{ROW_H}" as="geometry">')
            xml.append(f'            <mxRectangle width="{c1_w}" height="{ROW_H}" as="alternateBounds"/>')
            xml.append('          </mxGeometry>')
            xml.append('        </mxCell>')

            # Cột 2: Kiểu dữ liệu BSON (Data Type) - click đúp sửa trực tiếp
            c2_style = (
                f"shape=partialRectangle;connectable=0;fillColor=#ffffff;top=0;left=0;bottom=0;right=0;"
                f"overflow=hidden;align=left;spacingLeft=8;fontStyle=0;strokeColor=#000000;fontColor=#000000;fontSize=10;"
            )
            c2_id = f"{row_id}_c2"
            xml.append(f'        <mxCell id="{c2_id}" value="{ft}" style="{c2_style}" vertex="1" parent="{row_id}">')
            xml.append(f'          <mxGeometry x="{c1_w}" width="{c2_w}" height="{ROW_H}" as="geometry">')
            xml.append(f'            <mxRectangle width="{c2_w}" height="{ROW_H}" as="alternateBounds"/>')
            xml.append('          </mxGeometry>')
            xml.append('        </mxCell>')

    # Các đường liên kết quan hệ (Edges) kết nối chính xác theo dòng trường
    for rel_idx, rel in enumerate(RELATIONS):
        edge_id = f"rel_{rel_idx}"
        src_name = rel["src"]
        dst_name = rel["dst"]
        src_f = rel["src_f"]
        dst_f = rel["dst_f"]
        rel_type = rel["type"]

        src_row_id = field_cell_map.get((src_name, src_f), f"tbl_{src_name}")
        dst_row_id = field_cell_map.get((dst_name, dst_f), f"tbl_{dst_name}")

        t_src = TABLES[src_name]
        t_dst = TABLES[dst_name]

        if t_dst["col"] > t_src["col"]:
            port_props = "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
        elif t_dst["col"] < t_src["col"]:
            port_props = "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
        else:
            # Cùng cột
            y1 = t_src["field_y"].get(src_f, t_src["y"])
            y2 = t_dst["field_y"].get(dst_f, t_dst["y"])
            if y2 >= y1:
                port_props = "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
            else:
                port_props = "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"

        cond_label = f"{rel_type} ({src_f})" if src_f == dst_f else f"{rel_type} ({src_f} -&gt; {dst_f})"

        edge_style = (
            f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            f"startArrow=ERmandOne;startFill=0;endArrow=block;endFill=1;"
            f"strokeColor=#000000;strokeWidth=1.2;fontSize=9;fontStyle=1;{port_props}"
        )

        xml.append(f'        <mxCell id="{edge_id}" value="{cond_label}" style="{edge_style}" edge="1" source="{src_row_id}" target="{dst_row_id}" parent="1">')
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
    svg_content = generate_svg()
    drawio_content = generate_drawio()

    # 1. Ghi SVG
    for p in [ROOT / "so_do_erd_mongodb_32_bang.svg", DB_DIR / "so_do_erd_mongodb_32_bang.svg"]:
        p.write_text(svg_content, encoding="utf-8")
    print("✅ Đã ghi file SVG 32 bảng")

    # 2. Ghi Draw.io
    for p in [ROOT / "so_do_erd_mongodb_32_bang.drawio", DB_DIR / "so_do_erd_mongodb_32_bang.drawio"]:
        p.write_text(drawio_content, encoding="utf-8")
    print("✅ Đã ghi file Draw.io 32 bảng")

    # 3. Tạo bảng tra cứu điều kiện liên kết dạng HTML
    condition_rows = ""
    for r in RELATIONS:
        condition_rows += f"""<tr>
            <td style="padding:6px 12px; border:1px solid #e2e8f0; font-weight:bold;">{r['src']}</td>
            <td style="padding:6px 12px; border:1px solid #e2e8f0; font-family:monospace; color:#0284c7;">{r['src_f']}</td>
            <td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-weight:bold; color:#10b981;">{r['type']}</td>
            <td style="padding:6px 12px; border:1px solid #e2e8f0; font-weight:bold;">{r['dst']}</td>
            <td style="padding:6px 12px; border:1px solid #e2e8f0; font-family:monospace; color:#0284c7;">{r['dst_f']}</td>
            <td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:11px; color:#64748b;">$lookup: {r['src']}.{r['src_f']} = {r['dst']}.{r['dst_f']}</td>
        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ Đồ ERD MongoDB Chuẩn 32 Collections - Dễ Nhìn & Sắc Nét</title>
  <style>
    body {{
      margin: 0;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial, sans-serif;
      background: #f8fafc;
      color: #0f172a;
    }}
    .header {{
      background: #000000;
      color: #ffffff;
      padding: 14px 24px;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}
    .btn {{
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: bold;
      text-decoration: none;
      margin-left: 8px;
    }}
    .btn-svg {{ background: #10b981; color: white; }}
    .btn-png {{ background: #0284c7; color: white; }}
    .canvas-wrap {{
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 16px;
      overflow: auto;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      margin-bottom: 24px;
    }}
    svg {{
      min-width: 1750px;
      display: block;
    }}
    .lookup-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      background: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .lookup-table th {{
      background: #0f172a;
      color: #ffffff;
      padding: 8px 12px;
      text-align: left;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h2 style="margin:0; font-size:16px;">SƠ ĐỒ CƠ SỞ DỮ LIỆU MONGODB THỰC TẾ (32 COLLECTIONS)</h2>
      <p style="margin:4px 0 0; font-size:12px; color:#cbd5e1;">Bố cục 6 cột chuẩn tỷ lệ • Đường nối chính xác từng dòng thuộc tính • Không chồng chéo</p>
    </div>
    <div>
      <a href="so_do_erd_mongodb_32_bang.svg" download class="btn btn-svg">Tải SVG</a>
      <a href="so_do_erd_mongodb_32_bang.png" download class="btn btn-png">Tải PNG Siêu Nét</a>
    </div>
  </div>

  <div class="canvas-wrap">
    {svg_content}
  </div>

  <div style="background:#ffffff; padding:20px; border-radius:8px; border:1px solid #e2e8f0;">
    <h3 style="margin:0 0 12px 0; font-size:15px; color:#0f172a;">📋 BẢNG TRA CỨU ĐIỀU KIỆN LIÊN KẾT (JOIN / $LOOKUP MAPPING) GIỮA 32 BẢNG</h3>
    <table class="lookup-table">
      <thead>
        <tr>
          <th>Bảng Nguồn (Parent)</th>
          <th>Trường Nguồn</th>
          <th style="text-align:center;">Quan Hệ</th>
          <th>Bảng Đích (Child)</th>
          <th>Trường Đích (FK)</th>
          <th>Cú Pháp Điều Kiện $lookup</th>
        </tr>
      </thead>
      <tbody>
        {condition_rows}
      </tbody>
    </table>
  </div>
</body>
</html>"""

    for p in [ROOT / "so_do_erd_mongodb_32_bang.html", DB_DIR / "so_do_erd_mongodb_32_bang.html"]:
        p.write_text(html_content, encoding="utf-8")
    print("✅ Đã ghi file HTML 32 bảng")

    # 4. Xuất PNG
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    png_path = ROOT / "so_do_erd_mongodb_32_bang.png"
    html_target = ROOT / "so_do_erd_mongodb_32_bang.html"

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--window-size=2000,1380",
        f"--screenshot={png_path}",
        str(html_target.resolve().as_uri())
    ]
    try:
        subprocess.run(cmd, check=True, timeout=15)
        print(f"✅ Đã xuất PNG sắc nét 32 bảng: {png_path} ({png_path.stat().st_size} bytes)")
        (DB_DIR / "so_do_erd_mongodb_32_bang.png").write_bytes(png_path.read_bytes())
    except Exception as e:
        print(f"Lỗi chụp màn hình: {e}")


if __name__ == "__main__":
    main()
