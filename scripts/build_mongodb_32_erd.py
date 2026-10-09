import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/BabyShop")
DB_DIR = ROOT / "database"

# 32 Collections thực tế trong MongoDB của baby_shop_management
# Mỗi collection gồm: (Tên trường, Kiểu dữ liệu BSON/MongoDB)
TABLES = {
    # === CỘT 1: NGƯỜI DÙNG, HỆ THỐNG & KIỂM TOÁN (6 BẢNG) ===
    "Users": {
        "col": 1, "w": 280,
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
        "col": 1, "w": 280,
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
        "col": 1, "w": 280,
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
        "col": 1, "w": 280,
        "fields": [
            ("_id", "String"),
            ("seq", "Number")
        ]
    },
    "AuditLogs": {
        "col": 1, "w": 280,
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
        "col": 1, "w": 280,
        "fields": [
            ("_id", "String"),
            ("key", "String"),
            ("value", "Object"),
            ("appliedAt", "Date")
        ]
    },

    # === CỘT 2: ĐỐI TÁC, DANH MỤC & HÀNG HÓA (5 BẢNG) ===
    "LoaiHang": {
        "col": 2, "w": 280,
        "fields": [
            ("_id", "ObjectId"),
            ("MaLoai", "String"),
            ("TenLoai", "String"),
            ("MoTa", "String"),
            ("TrangThai", "String")
        ]
    },
    "NhaCungCap": {
        "col": 2, "w": 280,
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
        "col": 2, "w": 280,
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
        "col": 2, "w": 280,
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
        "col": 2, "w": 280,
        "fields": [
            ("_id", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuongTon", "Number"),
            ("SoLuong", "Number"),
            ("NgayCapNhat", "String"),
            ("updatedAt", "Date")
        ]
    },

    # === CỘT 3: MUA HÀNG & NHẬP KHO (4 BẢNG) ===
    "DonDatHang": {
        "col": 3, "w": 280,
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
        "col": 3, "w": 280,
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
        "col": 3, "w": 280,
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
        "col": 3, "w": 280,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPN", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },

    # === CỘT 4: BÁN HÀNG, HÓA ĐƠN & XUẤT KHO (6 BẢNG) ===
    "DonHang": {
        "col": 4, "w": 280,
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
        "col": 4, "w": 280,
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
        "col": 4, "w": 280,
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
        "col": 4, "w": 280,
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
        "col": 4, "w": 280,
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
        "col": 4, "w": 280,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPX", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },

    # === CỘT 5: KIỂM KÊ, ĐIỀU CHỈNH & ĐỔI TRẢ (5 BẢNG) ===
    "KiemKe": {
        "col": 5, "w": 280,
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
        "col": 5, "w": 280,
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
        "col": 5, "w": 280,
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
        "col": 5, "w": 280,
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
        "col": 5, "w": 280,
        "fields": [
            ("_id", "ObjectId"),
            ("MaPTH", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("SoLuong", "Number"),
            ("DonGia", "Number"),
            ("ThanhTien", "Number")
        ]
    },

    # === CỘT 6: TÀI CHÍNH, QUỸ, CÔNG NỢ & KHUYẾN MÃI (6 BẢNG) ===
    "CongNo": {
        "col": 6, "w": 280,
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
        "col": 6, "w": 280,
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
        "col": 6, "w": 280,
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
        "col": 6, "w": 280,
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
        "col": 6, "w": 280,
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
        "col": 6, "w": 280,
        "fields": [
            ("_id", "ObjectId"),
            ("MaKM", "ObjectId"),
            ("MaSP", "ObjectId"),
            ("createdAt", "Date")
        ]
    }
}

# Tọa độ X cho 6 cột
COL_X = {
    1: 70,
    2: 450,
    3: 830,
    4: 1210,
    5: 1590,
    6: 1970
}

# Tính toán vị trí Y xếp tầng trong từng cột
col_current_y = {1: 70, 2: 70, 3: 70, 4: 70, 5: 70, 6: 70}

for name, t in TABLES.items():
    col = t["col"]
    t["x"] = COL_X[col]
    t["y"] = col_current_y[col]
    t["h"] = 28 + len(t["fields"]) * 20
    col_current_y[col] += t["h"] + 24  # Khoảng cách giữa các bảng cùng cột

    t["cx"] = t["x"] + t["w"] / 2
    t["cy"] = t["y"] + t["h"] / 2
    t["top"] = (t["cx"], t["y"])
    t["bottom"] = (t["cx"], t["y"] + t["h"])
    t["left"] = (t["x"], t["cy"])
    t["right"] = (t["x"] + t["w"], t["cy"])


# Danh sách liên kết kèm ĐIỀU KIỆN RÀNG BUỘC (Condition)
RELATIONS = [
    # 1. Cột 1
    {"from": "VaiTro", "to": "NhanVien", "cond": "MaVaiTro", "p1": "bottom", "p2": "top"},
    {"from": "Users", "to": "NhanVien", "cond": "username", "p1": "bottom", "p2": "top"},
    {"from": "Users", "to": "AuditLogs", "cond": "userId = _id", "p1": "bottom", "p2": "top"},

    # 2. Cột 2
    {"from": "LoaiHang", "to": "SanPham", "cond": "MaLoai = _id", "p1": "bottom", "p2": "top"},
    {"from": "SanPham", "to": "TonKho", "cond": "MaSP = _id (1-1)", "p1": "bottom", "p2": "top"},

    # 3. Cột 3 (Mua hàng)
    {"from": "NhaCungCap", "to": "DonDatHang", "cond": "MaNCC = _id", "p1": "right", "p2": "left"},
    {"from": "DonDatHang", "to": "CT_DonDatHang", "cond": "MaDDH = _id", "p1": "bottom", "p2": "top"},
    {"from": "DonDatHang", "to": "PhieuNhap", "cond": "MaDDH = _id", "p1": "bottom", "p2": "top"},
    {"from": "PhieuNhap", "to": "CT_PhieuNhap", "cond": "MaPN = _id", "p1": "bottom", "p2": "top"},

    # 4. Cột 4 (Bán hàng)
    {"from": "KhachHang", "to": "DonHang", "cond": "MaKH = _id", "p1": "right", "p2": "left"},
    {"from": "DonHang", "to": "CT_DonHang", "cond": "MaDH = _id", "p1": "bottom", "p2": "top"},
    {"from": "DonHang", "to": "HoaDon", "cond": "MaDH = _id (1-1)", "p1": "bottom", "p2": "top"},
    {"from": "HoaDon", "to": "CT_HoaDon", "cond": "MaHD = _id", "p1": "bottom", "p2": "top"},
    {"from": "DonHang", "to": "PhieuXuat", "cond": "MaDH = _id", "p1": "bottom", "p2": "top"},
    {"from": "PhieuXuat", "to": "CT_PhieuXuat", "cond": "MaPX = _id", "p1": "bottom", "p2": "top"},

    # 5. Cột 5 (Kiểm kê & Đổi trả)
    {"from": "KiemKe", "to": "CT_KiemKe", "cond": "MaKK = _id", "p1": "bottom", "p2": "top"},
    {"from": "KiemKe", "to": "DieuChinhKho", "cond": "MaKK = _id", "p1": "bottom", "p2": "top"},
    {"from": "DonHang", "to": "PhieuTraHang", "cond": "MaDH = _id", "p1": "right", "p2": "left"},
    {"from": "PhieuTraHang", "to": "CT_PhieuTraHang", "cond": "MaPTH = _id", "p1": "bottom", "p2": "top"},

    # 6. Cột 6 (Tài chính & Khuyến mãi)
    {"from": "PhieuNhap", "to": "CongNo", "cond": "MaPN = _id (Nợ NCC)", "p1": "right", "p2": "left"},
    {"from": "HoaDon", "to": "CongNo", "cond": "MaHD = _id (Nợ KH)", "p1": "right", "p2": "left"},
    {"from": "HoaDon", "to": "ThanhToan", "cond": "MaHD = _id", "p1": "right", "p2": "left"},
    {"from": "HoaDon", "to": "PhieuThu", "cond": "ChungTuGoc = MaHD", "p1": "right", "p2": "left"},
    {"from": "PhieuNhap", "to": "PhieuChi", "cond": "ChungTuGoc = MaPN", "p1": "right", "p2": "left"},
    {"from": "KhuyenMai", "to": "CT_KhuyenMai", "cond": "MaKM = _id", "p1": "bottom", "p2": "top"},

    # 7. SanPham liên kết chi tiết
    {"from": "SanPham", "to": "CT_DonDatHang", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_PhieuNhap", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_DonHang", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_HoaDon", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_PhieuXuat", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_KiemKe", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_PhieuTraHang", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
    {"from": "SanPham", "to": "CT_KhuyenMai", "cond": "MaSP = _id", "p1": "right", "p2": "left"},
]


def generate_svg():
    width = 2320
    height = max(col_current_y.values()) + 60

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#ffffff; font-family: Arial, Helvetica, sans-serif;">',
        '<defs>',
        '  <!-- Đầu mũi tên tam giác đen đặc chuẩn bản vẽ kỹ thuật -->',
        '  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">',
        '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000" />',
        '  </marker>',
        '  <!-- Ký hiệu nguồn gạch vuông / cộng -->',
        '  <marker id="src-bar" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
        '    <line x1="2" y1="1" x2="2" y2="9" stroke="#000000" stroke-width="2.5" />',
        '  </marker>',
        '</defs>',
        '<!-- Header Title Banner -->',
        '<text x="50%" y="36" font-size="20" font-weight="bold" text-anchor="middle" fill="#000000">Sơ đồ cơ sở dữ liệu MongoDB hoàn thiện thực tế - 32 Collections (Kèm điều kiện liên kết)</text>',
        '<!-- RELATIONSHIP LINES WITH CONDITIONS -->'
    ]

    for rel in RELATIONS:
        t1 = TABLES[rel["from"]]
        t2 = TABLES[rel["to"]]
        p1 = t1[rel["p1"]]
        p2 = t2[rel["p2"]]
        cond = rel.get("cond", "")

        # Orthogonal path
        points = [p1]
        if rel["p1"] == "bottom" and rel["p2"] == "top":
            mid_y = (p1[1] + p2[1]) / 2
            points.append((p1[0], mid_y))
            points.append((p2[0], mid_y))
        elif rel["p1"] == "right" and rel["p2"] == "left":
            mid_x = (p1[0] + p2[0]) / 2
            points.append((mid_x, p1[1]))
            points.append((mid_x, p2[1]))
        elif rel["p1"] == "right" and rel["p2"] == "top":
            points.append((p2[0], p1[1]))
        elif rel["p1"] == "bottom" and rel["p2"] == "left":
            points.append((p1[0], p2[1]))
        else:
            mid_x = (p1[0] + p2[0]) / 2
            points.append((mid_x, p1[1]))
            points.append((mid_x, p2[1]))
        points.append(p2)

        d_str = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
        for pt in points[1:]:
            d_str += f" L {pt[0]:.1f} {pt[1]:.1f}"

        svg.append(f'<path d="{d_str}" fill="none" stroke="#000000" stroke-width="1.2" marker-start="url(#src-bar)" marker-end="url(#arrow)"/>')

        # Condition badge
        if cond:
            # Lấy điểm giữa của đoạn thẳng
            mid_idx = len(points) // 2
            mp = points[mid_idx]
            cond_w = len(cond) * 6.5 + 10
            svg.append(
                f'<rect x="{mp[0] - cond_w/2}" y="{mp[1] - 8}" width="{cond_w}" height="16" fill="#ffffff" stroke="#000000" stroke-width="0.8" rx="2" />'
                f'<text x="{mp[0]}" y="{mp[1] + 3.5}" font-size="9" font-weight="bold" text-anchor="middle" fill="#000000">{cond}</text>'
            )

    svg.append('<!-- 32 TABLE BOXES -->')

    for name, t in TABLES.items():
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        col1_w = int(w * 0.52)

        svg.append(f'<!-- Table: {name} -->')
        svg.append(f'<g id="tbl_{name}">')
        # Thân bảng viền đen nền trắng
        svg.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="#000000" stroke-width="1.6"/>')
        # Header đen đặc
        svg.append(f'  <rect x="{x}" y="{y}" width="{w}" height="26" fill="#000000" stroke="#000000" stroke-width="1.6"/>')
        # Tiêu đề bảng chữ trắng in đậm
        svg.append(f'  <text x="{x + w/2}" y="{y + 18}" font-size="13" font-weight="bold" text-anchor="middle" fill="#ffffff">{name}</text>')
        # Đường kẻ dọc phân cách 2 cột
        svg.append(f'  <line x1="{x + col1_w}" y1="{y + 26}" x2="{x + col1_w}" y2="{y + h}" stroke="#000000" stroke-width="1.0"/>')

        # Từng dòng trường
        for idx, (fname, ftype) in enumerate(t["fields"]):
            row_y = y + 26 + (idx * 20)
            # Đường kẻ ngang giữa các dòng
            if idx > 0:
                svg.append(f'  <line x1="{x}" y1="{row_y}" x2="{x + w}" y2="{row_y}" stroke="#000000" stroke-width="0.7"/>')

            # Tên trường
            svg.append(f'  <text x="{x + 8}" y="{row_y + 14}" font-size="11" font-weight="{"bold" if fname=="_id" else "normal"}" fill="#000000">{fname}</text>')
            # Kiểu dữ liệu MongoDB
            svg.append(f'  <text x="{x + col1_w + 8}" y="{row_y + 14}" font-size="10.5" fill="#000000">{ftype}</text>')

        svg.append('</g>')

    svg.append('</svg>')
    return "\n".join(svg)


def generate_drawio():
    xml = [
        '<mxfile host="app.diagrams.net" modified="2026-10-07T17:55:00.000Z" agent="Antigravity" version="21.0.0" type="device">',
        '  <diagram id="BabyShop_Mongo_32" name="MongoDB_32_Collections">',
        '    <mxGraphModel dx="2600" dy="1800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2600" pageHeight="1800" background="#ffffff">',
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
        for fn, ft in t["fields"]:
            field_rows += f"<tr><td style='border:1px solid #000;padding:2px 6px;'><b>{fn}</b></td><td style='border:1px solid #000;padding:2px 6px;'>{ft}</td></tr>"

        html_val = f"&lt;table style='width:100%;border-collapse:collapse;font-size:11px;'&gt;&lt;tr&gt;&lt;th colspan='2' style='background:#000000;color:#ffffff;border:1px solid #000;padding:4px;'&gt;{name}&lt;/th&gt;&lt;/tr&gt;{field_rows}&lt;/table&gt;"

        xml.append(
            f'        <mxCell id="{t_id}" value="{html_val}" style="text;html=1;whiteSpace=wrap;overflow=hidden;rounded=0;shadow=0;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">'
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
            f'        <mxCell id="{edge_id}" value="{rel.get("cond", "")}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=ERmandOne;startFill=0;endArrow=block;endFill=1;strokeColor=#000000;strokeWidth=1.2;" edge="1" parent="1" source="{src_id}" target="{trg_id}">'
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

    # 3. Ghi HTML
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ Đồ ERD MongoDB Thực Tế - 32 Collections</title>
  <style>
    body {{
      margin: 0;
      padding: 16px;
      font-family: Arial, sans-serif;
      background: #f8fafc;
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
    .canvas {{
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 16px;
      overflow: auto;
    }}
    svg {{
      min-width: 1800px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h2 style="margin:0; font-size:16px;">SƠ ĐỒ ERD CƠ SỞ DỮ LIỆU MONGODB THỰC TẾ (32 COLLECTIONS)</h2>
      <p style="margin:4px 0 0; font-size:12px; color:#cbd5e1;">Chuẩn phong cách tài liệu gốc: Header đen chữ trắng • Kiểu dữ liệu BSON/MongoDB • Kèm nhãn điều kiện liên kết</p>
    </div>
    <div>
      <a href="so_do_erd_mongodb_32_bang.svg" download class="btn btn-svg">Tải SVG</a>
      <a href="so_do_erd_mongodb_32_bang.png" download class="btn btn-png">Tải PNG Siêu Nét</a>
    </div>
  </div>
  <div class="canvas">
    {svg_content}
  </div>
</body>
</html>"""

    for p in [ROOT / "so_do_erd_mongodb_32_bang.html", DB_DIR / "so_do_erd_mongodb_32_bang.html"]:
        p.write_text(html_content, encoding="utf-8")
    print("✅ Đã ghi file HTML 32 bảng")

    # 4. Xuất PNG chất lượng cao
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    png_path = ROOT / "so_do_erd_mongodb_32_bang.png"
    html_target = ROOT / "so_do_erd_mongodb_32_bang.html"

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--window-size=2400,1650",
        f"--screenshot={png_path}",
        str(html_target.resolve().as_uri())
    ]
    try:
        subprocess.run(cmd, check=True, timeout=15)
        print(f"✅ Đã xuất PNG sắc nét 32 bảng: {png_path} ({png_path.stat().st_size} bytes)")
        (DB_DIR / "so_do_erd_mongodb_32_bang.png").write_bytes(png_path.read_bytes())
    except Exception as e:
        print(f"Lỗi chụp màn hình Edge: {e}")


if __name__ == "__main__":
    main()
