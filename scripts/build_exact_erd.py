import os
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Thư mục đích
ROOT = Path("D:/BabyShop")
DB_DIR = ROOT / "database"

# Dữ liệu 25 bảng chính xác từ ảnh của người dùng và database/schema.sql
TABLES = {
    "DonDat_Hang": {
        "x": 80, "y": 70, "w": 230,
        "fields": [
            ("MaDDH", "INTEGER"),
            ("MaNCC", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayDat", "DATE"),
            ("TrangThai", "VARCHAR(20)"),
            ("TongTien", "DECIMAL(10,2)")
        ]
    },
    "VaiTro": {
        "x": 680, "y": 70, "w": 190,
        "fields": [
            ("MaVT", "INTEGER"),
            ("TenVT", "VARCHAR")
        ]
    },
    "NhanVien": {
        "x": 1150, "y": 70, "w": 230,
        "fields": [
            ("MaNV", "INTEGER"),
            ("MaVT", "INTEGER"),
            ("HoTen", "VARCHAR(100)"),
            ("ChucVu", "VARCHAR(50)"),
            ("SDT", "VARCHAR(15)"),
            ("TrangThai", "VARCHAR(20)")
        ]
    },
    "PhieuTraHang": {
        "x": 1620, "y": 70, "w": 230,
        "fields": [
            ("MaPTH", "INTEGER"),
            ("MaDH", "INTEGER"),
            ("MaKH", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayTra", "DATE"),
            ("LyDo", "TEXT"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "KhachHang": {
        "x": 2100, "y": 70, "w": 230,
        "fields": [
            ("MaKH", "INTEGER"),
            ("HoTen", "VARCHAR(100)"),
            ("SDT", "VARCHAR(15)"),
            ("Email", "VARCHAR(100)"),
            ("DiaChi", "VARCHAR(200)"),
            ("DiemTichLuy", "INTEGER")
        ]
    },
    "NhaCungCap": {
        "x": 80, "y": 290, "w": 230,
        "fields": [
            ("MaNCC", "INTEGER"),
            ("TenNCC", "VARCHAR(100)"),
            ("SDT", "VARCHAR(15)"),
            ("DiaChi", "VARCHAR(200)"),
            ("Email", "VARCHAR(100)")
        ]
    },
    "PhieuNhap": {
        "x": 890, "y": 250, "w": 230,
        "fields": [
            ("MaPN", "INTEGER"),
            ("MaDDH", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayNhap", "DATE"),
            ("TrangThai", "VARCHAR(30)"),
            ("TongTien", "DECIMAL(10,2)")
        ]
    },
    "PhieuXuat": {
        "x": 1620, "y": 280, "w": 230,
        "fields": [
            ("MaPX", "INTEGER"),
            ("MaDH", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayXuat", "DATE"),
            ("LyDoXuat", "VARCHAR(200)"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "DonHang": {
        "x": 2100, "y": 290, "w": 230,
        "fields": [
            ("MaDH", "INTEGER"),
            ("MaKH", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayDat", "DATE"),
            ("TongTien", "DECIMAL(10,2)"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "CT_DonDathang": {
        "x": 390, "y": 420, "w": 220,
        "fields": [
            ("MaDDH", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuong", "INTEGER"),
            ("DonGia", "DECIMAL(10,2)"),
            ("ThanhTien", "DECIMAL(10,2)")
        ]
    },
    "KiemKe": {
        "x": 1000, "y": 430, "w": 210,
        "fields": [
            ("MaKK", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayKiemKe", "DATE"),
            ("GhiChu", "TEXT")
        ]
    },
    "CT_PhieuTraHang": {
        "x": 1880, "y": 380, "w": 230,
        "fields": [
            ("MaPTH", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuong", "INTEGER"),
            ("DonGia", "DECIMAL(10,2)"),
            ("ThanhTien", "DECIMAL(10,2)"),
            ("LyDo", "TEXT")
        ]
    },
    "CT_PhieuXuat": {
        "x": 1620, "y": 480, "w": 220,
        "fields": [
            ("MaPX", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuong", "INTEGER"),
            ("DonGia", "DECIMAL(10,2)"),
            ("ThanhTien", "DECIMAL(10,2)")
        ]
    },
    "CongNo": {
        "x": 80, "y": 550, "w": 240,
        "fields": [
            ("MaCN", "INTEGER"),
            ("MaNCC", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayPhatSinh", "DATE"),
            ("SoTien", "DECIMAL(10,2)"),
            ("SoTienDaTra", "DECIMAL(10,2)"),
            ("SoTienConLai", "DECIMAL(10,2)"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "CT_KiemKe": {
        "x": 980, "y": 600, "w": 250,
        "fields": [
            ("MaKK", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuongHeThong", "INTEGER"),
            ("SoLuongThucTe", "INTEGER"),
            ("ChenhLech", "INTEGER")
        ]
    },
    "HoaDon": {
        "x": 1450, "y": 580, "w": 230,
        "fields": [
            ("MaHD", "INTEGER"),
            ("MaDH", "INTEGER"),
            ("MaNV", "INTEGER"),
            ("NgayLap", "DATE"),
            ("TongTien", "DECIMAL(10,2)"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "ThanhToan": {
        "x": 1850, "y": 650, "w": 230,
        "fields": [
            ("MaTT", "INTEGER"),
            ("MaHD", "INTEGER"),
            ("PhuongThuc", "VARCHAR(50)"),
            ("SoTien", "DECIMAL(10,2)"),
            ("NgayThanhToan", "DATE"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "LoaiHang": {
        "x": 100, "y": 820, "w": 220,
        "fields": [
            ("MaLoai", "INTEGER"),
            ("TenLoai", "VARCHAR(100)"),
            ("MoTa", "TEXT")
        ]
    },
    "SanPham": {
        "x": 520, "y": 750, "w": 250,
        "fields": [
            ("MaSP", "INTEGER"),
            ("MaLoai", "INTEGER"),
            ("TenSP", "VARCHAR(100)"),
            ("DonViTinh", "VARCHAR(50)"),
            ("GiaNhap", "DECIMAL(10,2)"),
            ("GiaBan", "DECIMAL(10,2)"),
            ("HanSuDung", "DATE"),
            ("TrangThai", "VARCHAR(20)")
        ]
    },
    "KhuyenMai": {
        "x": 1330, "y": 790, "w": 240,
        "fields": [
            ("MaKM", "INTEGER"),
            ("TenKM", "VARCHAR(100)"),
            ("NgayBatDau", "DATE"),
            ("NgayKetThuc", "DATE"),
            ("PhanTramGiam", "(5,2)"),
            ("DieuKienApDung", "VARCHAR(200)"),
            ("TrangThai", "VARCHAR(30)")
        ]
    },
    "CT_DonHang": {
        "x": 2040, "y": 820, "w": 230,
        "fields": [
            ("MaDH", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuong", "INTEGER"),
            ("DonGia", "DECIMAL(10,2)"),
            ("GiamGia", "DECIMAL(10,2)"),
            ("ThanhTien", "DECIMAL(10,2)")
        ]
    },
    "TonKho": {
        "x": 100, "y": 1020, "w": 220,
        "fields": [
            ("MaSP", "INTEGER"),
            ("SoLuongTon", "INTEGER"),
            ("NgayCapNhat", "DATE")
        ]
    },
    "CT_PhieuNhap": {
        "x": 520, "y": 1040, "w": 230,
        "fields": [
            ("MaPN", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuong", "INTEGER"),
            ("DonGia", "DECIMAL(10,2)"),
            ("ThanhTien", "(10,2)")
        ]
    },
    "CT_KhuyenMai": {
        "x": 1330, "y": 1040, "w": 230,
        "fields": [
            ("MaKM", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("GiaTriGiam", "DECIMAL(10,2)")
        ]
    },
    "CT_HoaDon": {
        "x": 1720, "y": 1000, "w": 230,
        "fields": [
            ("MaHD", "INTEGER"),
            ("MaSP", "INTEGER"),
            ("SoLuong", "INTEGER"),
            ("DonGia", "DECIMAL(10,2)"),
            ("GiamGia", "DECIMAL(10,2)"),
            ("ThanhTien", "DECIMAL(10,2)")
        ]
    }
}

# Tính chiều cao và cổng kết nối cho từng bảng
for name, t in TABLES.items():
    t["h"] = 30 + len(t["fields"]) * 22
    t["cx"] = t["x"] + t["w"] / 2
    t["cy"] = t["y"] + t["h"] / 2
    t["top"] = (t["cx"], t["y"])
    t["bottom"] = (t["cx"], t["y"] + t["h"])
    t["left"] = (t["x"], t["cy"])
    t["right"] = (t["x"] + t["w"], t["cy"])

# Danh sách quan hệ chuẩn theo ảnh gốc
RELATIONS = [
    # (Bảng 1, Bảng n, Điểm ra (t1), Điểm vào (t2), Các điểm bẻ góc nếu cần)
    {"from": "VaiTro", "to": "NhanVien", "p1": "right", "p2": "left", "label": ""},
    {"from": "NhaCungCap", "to": "DonDat_Hang", "p1": "top", "p2": "bottom", "label": ""},
    {"from": "NhanVien", "to": "DonDat_Hang", "p1": "left", "p2": "right", "waypoints": [(640, 150), (640, 115)], "label": ""},
    {"from": "DonDat_Hang", "to": "CT_DonDathang", "p1": "bottom", "p2": "top", "waypoints": [(330, 215), (500, 215)], "label": ""},
    {"from": "SanPham", "to": "CT_DonDathang", "p1": "top", "p2": "bottom", "waypoints": [(570, 680), (500, 680)], "label": ""},
    {"from": "DonDat_Hang", "to": "PhieuNhap", "p1": "right", "p2": "left", "waypoints": [(620, 180), (620, 280)], "label": ""},
    {"from": "NhanVien", "to": "PhieuNhap", "p1": "bottom", "p2": "top", "waypoints": [(1200, 220), (1030, 220)], "label": ""},
    {"from": "PhieuNhap", "to": "CT_PhieuNhap", "p1": "bottom", "p2": "top", "waypoints": [(950, 410), (840, 410), (840, 1000), (635, 1000)], "label": ""},
    {"from": "SanPham", "to": "CT_PhieuNhap", "p1": "bottom", "p2": "top", "label": ""},
    {"from": "NhaCungCap", "to": "CongNo", "p1": "bottom", "p2": "top", "label": ""},
    {"from": "NhanVien", "to": "CongNo", "p1": "left", "p2": "top", "waypoints": [(640, 180), (640, 520), (200, 520)], "label": ""},
    {"from": "LoaiHang", "to": "SanPham", "p1": "right", "p2": "left", "label": ""},
    {"from": "SanPham", "to": "TonKho", "p1": "bottom", "p2": "top", "waypoints": [(580, 970), (210, 970)], "label": ""},
    {"from": "NhanVien", "to": "KiemKe", "p1": "bottom", "p2": "top", "waypoints": [(1260, 230), (1105, 230)], "label": ""},
    {"from": "KiemKe", "to": "CT_KiemKe", "p1": "bottom", "p2": "top", "label": "1-n"},
    {"from": "SanPham", "to": "CT_KiemKe", "p1": "right", "p2": "left", "waypoints": [(880, 800), (880, 660)], "label": ""},
    {"from": "KhachHang", "to": "DonHang", "p1": "bottom", "p2": "top", "label": ""},
    {"from": "NhanVien", "to": "DonHang", "p1": "right", "p2": "left", "waypoints": [(1450, 120), (1450, 310), (2050, 310)], "label": ""},
    {"from": "DonHang", "to": "CT_DonHang", "p1": "bottom", "p2": "top", "label": ""},
    {"from": "SanPham", "to": "CT_DonHang", "p1": "right", "p2": "left", "waypoints": [(920, 850), (920, 950), (2000, 950), (2000, 880)], "label": ""},
    {"from": "DonHang", "to": "HoaDon", "p1": "left", "p2": "right", "waypoints": [(2050, 350), (2050, 610), (1700, 610)], "label": ""},
    {"from": "NhanVien", "to": "HoaDon", "p1": "bottom", "p2": "top", "waypoints": [(1280, 230), (1540, 230)], "label": ""},
    {"from": "HoaDon", "to": "CT_HoaDon", "p1": "bottom", "p2": "top", "waypoints": [(1565, 750), (1835, 750)], "label": ""},
    {"from": "SanPham", "to": "CT_HoaDon", "p1": "right", "p2": "left", "waypoints": [(900, 860), (900, 970), (1680, 970), (1680, 1050)], "label": ""},
    {"from": "HoaDon", "to": "ThanhToan", "p1": "right", "p2": "left", "label": ""},
    {"from": "DonHang", "to": "PhieuXuat", "p1": "left", "p2": "right", "label": ""},
    {"from": "NhanVien", "to": "PhieuXuat", "p1": "right", "p2": "top", "waypoints": [(1420, 150), (1735, 150)], "label": ""},
    {"from": "PhieuXuat", "to": "CT_PhieuXuat", "p1": "bottom", "p2": "top", "label": ""},
    {"from": "SanPham", "to": "CT_PhieuXuat", "p1": "right", "p2": "left", "waypoints": [(900, 820), (900, 530)], "label": ""},
    {"from": "DonHang", "to": "PhieuTraHang", "p1": "top", "p2": "right", "waypoints": [(2160, 260), (1950, 260), (1950, 150)], "label": ""},
    {"from": "KhachHang", "to": "PhieuTraHang", "p1": "left", "p2": "right", "label": ""},
    {"from": "NhanVien", "to": "PhieuTraHang", "p1": "right", "p2": "left", "label": ""},
    {"from": "PhieuTraHang", "to": "CT_PhieuTraHang", "p1": "bottom", "p2": "top", "waypoints": [(1735, 260), (1995, 260)], "label": ""},
    {"from": "SanPham", "to": "CT_PhieuTraHang", "p1": "right", "p2": "left", "waypoints": [(880, 810), (880, 440)], "label": ""},
    {"from": "KhuyenMai", "to": "CT_KhuyenMai", "p1": "bottom", "p2": "top", "label": ""},
    {"from": "SanPham", "to": "KhuyenMai", "p1": "right", "p2": "left", "label": ""},
    {"from": "SanPham", "to": "CT_KhuyenMai", "p1": "bottom", "p2": "left", "waypoints": [(660, 970), (1280, 970), (1280, 1070)], "label": ""},
]


def generate_svg():
    width = 2460
    height = 1260

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#ffffff; font-family: Arial, Helvetica, sans-serif;">',
        '<defs>',
        '  <!-- Grid Pattern -->',
        '  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">',
        '    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f2f5" stroke-width="0.8"/>',
        '  </pattern>',
        '  <!-- Crow foot markers -->',
        '  <marker id="crow-end" viewBox="0 0 24 24" refX="22" refY="12" markerWidth="14" markerHeight="14" orient="auto">',
        '    <path d="M 2 4 L 22 12 L 2 20 M 2 12 L 22 12" fill="none" stroke="#222" stroke-width="1.8" />',
        '    <circle cx="6" cy="12" r="3.5" fill="#fff" stroke="#222" stroke-width="1.6" />',
        '  </marker>',
        '  <marker id="one-start" viewBox="0 0 16 16" refX="2" refY="8" markerWidth="12" markerHeight="12" orient="auto">',
        '    <line x1="6" y1="2" x2="6" y2="14" stroke="#222" stroke-width="1.8" />',
        '    <line x1="12" y1="2" x2="12" y2="14" stroke="#222" stroke-width="1.8" />',
        '  </marker>',
        '  <marker id="circle-end" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="10" markerHeight="10" orient="auto">',
        '    <circle cx="8" cy="8" r="4.5" fill="#fff" stroke="#222" stroke-width="1.8" />',
        '  </marker>',
        '</defs>',
        '<!-- Grid background -->',
        f'<rect width="{width}" height="{height}" fill="url(#grid)"/>',
        '<!-- Outer Border like draw.io canvas selection -->',
        f'<rect x="20" y="20" width="{width-40}" height="{height-40}" fill="none" stroke="#777777" stroke-width="1.5" />',
        '<circle cx="20" cy="20" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="{width-20}" cy="20" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="20" cy="{height-20}" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="{width-20}" cy="{height-20}" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="{width//2}" cy="20" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="{width//2}" cy="{height-20}" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="20" cy="{height//2}" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        f'<circle cx="{width-20}" cy="{height//2}" r="5" fill="#fff" stroke="#555" stroke-width="2"/>',
        '<!-- RELATIONSHIP LINES -->'
    ]

    # Vẽ các đường nối
    for rel in RELATIONS:
        t1 = TABLES[rel["from"]]
        t2 = TABLES[rel["to"]]
        p1 = t1[rel["p1"]]
        p2 = t2[rel["p2"]]

        points = [p1]
        if "waypoints" in rel:
            points.extend(rel["waypoints"])
        else:
            # Orthogonal routing tự động
            if rel["p1"] in ["left", "right"] and rel["p2"] in ["left", "right"]:
                mid_x = (p1[0] + p2[0]) / 2
                points.append((mid_x, p1[1]))
                points.append((mid_x, p2[1]))
            elif rel["p1"] in ["top", "bottom"] and rel["p2"] in ["top", "bottom"]:
                mid_y = (p1[1] + p2[1]) / 2
                points.append((p1[0], mid_y))
                points.append((p2[0], mid_y))
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
            f'<path d="{d_str}" fill="none" stroke="#2b2b2b" stroke-width="1.3" '
            f'marker-start="url(#one-start)" marker-end="url(#crow-end)"/>'
        )
        if rel.get("label"):
            mid_pt = points[len(points)//2]
            svg_lines.append(
                f'<rect x="{mid_pt[0]-16}" y="{mid_pt[1]-10}" width="32" height="16" fill="#ffffff" stroke="#ccc" stroke-width="0.5"/>'
                f'<text x="{mid_pt[0]}" y="{mid_pt[1]+3}" font-size="10" text-anchor="middle" fill="#333">{rel["label"]}</text>'
            )

    svg_lines.append('<!-- TABLE BOXES -->')

    # Vẽ từng bảng
    for name, t in TABLES.items():
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        col1_w = int(w * 0.46)

        svg_lines.append(f'<!-- Table {name} -->')
        svg_lines.append(f'<g id="table_{name}">')
        # Thân bảng
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.4"/>')
        # Tiêu đề bảng
        svg_lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="28" fill="#ffffff" stroke="#1e1e1e" stroke-width="1.4"/>')
        svg_lines.append(f'  <text x="{x + w/2}" y="{y + 19}" font-size="13" font-weight="bold" text-anchor="middle" fill="#111827">{name}</text>')
        # Đường chia cột dọc
        svg_lines.append(f'  <line x1="{x + col1_w}" y1="{y + 28}" x2="{x + col1_w}" y2="{y + h}" stroke="#2b2b2b" stroke-width="1.0"/>')

        # Từng dòng thuộc tính
        for idx, (fname, ftype) in enumerate(t["fields"]):
            row_y = y + 28 + (idx * 22)
            # Đường kẻ ngang giữa các dòng (nhạt)
            if idx > 0:
                svg_lines.append(f'  <line x1="{x}" y1="{row_y}" x2="{x + w}" y2="{row_y}" stroke="#e5e7eb" stroke-width="0.8"/>')
            # Tên trường
            svg_lines.append(f'  <text x="{x + 8}" y="{row_y + 15}" font-size="11.5" font-weight="500" fill="#111827">{fname}</text>')
            # Kiểu dữ liệu
            svg_lines.append(f'  <text x="{x + col1_w + 8}" y="{row_y + 15}" font-size="11" fill="#374151">{ftype}</text>')

        svg_lines.append('</g>')

    svg_lines.append('</svg>')
    return "\n".join(svg_lines)


def generate_drawio_xml():
    # Tạo file draw.io XML chuẩn mực để mở trực tiếp trong app Draw.io hoặc diagrams.net
    xml = [
        '<mxfile host="app.diagrams.net" modified="2026-10-07T17:40:00.000Z" agent="Antigravity" version="21.0.0" type="device">',
        '  <diagram id="BabyShopERD" name="ERD_25_Bang_Chuan">',
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

        # Format rows
        field_rows = ""
        for fn, ft in t["fields"]:
            field_rows += f"<tr><td style='border:1px solid #ddd;padding:2px 6px;'>{fn}</td><td style='border:1px solid #ddd;padding:2px 6px;'>{ft}</td></tr>"

        html_val = f"&lt;table style='width:100%;border-collapse:collapse;font-size:11px;'&gt;&lt;tr&gt;&lt;th colspan='2' style='background:#f4f4f4;border:1px solid #333;padding:4px;'&gt;&lt;b&gt;{name}&lt;/b&gt;&lt;/th&gt;&lt;/tr&gt;{field_rows}&lt;/table&gt;"

        xml.append(
            f'        <mxCell id="{t_id}" value="{html_val}" style="text;html=1;whiteSpace=wrap;overflow=hidden;rounded=0;shadow=0;strokeColor=#333333;fillColor=#ffffff;" vertex="1" parent="1">'
        )
        xml.append(
            f'          <mxGeometry x="{t["x"]}" y="{t["y"]}" width="{t["w"]}" height="{t["h"]}" as="geometry"/>'
        )
        xml.append('        </mxCell>')

    for idx, rel in enumerate(RELATIONS):
        cell_id += 1
        edge_id = str(cell_id)
        src_id = table_cell_ids[rel["from"]]
        trg_id = table_cell_ids[rel["to"]]

        xml.append(
            f'        <mxCell id="{edge_id}" value="{rel.get("label", "")}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;strokeColor=#333333;strokeWidth=1.5;" edge="1" parent="1" source="{src_id}" target="{trg_id}">'
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
    drawio_content = generate_drawio_xml()

    # 1. Ghi SVG
    svg_root = ROOT / "so_do_erd_chuan.svg"
    svg_db = DB_DIR / "so_do_erd_chuan.svg"
    svg_root.write_text(svg_content, encoding="utf-8")
    svg_db.write_text(svg_content, encoding="utf-8")
    print(f"✅ Đã tạo SVG: {svg_root} ({len(svg_content)} ký tự)")

    # 2. Ghi Draw.io XML
    drawio_root = ROOT / "so_do_erd_chuan.drawio"
    drawio_db = DB_DIR / "so_do_erd_chuan.drawio"
    drawio_root.write_text(drawio_content, encoding="utf-8")
    drawio_db.write_text(drawio_content, encoding="utf-8")
    print(f"✅ Đã tạo DRAWIO: {drawio_root}")

    # 3. Tạo file HTML tương tác mở trực tiếp bằng trình duyệt
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ Đồ ERD Chuẩn Thực Tế - Baby Shop Management</title>
  <style>
    body {{
      margin: 0;
      padding: 16px;
      font-family: Arial, sans-serif;
      background: #eef2f5;
    }}
    .toolbar {{
      background: #ffffff;
      padding: 12px 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}
    .btn {{
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: bold;
      border: none;
      cursor: pointer;
      margin-left: 8px;
    }}
    .btn-svg {{ background: #10b981; color: white; }}
    .btn-png {{ background: #0284c7; color: white; }}
    .canvas-card {{
      background: #ffffff;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.12);
      padding: 10px;
      overflow: auto;
    }}
    svg {{
      min-width: 1400px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="toolbar">
    <div>
      <h2 style="margin:0; font-size:16px; color:#1e293b;">SƠ ĐỒ ERD CƠ SỞ DỮ LIỆU CHUẨN THỰC TẾ (25 BẢNG LOGIC)</h2>
      <p style="margin:3px 0 0; font-size:12px; color:#64748b;">Khung thiết kế chuẩn Draw.io • 100% Thuộc tính & Kiểu dữ liệu thật • Quan hệ chân quạ (Crow's Foot)</p>
    </div>
    <div>
      <a href="so_do_erd_chuan.svg" download class="btn btn-svg" style="text-decoration:none;">Tải SVG Vector</a>
      <a href="so_do_erd_chuan.png" download class="btn btn-png" style="text-decoration:none;">Tải PNG 4K</a>
    </div>
  </div>
  <div class="canvas-card">
    {svg_content}
  </div>
</body>
</html>"""
    (ROOT / "so_do_erd_chuan.html").write_text(html_content, encoding="utf-8")
    (DB_DIR / "so_do_erd_chuan.html").write_text(html_content, encoding="utf-8")
    print(f"✅ Đã tạo HTML: {ROOT / 'so_do_erd_chuan.html'}")

    # 4. Xuất PNG độ nét cao bằng Edge Headless
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    png_path = ROOT / "so_do_erd_chuan.png"
    html_target = ROOT / "so_do_erd_chuan.html"

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--window-size=2560,1400",
        f"--screenshot={png_path}",
        str(html_target.resolve().as_uri())
    ]
    try:
        subprocess.run(cmd, check=True, timeout=15)
        print(f"✅ Đã xuất PNG chất lượng cao: {png_path} ({png_path.stat().st_size} bytes)")
        # Đồng bộ sang database/
        (DB_DIR / "so_do_erd_chuan.png").write_bytes(png_path.read_bytes())
    except Exception as e:
        print(f"Lỗi chụp màn hình Edge: {e}")


if __name__ == "__main__":
    main()
