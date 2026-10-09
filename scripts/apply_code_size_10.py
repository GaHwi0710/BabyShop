# -*- coding: utf-8 -*-
"""
apply_code_size_10.py
Định dạng toàn bộ tất cả các từ code trong file Word Nhom1_BCBTL.docx thành font size 10 (Pt(10)):
1. Toàn bộ 32 bảng cấu trúc CSDL (Bảng 4.1 đến Bảng 4.32):
   - Cột 0 (Tên trường): font 'Courier New', size 10, bold=True
   - Cột 1 (Kiểu dữ liệu): font 'Courier New', size 10
   - Cột 2 & 3: các từ code (tên bảng, tên trường, kiểu dữ liệu, toán tử $inc, $gte, format YYYY-MM-DD...) thành 'Courier New', size 10.
2. Bảng 6.1 (Module & Use cases):
   - Cột Use Case và Cột Collection MongoDB thành 'Courier New', size 10.
3. Mục 4.6 (Chỉ mục / Database Indexes):
   - Toàn bộ các dòng định nghĩa index thành 'Courier New', size 10.
4. Mục 4.7 (Script tạo CSDL):
   - Toàn bộ đoạn code script createIndex thành 'Courier New', size 10.
5. Phụ lục (Script CSDL ensure-indexes.js):
   - Toàn bộ đoạn code script thành 'Courier New', size 10.
6. Toàn bộ các đoạn văn trong báo cáo:
   - Tất cả các từ code (tên 32 collection, tên trường, BSON type, tên file .js, hàm/operator MongoDB...)
     được chuyển thành font 'Courier New', size 10.
7. Cập nhật ảnh ERD 32 bảng chuẩn và chỉnh sửa lỗi lặp chữ ở trang bìa.
"""

import sys
import os
import re
import shutil
from pathlib import Path
import docx
from docx.shared import Pt, RGBColor

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/BabyShop")
FILE_PATH = ROOT / "Nhom1_BCBTL.docx"
BACKUP_PATH = ROOT / "Nhom1_BCBTL_backup.docx"
PNG_32_FILE = ROOT / "so_do_erd_mongodb_32_bang.png"

# Danh sách đầy đủ các định danh code nghiệp vụ và kỹ thuật trong hệ thống
CODE_IDENTIFIERS = [
    # 32 Collections & CT_*
    'CT_DonDatHang', 'CT_PhieuNhap', 'CT_DonHang', 'CT_HoaDon', 'CT_PhieuXuat',
    'CT_PhieuTraHang', 'CT_KiemKe', 'CT_KhuyenMai', 'DieuChinhKho', 'DonDatHang',
    'PhieuTraHang', 'NhaCungCap', 'KhachHang', 'AuditLogs', 'PhieuNhap', 'PhieuXuat',
    'KhuyenMai', 'ThanhToan', 'NhanVien', 'LoaiHang', 'PhieuThu', 'PhieuChi',
    'Counters', '_metadata', 'SanPham', 'DonHang', 'HoaDon', 'TonKho', 'TheKho',
    'KiemKe', 'VaiTro', 'Users', 'CongNo', 'SoQuy', 'CT_*',
    
    # BSON Types
    'ObjectId', 'String', 'Number', 'Boolean', 'Array', 'Object', 'Mixed', 'Date',
    
    # Operators & Functions & Files
    '$inc', '$gte', '$lte', '$gt', '$lt', '$set', '$lookup',
    'baby_shop_management', 'ensure-indexes.js', 'init_database.js', 'mongodb.js', 'seed.js',
    'PROTECTED_VOUCHERS', 'adjustStock', 'ReturnPage', 'AdminPage', 'ReportPage',
    
    # Field names
    'passwordHash', 'SoLuongTon', 'SoHoaDonNCC', 'NgayHoaDonNCC', 'DaThanhToan',
    'LoaiPhieuXuat', 'NgayPhatSinh', 'HanThanhToan', 'SoLanSuDung', 'GioiHanSuDung',
    'HinhThucThanhToan', 'TienThueGTGT', 'TonKhoToiThieu', 'DiemTichLuy', 'HangThanhVien',
    'LaVaiTroHeThong', 'TrangThaiKiemKe', 'LyDoDieuChinh', 'NgayDieuChinh', 'PhanTramGiam',
    'GiamToiDa', 'DonHangToiThieu', 'NgayBatDau', 'NgayKetThuc', 'SoLuongSoSach',
    'SoLuongThucTe', 'ChenhLech', 'NguoiLienHe', 'NguoiNopTien', 'NguoiNhanTien',
    'ChungTuGoc', 'LoaiCongNo', 'SoTienConLai', 'SoTienDaTra', 'TongThanhToan',
    'TienGiamGia', 'DiemSuDung', 'MaKHCode', 'MaVaiTro', 'TenVaiTro', 'MaLoai', 'TenLoai',
    'TenNCC', 'TenKH', 'TenSP', 'DonViTinh', 'MaVach', 'BienThe', 'HinhAnh', 'GiaNhap',
    'GiaVon', 'ThueSuat', 'TienThue', 'createdAt', 'updatedAt', 'appliedAt', 'timestamp',
    'username', 'fullName', 'details', 'stock', 'HanSuDung', 'ConNo', 'TongTien', 'TienHang',
    'SoLuong', 'DonGia', 'ThanhTien', 'NguoiLap', 'GhiChu', 'LyDo', 'TrangThai', 'KemTheo',
    'action', 'module', 'userId', 'role', 'status', 'email', 'phone', 'CCCD', 'HoTen',
    'ChucVu', 'PhongBan', 'SDT', 'Email', 'DiaChi', 'QuyenHan', 'MaKey', 'PhuongThuc',
    'MaDoiTuong', 'LoaiDoiTuong', 'SoTien', 'NgayLap', 'NgayNhap', 'NgayXuat', 'NgayTra',
    'NgayDat', 'NgayBan', 'NgayThanhToan', 'NgayKiemKe', '_id',
    
    # Mã nghiệp vụ tự sinh (Codes)
    'MaDDH', 'MaPTH', 'MaNCC', 'MaHD', 'MaDH', 'MaPN', 'MaPX', 'MaPT', 'MaPC',
    'MaKK', 'MaKM', 'MaNV', 'MaSP', 'MaKH', 'MaCN', 'MaTT', 'MaDC', 'MaKho'
]

# Tạo regex tìm kiếm chính xác các từ code (ưu tiên từ dài trước)
CODE_IDENTIFIERS_SORTED = sorted(list(set(CODE_IDENTIFIERS)), key=lambda x: len(x), reverse=True)
escaped_terms = [re.escape(t) for t in CODE_IDENTIFIERS_SORTED]
code_regex = re.compile(r'(?<![A-Za-z0-9_])(' + '|'.join(escaped_terms) + r')(?![A-Za-z0-9_])')

def format_run_as_code(run, is_bold=None):
    """Định dạng run thành font Courier New, size 10pt."""
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    if is_bold is not None:
        run.font.bold = is_bold

def format_cell_code(cell, is_pure_code=False, is_bold=None):
    """Định dạng các từ code trong ô bảng."""
    for p in cell.paragraphs:
        if is_pure_code:
            # Toàn bộ ô là code (ví dụ cột 0 và cột 1)
            for r in p.runs:
                format_run_as_code(r, is_bold=is_bold)
        else:
            # Ô chứa text mô tả, cần quét và đổi những từ code sang Courier New size 10
            format_paragraph_code_words(p, in_table=True)

def format_paragraph_code_words(p, in_table=False):
    """Quét và định dạng các từ code trong đoạn văn thành font Courier New size 10."""
    # Không can thiệp nếu đoạn văn chứa ảnh
    if p._element.xpath('.//a:blip'):
        return False

    # Bỏ qua các tiêu đề Heading lớn và chú thích Hình/Bảng (chỉ chỉnh Courier New nếu có sẵn)
    if not in_table:
        if p.style.name.startswith('Heading') or p.text.strip().startswith('Hình ') or p.text.strip().startswith('Bảng '):
            for r in p.runs:
                if r.font.name == 'Courier New':
                    r.font.size = Pt(10)
            return False

    # Kiểm tra xem có từ code hoặc Courier New nào trong đoạn không
    has_courier = any(r.font.name == 'Courier New' for r in p.runs)
    has_regex = any(code_regex.search(r.text) for r in p.runs if r.font.name != 'Courier New')

    if not has_courier and not has_regex:
        # Trong bảng, nếu chưa có size thì đặt size 9.5pt hoặc 10pt
        if in_table:
            for r in p.runs:
                if not r.font.size:
                    r.font.size = Pt(10)
        return False

    # Phân tách và xây dựng lại danh sách run
    new_runs_data = []
    for r in p.runs:
        if r.font.name == 'Courier New':
            new_runs_data.append((r.text, 'Courier New', Pt(10), r.font.bold, r.font.italic, r.font.color.rgb if r.font.color else None))
        else:
            text = r.text
            if not code_regex.search(text):
                base_size = r.font.size if r.font.size else (Pt(10) if in_table else None)
                new_runs_data.append((text, r.font.name, base_size, r.font.bold, r.font.italic, r.font.color.rgb if r.font.color else None))
            else:
                parts = code_regex.split(text)
                for part in parts:
                    if not part:
                        continue
                    if code_regex.fullmatch(part):
                        # Đây là từ code -> Courier New, size 10
                        new_runs_data.append((part, 'Courier New', Pt(10), True if in_table else r.font.bold, False, None))
                    else:
                        base_size = r.font.size if r.font.size else (Pt(10) if in_table else None)
                        new_runs_data.append((part, r.font.name, base_size, r.font.bold, r.font.italic, r.font.color.rgb if r.font.color else None))

    # Gán lại các run vào đoạn văn
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

def main():
    print(f"📖 Đang xử lý file: {FILE_PATH}...")
    if not FILE_PATH.exists():
        print(f"❌ Không tìm thấy tệp: {FILE_PATH}")
        return

    # Sao lưu an toàn trước khi chỉnh sửa
    shutil.copy2(FILE_PATH, BACKUP_PATH)
    print(f"🛡️ Đã sao lưu bản dự phòng tại: {BACKUP_PATH}")

    doc = docx.Document(str(FILE_PATH))
    print(f"✅ Đã tải: {len(doc.paragraphs)} đoạn văn, {len(doc.tables)} bảng.")

    # 1. Sửa lỗi lặp từ trang bìa nếu có
    for p in doc.paragraphs[:10]:
        if "BÁO CÁO BÁO CÁO BÀI TẬP LỚN" in p.text:
            p.text = p.text.replace("BÁO CÁO BÁO CÁO BÀI TẬP LỚN", "BÁO CÁO BÀI TẬP LỚN")
            print("✨ Đã sửa trang bìa: 'BÁO CÁO BÀI TẬP LỚN'")

    # 2. Cập nhật ảnh ERD 32 bảng chuẩn vào Hình 4.1 nếu chưa đúng
    if PNG_32_FILE.exists():
        png_bytes = PNG_32_FILE.read_bytes()
        for i, p in enumerate(doc.paragraphs):
            if "Hình 4.1. Sơ đồ quan hệ logic" in p.text:
                prev_p = doc.paragraphs[i-1]
                for r in prev_p.runs:
                    for blip in r._r.xpath('.//a:blip'):
                        r_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if r_id in doc.part.related_parts:
                            doc.part.related_parts[r_id]._blob = png_bytes
                            print(f"🖼️ Đã cập nhật ảnh sơ đồ ERD 32 bảng chuẩn (r_id={r_id}, size={len(png_bytes)})!")

    # 3. Định dạng toàn bộ 32 bảng cấu trúc CSDL (Tables 9 đến 40)
    print("📊 Đang định dạng từ code trong 32 bảng CSDL (Bảng 4.1 đến Bảng 4.32)...")
    schema_code_terms_count = 0
    for ti in range(9, 41):
        t = doc.tables[ti]
        for ri, r in enumerate(t.rows):
            if ri == 0:
                # Dòng tiêu đề bảng: 10pt bold
                for c in r.cells:
                    for p in c.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(10)
                            run.font.bold = True
                continue

            # Cột 0: Tên trường (Field Name) -> BẮT BUỘC Courier New, size 10, bold=True
            c0 = r.cells[0]
            for p in c0.paragraphs:
                for run in p.runs:
                    format_run_as_code(run, is_bold=True)
                    schema_code_terms_count += 1

            # Cột 1: Kiểu dữ liệu (Data Type) -> BẮT BUỘC Courier New, size 10
            c1 = r.cells[1]
            for p in c1.paragraphs:
                for run in p.runs:
                    format_run_as_code(run, is_bold=False)
                    schema_code_terms_count += 1

            # Cột 2 (Ràng buộc) và Cột 3 (Mô tả): format các từ code xuất hiện bên trong
            format_cell_code(r.cells[2], is_pure_code=False)
            format_cell_code(r.cells[3], is_pure_code=False)

    print(f"✅ Đã định dạng hơn {schema_code_terms_count} trường và kiểu dữ liệu thành font Courier New size 10 trong 32 bảng schema!")

    # 4. Định dạng Bảng 41 (Module & Use Cases - Bảng 6.1)
    t41 = doc.tables[41]
    for ri, r in enumerate(t41.rows):
        if ri == 0:
            for c in r.cells:
                for p in c.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(10)
                        run.font.bold = True
            continue
        # Cột 2 (Use Cases: UC01 - UC04) -> Courier New size 10
        for p in r.cells[2].paragraphs:
            for run in p.runs:
                format_run_as_code(run, is_bold=True)
        # Cột 3 (Collection MongoDB: Users, VaiTro...) -> Courier New size 10
        format_cell_code(r.cells[3], is_pure_code=False)
        # Cột 4 (Màn hình tương ứng)
        format_cell_code(r.cells[4], is_pure_code=False)

    # 5. Định dạng các bảng khác (T1-T8, T42-T44)
    for ti in [1, 2, 3, 4, 5, 6, 7, 8, 42, 43, 44]:
        t = doc.tables[ti]
        for ri, r in enumerate(t.rows):
            for ci, c in enumerate(r.cells):
                for p in c.paragraphs:
                    for run in p.runs:
                        if run.font.name == 'Courier New':
                            run.font.size = Pt(10)
                        elif not run.font.size and ri > 0:
                            run.font.size = Pt(10)
                format_cell_code(c, is_pure_code=False)

    # 6. Định dạng Mục 4.6 (Chỉ mục / Database Indexes)
    print("📑 Đang định dạng Mục 4.6 (Chỉ mục)...")
    for i in range(580, min(610, len(doc.paragraphs))):
        p = doc.paragraphs[i]
        if p.text.strip().startswith("• ") and ("{" in p.text or ":" in p.text):
            for run in p.runs:
                format_run_as_code(run)

    # 7. Định dạng Mục 4.7 (Script tạo CSDL) và Phụ lục (ensure-indexes.js)
    print("💻 Đang định dạng các khối mã lệnh (Script tạo CSDL & Phụ lục)...")
    for p in doc.paragraphs:
        if "createIndex" in p.text or "ensure-indexes.js" in p.text or "// Script tự động" in p.text:
            for run in p.runs:
                format_run_as_code(run)

    # 8. Định dạng toàn bộ các từ code trong các đoạn văn tử tế
    print("📝 Đang quét và định dạng toàn bộ từ code trong văn bản...")
    p_code_count = 0
    for pi, p in enumerate(doc.paragraphs):
        if format_paragraph_code_words(p, in_table=False):
            p_code_count += 1

    print(f"✅ Đã định dạng từ code trong {p_code_count} đoạn văn thành Courier New size 10!")

    # 9. Lưu trực tiếp vào file Nhom1_BCBTL.docx
    print(f"💾 Đang lưu kết quả hoàn tất vào: {FILE_PATH}...")
    doc.save(str(FILE_PATH))
    print(f"🎉 THÀNH CÔNG RỰC RỠ! Tệp đã được lưu tại: {FILE_PATH} ({FILE_PATH.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
