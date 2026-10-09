# -*- coding: utf-8 -*-
import sys
import re
import docx
from docx.shared import Pt

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('D:/BabyShop/Nhom1_BCBTL.docx')

CODE_IDENTIFIERS = [
    # Collections
    'CT_DonDatHang', 'CT_PhieuNhap', 'CT_DonHang', 'CT_HoaDon', 'CT_PhieuXuat',
    'CT_PhieuTraHang', 'CT_KiemKe', 'CT_KhuyenMai', 'DieuChinhKho', 'DonDatHang',
    'PhieuTraHang', 'NhaCungCap', 'KhachHang', 'AuditLogs', 'PhieuNhap', 'PhieuXuat',
    'KhuyenMai', 'ThanhToan', 'NhanVien', 'LoaiHang', 'PhieuThu', 'PhieuChi',
    'Counters', '_metadata', 'SanPham', 'DonHang', 'HoaDon', 'TonKho', 'TheKho',
    'KiemKe', 'VaiTro', 'Users', 'CongNo', 'SoQuy', 'CT_*',
    # Field names & methods
    'passwordHash', 'SoLuongTon', 'SoHoaDonNCC', 'NgayHoaDonNCC', 'DaThanhToan',
    'LoaiPhieuXuat', 'NgayPhatSinh', 'HanThanhToan', 'SoLanSuDung', 'GioiHanSuDung',
    'HinhThucThanhToan', 'TienThueGTGT', 'PROTECTED_VOUCHERS', 'baby_shop_management',
    'ensure-indexes.js', 'init_database.js', 'mongodb.js', 'adjustStock', 'ReturnPage',
    'AdminPage', 'ReportPage', 'ObjectId', '$inc', '$gte', '$set', '$lookup', '_id',
    'MaDDH', 'MaPTH', 'MaNCC', 'MaHD', 'MaDH', 'MaPN', 'MaPX', 'MaPT', 'MaPC', 'MaKK',
    'MaKM', 'MaNV', 'MaSP', 'MaKH', 'MaCN', 'MaTT', 'MaDC', 'MaVaiTro', 'MaKey', 'MaLoai',
    'SoLuong', 'DonGia', 'ThanhTien', 'GiaVon', 'ThueSuat', 'TienThue', 'createdAt',
    'updatedAt', 'username', 'fullName', 'details', 'stock', 'HanSuDung', 'ConNo',
    'LoaiCongNo', 'NguoiNopTien', 'NguoiNhanTien', 'ChungTuGoc', 'SoLuongSoSach',
    'SoLuongThucTe', 'ChenhLech', 'QuyenHan', 'LaVaiTroHeThong'
]

escaped_terms = [re.escape(t) for t in CODE_IDENTIFIERS]
code_regex = re.compile(r'(?<![A-Za-z0-9_])(' + '|'.join(escaped_terms) + r')(?![A-Za-z0-9_])')

def format_paragraph_code_words(p):
    # Do not alter headings, captions, or paragraphs containing drawings
    if p.style.name.startswith('Heading') or p.text.startswith('Hình ') or p.text.startswith('Bảng '):
        # Only adjust size of existing Courier New runs if any
        for r in p.runs:
            if r.font.name == 'Courier New':
                r.font.size = Pt(10)
        return False
    
    if p._element.xpath('.//a:blip'):
        return False

    # Check if there is any run needing formatting
    has_courier = any(r.font.name == 'Courier New' for r in p.runs)
    has_regex_match = any(code_regex.search(r.text) for r in p.runs if r.font.name != 'Courier New')

    if not has_courier and not has_regex_match:
        return False

    # Build new runs
    new_runs_data = []
    for r in p.runs:
        if r.font.name == 'Courier New':
            new_runs_data.append((r.text, 'Courier New', Pt(10), r.font.bold, r.font.italic, r.font.color.rgb if r.font.color else None))
        else:
            text = r.text
            if not code_regex.search(text):
                new_runs_data.append((text, r.font.name, r.font.size, r.font.bold, r.font.italic, r.font.color.rgb if r.font.color else None))
            else:
                parts = code_regex.split(text)
                for part in parts:
                    if not part:
                        continue
                    if code_regex.fullmatch(part):
                        new_runs_data.append((part, 'Courier New', Pt(10), True, False, None))
                    else:
                        new_runs_data.append((part, r.font.name, r.font.size, r.font.bold, r.font.italic, r.font.color.rgb if r.font.color else None))

    # Replace runs cleanly in paragraph
    for r in list(p.runs):
        p._p.remove(r._r)
    
    for text, font_name, font_size, bold, italic, color_rgb in new_runs_data:
        new_r = p.add_run(text)
        if font_name:
            new_r.font.name = font_name
        if font_size:
            new_r.font.size = font_size
        if bold is not None:
            new_r.font.bold = bold
        if italic is not None:
            new_r.font.italic = italic
        if color_rgb is not None:
            new_r.font.color.rgb = color_rgb

    return True

# Test on a few paragraphs
changed = 0
for pi, p in enumerate(doc.paragraphs):
    if format_paragraph_code_words(p):
        changed += 1

print(f"Total paragraphs updated with size 10 code words: {changed}")

# Check P30 and P546
print("\nP30 runs:")
for r in doc.paragraphs[30].runs:
    print(f"  {r.text!r} | font={r.font.name} | size={r.font.size.pt if r.font.size else None} | bold={r.font.bold}")

print("\nP546 runs (first 10):")
for r in doc.paragraphs[546].runs[:10]:
    print(f"  {r.text!r} | font={r.font.name} | size={r.font.size.pt if r.font.size else None} | bold={r.font.bold}")
