# -*- coding: utf-8 -*-
import sys
import re
import docx

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('D:/BabyShop/Nhom1_BCBTL.docx')

code_terms = [
    'CT_DonDatHang', 'CT_PhieuNhap', 'CT_DonHang', 'CT_HoaDon', 'CT_PhieuXuat',
    'CT_PhieuTraHang', 'CT_KiemKe', 'CT_KhuyenMai', 'DieuChinhKho', 'DonDatHang',
    'PhieuTraHang', 'NhaCungCap', 'KhachHang', 'AuditLogs', 'PhieuNhap', 'PhieuXuat',
    'KhuyenMai', 'ThanhToan', 'NhanVien', 'LoaiHang', 'PhieuThu', 'PhieuChi',
    'Counters', '_metadata', 'SanPham', 'DonHang', 'HoaDon', 'TonKho', 'TheKho',
    'KiemKe', 'VaiTro', 'Users', 'CongNo', 'SoQuy',
    'passwordHash', 'SoLuongTon', 'SoHoaDonNCC', 'NgayHoaDonNCC', 'DaThanhToan',
    'LoaiPhieuXuat', 'NgayPhatSinh', 'HanThanhToan', 'SoLanSuDung', 'GioiHanSuDung',
    'HinhThucThanhToan', 'TienThueGTGT', 'PROTECTED_VOUCHERS', 'baby_shop_management',
    'ensure-indexes.js', 'init_database.js', 'mongodb.js', 'adjustStock', 'ReturnPage',
    'AdminPage', 'ReportPage', 'ObjectId', 'String', 'Number', 'Boolean', 'Array',
    'Object', 'Mixed', '$inc', '$gte', '$set', '$lookup', '_id', 'MaDDH', 'MaPTH',
    'MaNCC', 'MaHD', 'MaDH', 'MaPN', 'MaPX', 'MaPT', 'MaPC', 'MaKK', 'MaKM', 'MaNV',
    'MaSP', 'MaKH', 'MaCN', 'MaTT', 'MaDC', 'MaVaiTro', 'MaKey', 'MaLoai', 'SoLuong',
    'DonGia', 'ThanhTien', 'GiaVon', 'ThueSuat', 'TienThue', 'createdAt', 'updatedAt',
    'username', 'fullName', 'details', 'stock', 'HanSuDung', 'ConNo'
]

not_courier_count = 0
for pi, p in enumerate(doc.paragraphs):
    for r in p.runs:
        if r.font.name != 'Courier New':
            for term in code_terms:
                if re.search(r'\b' + re.escape(term) + r'\b', r.text):
                    not_courier_count += 1
                    if not_courier_count <= 20:
                        print(f"P{pi}: term '{term}' in run '{r.text[:60]}'")
                    break
print(f"Total occurrences of code terms in non-Courier runs: {not_courier_count}")
