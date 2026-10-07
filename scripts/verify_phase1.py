import sys, docx
sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('baocaobtl_fixed.docx')
print('Read fixed docx success!')
print('Total paragraphs:', len(doc.paragraphs))
print('Total tables:', len(doc.tables))

# Check keywords in paragraphs
text_all = ' '.join(p.text for p in doc.paragraphs)
for kw in ['baby_shop_management', 'mom_baby_store', 'scrypt', 'bcrypt', 'Recharts', 'xlsx', 'CT_DonDatHang', 'DieuChinhKho', 'PhieuTraHang', 'Counters', 'AuditLogs', 'HanSuDung']:
    count = text_all.count(kw)
    print(f'Paragraphs - Keyword "{kw}": {count}')

# Check tables
table_cells_text = ' '.join(c.text for t in doc.tables for r in t.rows for c in r.cells)
for kw in ['Users', 'VaiTro', 'NhanVien', 'KhachHang', 'NhaCungCap', 'LoaiHang', 'SanPham', 'TonKho', 'DonDatHang', 'CT_DonDatHang', 'DonHang', 'CT_DonHang', 'HoaDon', 'CT_HoaDon', 'PhieuNhap', 'CT_PhieuNhap', 'PhieuXuat', 'CT_PhieuXuat', 'PhieuThu', 'PhieuChi', 'ThanhToan', 'CongNo', 'KiemKe', 'CT_KiemKe', 'DieuChinhKho', 'PhieuTraHang', 'CT_PhieuTraHang', 'KhuyenMai', 'CT_KhuyenMai', 'Counters', 'AuditLogs']:
    count = table_cells_text.count(kw)
    print(f'Table cell - Collection "{kw}": {count}')
