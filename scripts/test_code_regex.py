# -*- coding: utf-8 -*-
import sys
import re
import docx
from docx.shared import Pt

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('D:/BabyShop/Nhom1_BCBTL.docx')

CODE_IDENTIFIERS = [
    # Collections (sorted by length descending to match longest first)
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

# Build regex pattern with word boundaries (except for terms with special chars like CT_*, _metadata, _id, $inc, $gte, etc.)
escaped_terms = [re.escape(t) for t in CODE_IDENTIFIERS]
code_regex = re.compile(r'(?<![A-Za-z0-9_])(' + '|'.join(escaped_terms) + r')(?![A-Za-z0-9_])')

print(f"Loaded {len(CODE_IDENTIFIERS)} code identifiers.")
total_p_matches = 0
for pi, p in enumerate(doc.paragraphs):
    matches = code_regex.findall(p.text)
    if matches:
        total_p_matches += len(matches)
        if pi < 50 and matches:
            print(f"P{pi}: {matches}")

print(f"Total code term matches in paragraphs: {total_p_matches}")
