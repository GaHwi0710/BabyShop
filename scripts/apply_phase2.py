import sys
import docx
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl

sys.stdout.reconfigure(encoding='utf-8')

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_row(row, heights=None, font_size=9.5, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    for idx, cell in enumerate(row.cells):
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = align if idx not in [0, 2] else WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            r.font.bold = bold

def add_styled_row_to_table(tbl, row_data, font_size=9.5):
    row = tbl.add_row()
    for idx, val in enumerate(row_data):
        row.cells[idx].text = str(val)
    style_row(row, font_size=font_size)
    return row

def main():
    print("Loading baocaobtl_fixed.docx...")
    doc = docx.Document("baocaobtl_fixed.docx")
    body = doc._body._body

    # =========================================================================
    # PHẦN 1: VÁ CÁC LỖI CÒN SÓT CỦA PHA 1 (YÊU CẦU A)
    # =========================================================================
    print("--- 1. Fixing remaining Phase 1 items in paragraphs ---")
    
    # 1.1. Sửa Lời mở đầu & Mục 3.1.2: "31 collection (bao gồm Users)"
    for p in doc.paragraphs[:50]:
        if "31 collection" in p.text and "bảng hệ thống Users" in p.text:
            print("  Fixing Chapter 3 outline text...")
            p.text = p.text.replace("31 collection tiếng Việt chuẩn hóa và bảng hệ thống Users", "31 collection (bao gồm Users)")
            for r in p.runs: r.font.name = "Times New Roman"

    for p in doc.paragraphs[575:600]:
        if "baby_shop_management" in p.text and "bảng hệ thống Users" in p.text:
            print("  Fixing 3.1.2 Database architecture text...")
            p.text = p.text.replace("31 collection tiếng Việt chuẩn hóa và bảng hệ thống Users", "31 collection (bao gồm Users)")
            for r in p.runs: r.font.name = "Times New Roman"

    # 1.2. Sửa các UC: Tên collection thật, mã chứng từ thật, bỏ barcode, bỏ inventory_transactions
    for i in range(150, 525):
        p = doc.paragraphs[i]
        t = p.text

        # UC03: users -> Users
        if "cập nhật vào collection `users`" in t:
            p.text = t.replace("`users`", "`Users`")
        
        # UC04: Sửa câu lồng ngoặc PUT/PATCH
        if "PUT /api/admin/accounts/:id (và PATCH toggle-lock)" in t:
            p.text = "6. Hệ thống thực hiện thao tác tương ứng (gọi PUT /api/admin/accounts/:id để cập nhật hoặc PATCH /api/admin/accounts/:id/toggle-lock để khóa/mở khóa tài khoản) và làm mới danh sách hiển thị."

        # UC05: KH-00001 -> KH001
        if "KH-00001" in t:
            p.text = t.replace("KH-00001", "KH001")

        # UC06: NCC-00001 -> NCC001, suppliers -> NhaCungCap
        if "NCC-00001" in t:
            p.text = t.replace("NCC-00001", "NCC001")
        if "collection `suppliers`" in t:
            p.text = t.replace("`suppliers`", "`NhaCungCap`")

        # UC07: Xóa mã vạch/barcode, thay bằng mã SP/tên SP; products -> SanPham, inventory -> TonKho
        if "mã vạch" in t.lower() or "barcode" in t.lower():
            if "Mô tả tóm tắt" in t:
                p.text = "Mô tả tóm tắt: Quản lý toàn bộ danh mục sản phẩm kinh doanh (sữa, bỉm, đồ dùng...), mã sản phẩm, giá nhập, giá bán, hạn sử dụng và định mức tồn kho an toàn."
            elif "thanh tìm kiếm mã vạch/tên hàng" in t:
                p.text = "2. Hệ thống hiển thị danh mục sản phẩm, bộ lọc theo loại hàng và thanh tìm kiếm theo tên hoặc mã sản phẩm."
            elif "Mã vạch Barcode" in t:
                p.text = "3. Người dùng chọn 'Thêm sản phẩm mới', nhập: Mã sản phẩm (MaSP), Tên sản phẩm (TenSP), Loại hàng (MaLoai), Đơn vị tính (DonViTinh), Giá nhập (GiaNhap), Giá bán (GiaBan), Hạn sử dụng (HanSuDung) và Tồn kho tối thiểu (SoLuongToiThieu mặc định 10)."
            elif "Mã vạch bị trùng" in t:
                p.text = "3b. Mã sản phẩm hoặc tên sản phẩm bị trùng lặp: Hệ thống cảnh báo lỗi và yêu cầu kiểm tra lại thông tin."
        if "collection `products`" in t or "`inventory`" in t:
            p.text = t.replace("`products`", "`SanPham`").replace("`inventory`", "`TonKho`")

        # UC08: categories -> LoaiHang
        if "collection `categories`" in t:
            p.text = t.replace("`categories`", "`LoaiHang`")

        # UC09: employees -> NhanVien
        if "collection `employees`" in t:
            p.text = t.replace("`employees`", "`NhanVien`")

        # UC10: DH-00001 -> DDH001, purchase_orders -> DonDatHang, 'pending' -> 'Chờ duyệt'
        if "DH-00001" in t and ("đơn hàng" in t.lower() or "đặt hàng" in t.lower()):
            p.text = t.replace("DH-00001", "DDH001")
        if "collection `purchase_orders`" in t or "'pending'" in t:
            p.text = t.replace("`purchase_orders`", "`DonDatHang`").replace("'pending'", "'Chờ duyệt'")

        # UC11: PN-00001 -> PN001, warehouse_receipts -> PhieuNhap, bỏ inventory_transactions
        if "PN-00001" in t:
            p.text = t.replace("PN-00001", "PN001")
        if "warehouse_receipts" in t or "inventory_transactions" in t:
            p.text = "6. Backend ghi nhận phiếu nhập vào collection `PhieuNhap` (kèm chi tiết các dòng hàng vào `CT_PhieuNhap`), đồng thời tự động cập nhật tăng số lượng tồn kho trong `TonKho` và ghi nhận công nợ phải trả vào `CongNo`."

        # UC13: HD-00001 -> HD001, xóa máy quét mã vạch, viết lại bước 8
        if "HD-00001" in t:
            p.text = t.replace("HD-00001", "HD001")
        if "máy quét mã vạch" in t:
            p.text = "4. Nhân viên gõ tên hoặc mã sản phẩm vào thanh tìm kiếm nhanh để chọn và thêm sản phẩm vào giỏ hàng POS."
        if "sales_invoices" in t and "POST /api/sales-orders" in t:
            p.text = "8. Backend tiếp nhận POST /api/sales-orders: Ghi nhận đơn hàng vào collection `DonHang` (và `CT_DonHang`), tự sinh chứng từ trong `HoaDon` (và `CT_HoaDon`), tự động tạo phiếu xuất kho trong `PhieuXuat` (và `CT_PhieuXuat`), giảm số lượng tồn kho trong `TonKho`, ghi nhật ký thu tiền hoặc phát sinh công nợ trong `CongNo` nếu bán nợ."

        # UC15: PX-00001 -> PX001, bỏ inventory_transactions, inventory -> TonKho
        if "PX-00001" in t:
            p.text = t.replace("PX-00001", "PX001")
        if "lưu vết vào `inventory_transactions`" in t:
            p.text = "6. Backend trừ số lượng tồn kho trong `TonKho`, cập nhật trường stock trong `SanPham` và lưu chi tiết xuất kho vào collection `CT_PhieuXuat`."

        # UC17: PT-00001 -> PT001, cash_receipts -> PhieuThu
        if "PT-00001" in t:
            p.text = t.replace("PT-00001", "PT001")
        if "`cash_receipts`" in t:
            p.text = t.replace("`cash_receipts`", "`PhieuThu`")

        # UC18: PC-00001 -> PC001, cash_payments -> PhieuChi
        if "PC-00001" in t:
            p.text = t.replace("PC-00001", "PC001")
        if "`cash_payments`" in t:
            p.text = t.replace("`cash_payments`", "`PhieuChi`")

        # UC19: Bỏ tên bảng cũ
        if "`cash_receipts`, `cash_payments`, `sales_invoices`" in t:
            p.text = "2. Hệ thống tổng hợp dữ liệu từ `PhieuThu`, `PhieuChi`, `HoaDon`, `DonDatHang` và `PhieuNhap`."

        # UC21: KK-00001 -> KK001, nút 'Cân bằng kho', Thủ kho tự làm được
        if "Tác nhân chính: Thủ kho, Quản lý" in t:
            p.text = "Tác nhân chính: Thủ kho (tự chủ thực hiện cân bằng kho), Quản lý"
        if "KK-00001" in t:
            p.text = t.replace("KK-00001", "KK001")
        if "Hoàn tất kiểm kê" in t and "adjust" in t:
            p.text = "6. Thủ kho nhấn nút 'Cân bằng kho' (hoặc 'Điều chỉnh kho') trên giao diện để gửi yêu cầu POST /api/stocktakes/:id/adjust."
        if "điều chỉnh số lượng tồn kho trong `inventory`" in t:
            p.text = "7. Hệ thống tự động điều chỉnh số lượng tồn kho trong collection `TonKho` về đúng số thực tế kiểm đếm, tạo phiếu điều chỉnh trong `DieuChinhKho` và lưu vết vào `AuditLogs`."

    # =========================================================================
    # PHẦN 2: CẬP NHẬT TÁC NHÂN (MỤC 2.2 & TABLE 7) THEO MA TRẬN QUYỀN
    # =========================================================================
    print("--- 2. Updating Section 2.2 and Table 7 (Actors) ---")
    t7 = doc.tables[7]
    actor_data = [
        ("1", "Quản trị hệ thống (QuanTriHeThong / Admin)",
         "Cán bộ kỹ thuật phụ trách quản trị, bảo mật và vận hành toàn bộ hạ tầng phần mềm.",
         "Toàn quyền quản lý tài khoản người dùng, phân quyền RBAC chi tiết (xem/tạo/sửa/xóa) trên 24 module, giám sát nhật ký kiểm toán (AuditLogs), sao lưu và phục hồi dữ liệu hệ thống (Backup/Restore)."),
        ("2", "Quản lý chung (QuanLy / Manager)",
         "Chủ cửa hàng hoặc cấp quản lý phụ trách điều hành tổng thể mọi hoạt động kinh doanh, nhân sự và kho bãi.",
         "Toàn quyền nghiệp vụ (bypass), xem bảng điều khiển Dashboard thời gian thực, duyệt đơn mua hàng, giám sát sổ quỹ thu chi, công nợ và xem toàn bộ hệ thống 17 báo cáo tài chính - quản trị."),
        ("3", "Kế toán (KeToan / Accountant)",
         "Nhân sự chuyên trách công tác tài chính, kiểm soát dòng tiền, công nợ và lập báo cáo kế toán.",
         "Quản lý hóa đơn, lập phiếu thu tiền mặt (Mẫu 01-TT), lập phiếu chi tiền mặt (Mẫu 02-TT), theo dõi và thanh toán công nợ hai chiều (NCC và Khách hàng), đối chiếu sổ quỹ tiền mặt, kết xuất hệ thống 17 báo cáo tài chính và sổ sách kế toán chuẩn mực."),
        ("4", "Nhân viên bán hàng (NhanVienBanHang / Sales)",
         "Nhân viên trực tiếp tư vấn, thực hiện các giao dịch bán lẻ tại quầy và chăm sóc khách hàng.",
         "Bán hàng tại quầy (SalesPOSPage), lập đơn hàng POS, tự động phát sinh hóa đơn và phiếu xuất kho, tạo mã VietQR động NAPAS, tích lũy điểm thưởng thành viên, đổi mã voucher giảm giá, xử lý đổi trả hàng (ReturnPage) và lập phiếu thu tiền mặt bán lẻ."),
        ("5", "Thủ kho (ThuKho / NhanVienKho)",
         "Nhân sự chịu trách nhiệm trực tiếp về mặt hiện vật của hàng hóa, bảo quản và luân chuyển kho.",
         "Quản lý danh mục sản phẩm, lập phiếu nhập kho theo đơn đặt hàng NCC, lập phiếu xuất kho, theo dõi tồn kho thời gian thực, thực hiện kiểm kê kho định kỳ và tự chủ bấm nút Cân bằng kho (Điều chỉnh kho) cập nhật tồn kho thực tế mà không cần chờ duyệt."),
    ]
    for r_idx, data in enumerate(actor_data):
        row = t7.rows[r_idx + 1]
        for c_idx, text in enumerate(data):
            row.cells[c_idx].text = text
            style_row(row, font_size=9.5)

    # =========================================================================
    # PHẦN 3: BỔ SUNG UC25, UC26, UC27 VÀO MỤC 2.3 & TABLE 8
    # =========================================================================
    print("--- 3. Adding UC25, UC26, UC27 to Section 2.3 and Table 8 ---")
    
    # 3.1. Cập nhật các đoạn văn giới thiệu tổng số Use Case (24 -> 27)
    for p in doc.paragraphs[:160]:
        if "24 Use Case" in p.text:
            p.text = p.text.replace("24 Use Case", "27 Use Case")
        if "24 ca sử dụng" in p.text:
            p.text = p.text.replace("24 ca sử dụng", "27 ca sử dụng")
        if "Bảng 2.3.1. Danh mục 24 Use Case" in p.text:
            p.text = "Bảng 2.3.1. Danh mục 27 Use Case của Hệ thống quản lý Cửa hàng Mẹ và Bé"

    # 3.2. Bổ sung 3 dòng vào Table 8
    t8 = doc.tables[8]
    new_ucs_table = [
        ["UC25", "Quản lý đổi trả hàng", "NhanVienBanHang, QuanLy", "Kho / Bán hàng", "ReturnPage (Đổi trả & Hoàn tiền)"],
        ["UC26", "Tích điểm và đổi voucher", "NhanVienBanHang, Khách hàng", "Bán hàng / Khách hàng", "CustomersPage (Tích điểm & Voucher)"],
        ["UC27", "Sao lưu và phục hồi dữ liệu", "QuanTriHeThong (Admin)", "Quản trị hệ thống", "BackupPage (Sao lưu & Phục hồi JSON)"]
    ]
    # Kiểm tra xem Table 8 đã có UC25 chưa
    t8_codes = [r.cells[0].text.strip() for r in t8.rows]
    for row_data in new_ucs_table:
        if row_data[0] not in t8_codes:
            add_styled_row_to_table(t8, row_data, font_size=9.5)

    # 3.3. Bổ sung đặc tả chi tiết UC25, UC26, UC27 vào cuối Mục 2.3.2 (trước Mục 2.4)
    p_24_heading = None
    for child in body:
        if isinstance(child, CT_P):
            p = docx.text.paragraph.Paragraph(child, doc)
            if "2.4. Biểu đồ Use Case (Use Case Diagram)" in p.text:
                p_24_heading = child
                break

    if p_24_heading is not None:
        print("  Inserting detailed specifications for UC25, UC26, UC27...")
        uc_specs = [
            # UC25
            ("Use Case: UC25 – Quản lý đổi trả hàng", [
                "Tác nhân chính: Nhân viên bán hàng, Quản lý",
                "Mô tả tóm tắt: Tiếp nhận sản phẩm khách hàng mang trả lại theo hóa đơn bán lẻ, kiểm tra tính hợp lệ của hàng hóa, hoàn tiền hoặc đổi sản phẩm khác, tự động nhập lại kho và cập nhật doanh thu bán lẻ.",
                "Tiền điều kiện: Khách hàng mang hàng hóa và hóa đơn mua hàng còn trong thời hạn đổi trả quy định (trong vòng 7 ngày) đến cửa hàng.",
                "Luồng sự kiện chính:",
                "1. Nhân viên truy cập menu 'Kho' -> 'Trả hàng' (ReturnPage) hoặc điều hướng trực tiếp từ màn hình Bán hàng POS.",
                "2. Nhân viên nhập mã hóa đơn mua hàng gốc (ví dụ: HD001) để hệ thống tự động tải chi tiết danh sách sản phẩm và đơn giá tương ứng.",
                "3. Nhân viên chọn sản phẩm khách hàng muốn trả, nhập số lượng trả, tình trạng sản phẩm và ghi chú lý do trả hàng (hàng lỗi bao bì, đổi size, đổi loại sữa...).",
                "4. Hệ thống tự động tính toán tổng số tiền hoàn trả cho khách hàng (refundAmount) căn cứ theo đơn giá thực tế trên hóa đơn mua ban đầu.",
                "5. Nhân viên chọn hình thức hoàn trả tiền (Tiền mặt hoặc Chuyển khoản) và nhấn nút 'Tạo phiếu trả hàng'.",
                "6. Frontend gửi yêu cầu POST /api/returns: Backend tự động sinh mã phiếu trả duy nhất (PTH001), lưu thông tin vào collection PhieuTraHang và chi tiết vào CT_PhieuTraHang.",
                "7. Hệ thống tự động cập nhật tăng lại số lượng tồn kho trong collection TonKho (và cập nhật trường stock trong SanPham) đối với các mặt hàng hoàn trả còn nguyên vẹn.",
                "8. Trường hợp hoàn tiền mặt, hệ thống tự động ghi nhận phiếu chi hoặc giảm trừ quỹ tiền mặt tương ứng, đồng thời lưu vết hành động vào AuditLogs.",
                "Luồng ngoại lệ / Thay thế:",
                "2a. Mã hóa đơn không tồn tại hoặc đã quá hạn đổi trả quy định: Hệ thống cảnh báo từ chối tiếp nhận đổi trả.",
                "Hậu điều kiện: Hàng hóa được nhập lại kho an toàn, khách hàng nhận lại tiền hoàn hoặc hàng đổi mới, doanh thu và sổ quỹ được cập nhật minh bạch, chính xác."
            ]),
            # UC26
            ("Use Case: UC26 – Quản lý tích điểm và đổi voucher", [
                "Tác nhân chính: Nhân viên bán hàng, Khách hàng",
                "Mô tả tóm tắt: Theo dõi điểm thưởng tích lũy của khách hàng thân thiết theo tỷ lệ giá trị đơn hàng (10.000 VNĐ = 1 điểm), phân hạng thành viên (Đồng, Bạc, Vàng, Kim Cương) và quy đổi điểm thưởng thành mã giảm giá (voucher) áp dụng chiết khấu tức thì cho đơn mua hàng.",
                "Tiền điều kiện: Khách hàng đã có hồ sơ thông tin trong collection KhachHang.",
                "Luồng sự kiện chính:",
                "1. Khi giao dịch tại quầy thu ngân (SalesPOSPage) hoặc quản lý danh bạ khách hàng (CustomersPage), nhân viên tra cứu khách hàng qua số điện thoại hoặc mã KH (ví dụ: KH001).",
                "2. Hệ thống hiển thị điểm tích lũy hiện tại (loyaltyPoints) và hạng thẻ thành viên tương ứng của khách hàng.",
                "3. Khi khách hàng tích lũy đủ điểm và có nhu cầu đổi voucher: Nhân viên nhấn nút 'Đổi voucher'.",
                "4. Hệ thống hiển thị bảng các hạn mức đổi thưởng chuẩn hóa theo chính sách cửa hàng:",
                "   - Đổi 50 điểm: Nhận voucher BAC50K (giảm 50.000 VNĐ cho đơn từ 300.000 VNĐ).",
                "   - Đổi 100 điểm: Nhận voucher VANG100K (giảm 100.000 VNĐ cho đơn từ 500.000 VNĐ).",
                "   - Đổi 200 điểm: Nhận voucher KC200K (giảm 200.000 VNĐ cho đơn từ 1.000.000 VNĐ).",
                "5. Nhân viên chọn gói voucher khách muốn đổi và xác nhận.",
                "6. Frontend gửi yêu cầu POST /api/customers/:id/redeem-voucher với mã gói voucher tương ứng.",
                "7. Backend kiểm tra điều kiện điểm, thực hiện trừ điểm tích lũy của khách hàng trong collection KhachHang, tự động tạo mã voucher mới lưu vào collection KhuyenMai và trả về mã giảm giá.",
                "8. Nhân viên áp dụng trực tiếp mã voucher vừa đổi vào giỏ hàng POS để chiết khấu tức thì cho khách hàng trên hóa đơn.",
                "Luồng ngoại lệ / Thay thế:",
                "4a. Khách hàng chưa tích lũy đủ điểm tối thiểu: Hệ thống cảnh báo số điểm hiện tại không đủ để quy đổi mức voucher đã chọn.",
                "Hậu điều kiện: Số dư điểm thưởng của khách hàng được khấu trừ chính xác, mã voucher được kích hoạt hợp lệ trong hệ thống khuyến mại."
            ]),
            # UC27
            ("Use Case: UC27 – Quản trị sao lưu và phục hồi dữ liệu", [
                "Tác nhân chính: Quản trị viên hệ thống (Admin)",
                "Mô tả tóm tắt: Sao lưu toàn diện 31 collection của CSDL MongoDB thành tệp snapshot định dạng JSON lưu trữ trên đĩa máy chủ và hỗ trợ phục hồi nguyên trạng cơ sở dữ liệu khi xảy ra sự cố kỹ thuật hoặc chuyển đổi môi trường triển khai.",
                "Tiền điều kiện: Người dùng đăng nhập hệ thống với vai trò Quản trị hệ thống (QuanTriHeThong / Admin).",
                "Luồng sự kiện chính:",
                "1. Quản trị viên điều hướng tới menu 'Quản trị' -> 'Sao lưu dữ liệu' (BackupPage).",
                "2. Hệ thống tải và hiển thị danh sách các bản snapshot sao lưu đã có trên máy chủ (kèm ngày giờ tạo, dung lượng tệp và số lượng collection đã sao lưu).",
                "3. Quản trị viên nhấn nút 'Tạo bản sao lưu mới' (Create Snapshot).",
                "4. Frontend gửi yêu cầu POST /api/admin/backup tới máy chủ backend.",
                "5. Backend quét toàn bộ danh sách 31 collection (BACKUP_COLLECTIONS), trích xuất toàn bộ BSON Document thành tệp JSON có cấu trúc lưu vào thư mục backups/ trên máy chủ, đồng thời ghi nhật ký kiểm toán với hành động 'BACKUP'.",
                "6. Hệ thống tự động làm mới danh sách bản sao lưu và cho phép Quản trị viên tải tệp snapshot (.json) về lưu trữ trên máy tính cá nhân an toàn.",
                "7. Khi cần phục hồi cơ sở dữ liệu: Quản trị viên chọn một bản snapshot từ danh sách (hoặc tải tệp JSON từ máy tính) và nhấn 'Phục hồi dữ liệu' (Restore).",
                "8. Hệ thống hiển thị hộp thoại cảnh báo xác nhận bảo mật nghiêm ngặt. Sau khi Quản trị viên xác nhận, backend gửi POST /api/admin/restore, tự động xóa trắng và nạp lại đầy đủ 31 collection từ snapshot, ghi nhật ký kiểm toán với hành động 'RESTORE'.",
                "Luồng ngoại lệ / Thay thế:",
                "7a. Tệp sao lưu không đúng định dạng snapshot JSON hoặc dữ liệu bị lỗi: Hệ thống cảnh báo lỗi, từ chối nạp dữ liệu và rollback an toàn.",
                "Hậu điều kiện: Toàn bộ dữ liệu nghiệp vụ của cửa hàng được bảo vệ dự phòng an toàn, sẵn sàng phục hồi nhanh chóng khi có sự cố."
            ])
        ]
        for title, lines in uc_specs:
            p_title = doc.add_paragraph()
            p_title.style = "Normal"
            r = p_title.add_run(title)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.bold = True
            p_24_heading.addprevious(p_title._p)

            for line in lines:
                p_line = doc.add_paragraph()
                p_line.style = "Normal"
                r = p_line.add_run(line)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                if line.startswith("Tác nhân chính:") or line.startswith("Tiền điều kiện:") or line.startswith("Luồng sự kiện chính:") or line.startswith("Luồng ngoại lệ / Thay thế:") or line.startswith("Hậu điều kiện:"):
                    r.font.bold = True
                p_24_heading.addprevious(p_line._p)

            p_sep = doc.add_paragraph()
            p_24_heading.addprevious(p_sep._p)

    # =========================================================================
    # PHẦN 4: HOÀN THIỆN MỤC 3.5 (MỐI LIÊN HỆ KẾ TOÁN & NGUYÊN TẮC HẠCH TOÁN)
    # =========================================================================
    print("--- 4. Completing Section 3.5 (Accounting relationships & Journal rules) ---")
    for i, p in enumerate(doc.paragraphs):
        if "3.5. Sơ đồ tổng quan mối liên hệ giữa các phân hệ nghiệp vụ Kế Toán" in p.text:
            print("  Filling Section 3.5 content...")
            p.text = "3.5. Sơ đồ tổng quan mối liên hệ giữa các phân hệ nghiệp vụ Kế toán và Nguyên tắc Hạch toán"
            for r in p.runs: r.font.name = "Times New Roman"

            # Tìm đoạn văn ngay sau đó (đang rỗng)
            if i + 1 < len(doc.paragraphs):
                next_p = doc.paragraphs[i + 1]
                next_p.text = (
                    "Trong hệ thống Baby Shop Management ERP, các phân hệ nghiệp vụ được thiết kế liên kết hữu cơ theo dòng luân chuyển chứng từ kế toán chuẩn mực:\n\n"
                    "1. Luồng Bán hàng – Xuất kho – Doanh thu & Công nợ: Khi phát sinh giao dịch bán lẻ tại quầy POS (DonHang), hệ thống tự động sinh Hóa đơn (HoaDon) và tạo Phiếu xuất kho (PhieuXuat), đồng thời cập nhật giảm số lượng tồn kho trong TonKho. Nếu khách hàng thanh toán ngay bằng tiền mặt, hệ thống tự động tạo Phiếu thu (PhieuThu); nếu bán chịu, hệ thống tự động ghi nhận công nợ phải thu vào collection CongNo (LoaiCongNo: 'Khách hàng').\n\n"
                    "2. Luồng Mua hàng – Nhập kho – Giá vốn & Công nợ NCC: Đơn đặt hàng (DonDatHang) gửi tới nhà cung cấp là căn cứ để tạo Phiếu nhập kho (PhieuNhap). Khi nhập kho, hệ thống tự động tăng tồn kho hàng hóa (TonKho), ghi nhận chi tiết dòng hàng vào CT_PhieuNhap và phát sinh công nợ phải trả vào collection CongNo (LoaiCongNo: 'Nhà cung cấp'). Khi thanh toán công nợ, kế toán lập Phiếu chi (PhieuChi) và đồng bộ giảm trừ công nợ.\n\n"
                    "3. Nguyên tắc Hạch toán Nợ/Có tự động (On-The-Fly): Hệ thống KHÔNG sử dụng bảng CSDL tĩnh accounting_entries mà áp dụng nguyên tắc tổng hợp động tại thời điểm truy vấn Sổ nhật ký chung (Mẫu S03a-DNN qua API GET /api/reports/general-journal) từ các chứng từ gốc:\n"
                    "   • Nghiệp vụ Bán hàng: Nợ TK 111 (hoặc Nợ TK 131 nếu bán nợ) / Có TK 511 (Doanh thu bán hàng), Có TK 33311 (Thuế GTGT đầu ra); đồng thời ghi nhận Giá vốn: Nợ TK 632 / Có TK 156.\n"
                    "   • Nghiệp vụ Mua hàng nhập kho: Nợ TK 156 (Hàng hóa) / Có TK 331 (Phải trả NCC) hoặc Có TK 111 (nếu thanh toán ngay).\n"
                    "   • Nghiệp vụ Thu tiền mặt: Nợ TK 111 / Có TK 131 (Thu nợ khách hàng).\n"
                    "   • Nghiệp vụ Chi tiền mặt: Nợ TK 331 (Thanh toán nợ NCC) / Có TK 111.\n"
                    "   *(Lưu ý: Hệ thống không sử dụng tài khoản Tiền gửi ngân hàng 112 do các giao dịch chuyển khoản tại cửa hàng bán lẻ quy mô nhỏ được quy đổi hạch toán trực tiếp qua dòng tiền quỹ. Nghiệp vụ kiểm kê kho và đổi trả hàng được xử lý cân bằng kho và hoàn tiền trực tiếp, không phát sinh bút toán kế toán riêng trong code)*.\n\n"
                    "⟦ Ảnh chụp minh họa thực tế: Sơ đồ luân chuyển chứng từ và liên kết nghiệp vụ kế toán giữa các phân hệ ⟧\n"
                    "Hình 3.5.1. Sơ đồ luân chuyển chứng từ và mối liên hệ giữa các phân hệ nghiệp vụ kế toán"
                )
                for r in next_p.runs: r.font.name = "Times New Roman"

    # =========================================================================
    # PHẦN 5: CHƯƠNG 4 – THIẾT KẾ GIAO DIỆN (20 MÀN HÌNH THỰC TẾ)
    # =========================================================================
    print("--- 5. Updating Chapter 4 for 20 real frontend pages ---")
    
    # 5.1. Cập nhật giới thiệu Chương 4 (16 -> 20 màn hình)
    for p in doc.paragraphs[:50]:
        if "16 màn hình" in p.text:
            p.text = p.text.replace("16 màn hình", "20 màn hình giao diện")
            for r in p.runs: r.font.name = "Times New Roman"

    # 5.2. Xóa các đoạn nhắc mã vạch / barcode trong Chương 4
    for i in range(730, min(850, len(doc.paragraphs))):
        p = doc.paragraphs[i]
        if "quét mã vạch (Barcode)" in p.text:
            p.text = p.text.replace("quét mã vạch (Barcode)", "tìm kiếm nhanh theo tên và mã hàng")
        if "quét mã vạch" in p.text:
            p.text = p.text.replace("quét mã vạch hoặc chọn sản phẩm", "tìm kiếm và chọn sản phẩm").replace("và quét mã vạch", "")

    # 5.3. Cập nhật nội dung màn hình 4.2.16 (Báo cáo) ghi rõ 17 báo cáo và #15
    for i in range(825, min(845, len(doc.paragraphs))):
        p = doc.paragraphs[i]
        if "4.2.16. Màn hình Báo cáo" in p.text:
            p.text = "4.2.16. Màn hình Hệ thống 17 Báo cáo Kế toán & Quản trị (ReportPage)"
        if "Các loại báo cáo chính:" in p.text or "Báo cáo doanh thu, Tồn kho, Công nợ, Mua hàng, Sổ quỹ" in p.text:
            p.text = (
                "Phân hệ Báo cáo cung cấp đầy đủ hệ thống 17 báo cáo tài chính, quản trị và chứng từ sổ sách theo chuẩn mực:\n"
                "1. Báo cáo doanh thu bán hàng; 2. Báo cáo nhập – xuất kho tổng hợp; 3. Báo cáo tồn kho (Nhập - Xuất - Tồn); 4. Báo cáo công nợ tổng hợp (NCC và Khách hàng); 5. Sổ quỹ thu – chi tiền mặt tổng hợp; "
                "6. Báo cáo thu tiền mặt độc lập (8 cột Mẫu 01-TT); 7. Báo cáo chi tiền mặt độc lập (8 cột Mẫu 02-TT); 8. Báo cáo nhập kho độc lập (11 cột Mẫu 01-VT); 9. Báo cáo xuất kho độc lập (11 cột Mẫu 02-VT); "
                "10. Báo cáo thu tiền chuyển khoản (Giấy báo Có); 11. Báo cáo chi tiền chuyển khoản (Ủy nhiệm chi); 12. Báo cáo kết quả hoạt động kinh doanh (Mẫu B 02 - DN); 13. Sổ chi tiết hàng hóa (Mẫu S10-DN); "
                "14. Sổ nhật ký chung (Mẫu S03a-DNN); 15. Sổ tài sản cố định (Mẫu S21-DN) – [Ghi chú: Biểu mẫu khung trắng phục vụ hoàn thiện hệ thống chứng từ kế toán, hiện tại isModuleAvailable: false và chưa có thuật toán tính khấu hao]; "
                "16. Báo cáo doanh số theo nhân viên; 17. Báo cáo kiểm kê và điều chỉnh kho."
            )

    # 5.4. Bổ sung các màn hình còn thiếu (4.2.17 -> 4.2.20) trước Mục 4.3
    p_43_heading = None
    for child in body:
        if isinstance(child, CT_P):
            p = docx.text.paragraph.Paragraph(child, doc)
            if "4.3. Các thành phần giao diện dùng chung" in p.text:
                p_43_heading = child
                break

    if p_43_heading is not None:
        print("  Adding missing screens 4.2.17 to 4.2.20 before Section 4.3...")
        screens_to_add = [
            ("4.2.17. Màn hình Đổi trả hàng (ReturnPage)", [
                "Màn hình Đổi trả hàng phục vụ nhân viên bán hàng và thủ kho trong việc tiếp nhận và xử lý hàng hóa khách hàng mang trả lại.",
                "Giao diện bao gồm thanh tra cứu hóa đơn bán lẻ gốc, bảng chi tiết các sản phẩm trong hóa đơn, ô nhập số lượng trả, tình trạng sản phẩm (nguyên vẹn hay hư hỏng) và lý do đổi trả. Phía dưới hiển thị tổng tiền hoàn trả và phương thức hoàn tiền.",
                "⟦ Ảnh chụp minh họa thực tế: Giao diện màn hình Đổi trả hàng ⟧",
                "Hình 4.2.17. Giao diện màn hình Đổi trả hàng",
                "Nhân viên tra cứu hóa đơn, chọn mặt hàng cần trả, nhập số lượng và lý do, sau đó bấm 'Tạo phiếu trả hàng' để hệ thống tự động nhập kho lại hàng hóa và ghi nhận chi tiền hoàn lại cho khách."
            ]),
            ("4.2.18. Màn hình Quản lý Công nợ Nhà cung cấp (DebtsPage)", [
                "Màn hình Quản lý Công nợ giúp kế toán theo dõi chi tiết các khoản nợ phải trả phát sinh từ các đợt nhập hàng của nhà cung cấp.",
                "Giao diện hiển thị bảng danh sách các khoản nợ với các cột: Mã công nợ, Nhà cung cấp, Phiếu nhập liên quan, Ngày phát sinh, Tổng tiền nợ, Số tiền đã trả, Dư nợ còn lại, Hạn thanh toán và Trạng thái nợ. Có nút 'Thanh toán' nhanh cho từng khoản nợ.",
                "⟦ Ảnh chụp minh họa thực tế: Giao diện màn hình Quản lý Công nợ ⟧",
                "Hình 4.2.18. Giao diện màn hình Quản lý Công nợ Nhà cung cấp",
                "Kế toán lọc theo nhà cung cấp hoặc trạng thái nợ, bấm 'Thanh toán' để mở hộp thoại trả nợ, nhập số tiền thanh toán và phương thức chi, hệ thống tự động sinh phiếu chi và giảm trừ công nợ tức thì."
            ]),
            ("4.2.19. Màn hình Quản lý Khuyến mại & Mã giảm giá (PromotionsPage)", [
                "Màn hình Khuyến mại cho phép thiết lập và quản lý các chương trình ưu đãi, voucher giảm giá phục vụ kích cầu bán lẻ.",
                "Giao diện bao gồm bảng danh sách mã khuyến mại, mức giảm giá (theo % hoặc số tiền cố định), điều kiện giá trị đơn hàng tối thiểu, thời gian hiệu lực và số lần đã sử dụng. Có form tạo mới chương trình khuyến mại linh hoạt.",
                "⟦ Ảnh chụp minh họa thực tế: Giao diện màn hình Quản lý Khuyến mại ⟧",
                "Hình 4.2.19. Giao diện màn hình Quản lý Khuyến mại",
                "Người quản lý thiết lập các mã khuyến mại hoặc theo dõi các mã voucher phát sinh từ chương trình tích điểm khách hàng thân thiết (BAC50K, VANG100K, KC200K)."
            ]),
            ("4.2.20. Màn hình Quản trị Hệ thống: Nhật ký kiểm toán & Sao lưu dữ liệu", [
                "Bao gồm hai phân hệ quản trị cấp cao dành cho Quản trị viên: Nhật ký kiểm toán (AuditLogPage) và Sao lưu dữ liệu (BackupPage).",
                "AuditLogPage hiển thị toàn bộ lịch sử 16 mã hành động tác động vào hệ thống (thời gian, người thực hiện, vai trò, địa chỉ IP, hành động và dữ liệu thay đổi). BackupPage quản lý danh sách các tệp sao lưu JSON snapshot và cung cấp nút Sao lưu ngay và Phục hồi dữ liệu.",
                "⟦ Ảnh chụp minh họa thực tế: Giao diện màn hình Nhật ký kiểm toán và Sao lưu ⟧",
                "Hình 4.2.20. Giao diện màn hình Nhật ký kiểm toán và Sao lưu dữ liệu",
                "Quản trị viên giám sát an toàn thông tin, phát hiện các hành vi bất thường qua Audit Log và thực hiện sao lưu CSDL định kỳ hoặc phục hồi dữ liệu khi có sự cố."
            ])
        ]
        for title, lines in screens_to_add:
            p_title = doc.add_paragraph()
            p_title.style = "Heading 3"
            r = p_title.add_run(title)
            r.font.name = "Times New Roman"
            p_43_heading.addprevious(p_title._p)

            for line in lines:
                p_line = doc.add_paragraph()
                p_line.style = "Normal"
                r = p_line.add_run(line)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                p_43_heading.addprevious(p_line._p)

            p_sep = doc.add_paragraph()
            p_43_heading.addprevious(p_sep._p)

    # =========================================================================
    # PHẦN 6: KẾT LUẬN & HƯỚNG PHÁT TRIỂN & PHỤ LỤC (YÊU CẦU C)
    # =========================================================================
    print("--- 6. Updating Conclusion, Future Work, and Appendices ---")
    
    # 6.1. Cập nhật Kết luận (P850 - P875)
    for p in doc.paragraphs[845:875]:
        t = p.text
        # 24 ca sử dụng -> 27 ca sử dụng
        if "24 ca sử dụng" in t:
            p.text = t.replace("24 ca sử dụng (Use Case) chi tiết", "27 ca sử dụng (Use Case) chi tiết (bổ sung Quản lý Đổi trả hàng, Tích điểm & Đổi voucher, Sao lưu & Phục hồi dữ liệu)")
        # 25 collection chuyên biệt -> 31 collection (bao gồm Users)
        if "25 collection" in t:
            p.text = (
                "Về mặt cơ sở dữ liệu: Thiết kế cấu trúc CSDL NoSQL MongoDB gồm 31 collection (bao gồm Users) chuẩn hóa tiếng Việt, "
                "sử dụng Native MongoDB Driver ^7.5.0. Thiết lập hệ thống chỉ mục (Index) tối ưu, cơ chế toàn vẹn dữ liệu kết hợp tầng Controller validation "
                "và Database Index, hỗ trợ tự động sinh mã chứng từ tuần tự qua bộ đếm Counters và cơ chế lưu trữ kép chi tiết chứng từ (Dual-Storage)."
            )
        # Sửa mã QR tĩnh -> VietQR động NAPAS
        if "mã QR tĩnh" in t:
            p.text = (
                "Hệ thống đã hỗ trợ mã thanh toán VietQR động chuẩn NAPAS sinh tự động theo số tiền hóa đơn, "
                "tuy nhiên chưa kết nối trực tiếp cổng Webhook ngân hàng thương mại để tự động gạch nợ tức thì khi tiền về tài khoản ngân hàng."
            )

    # 6.2. Bổ sung máy quét mã vạch và máy in nhiệt POS vào Hướng phát triển
    p_ref_heading = None
    for child in body:
        if isinstance(child, CT_P):
            p = docx.text.paragraph.Paragraph(child, doc)
            if "TÀI LIỆU THAM KHẢO" in p.text:
                p_ref_heading = child
                break

    if p_ref_heading is not None:
        print("  Adding hardware integration to Future Work...")
        hw_p = doc.add_paragraph()
        hw_p.style = "Normal"
        r = hw_p.add_run(
            "Tích hợp thiết bị phần cứng ngoại vi: Mở rộng khả năng kết nối trực tiếp với máy quét mã vạch chuyên dụng (Barcode Scanner) "
            "và máy in nhiệt POS khổ 80mm qua giao tiếp USB/HID nhằm tăng tốc hơn nữa quy trình quét hàng bán lẻ tại quầy thu ngân và khâu xuất nhập kiểm kê kho."
        )
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        p_ref_heading.addprevious(hw_p._p)

    # 6.3. Cập nhật Phụ lục A & B trong các bảng
    # Table 41: Xóa "quét mã vạch/QR" -> "thanh toán mã VietQR động NAPAS"
    t41 = doc.tables[41]
    for r in t41.rows:
        for c in r.cells:
            if "quét mã vạch/QR" in c.text:
                c.text = c.text.replace("quét mã vạch/QR", "thanh toán mã VietQR động NAPAS")
                for p in c.paragraphs:
                    for run in p.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(9.5)

    # Table 43: Sửa "25 collection" -> "31 collection CSDL MongoDB"
    t43 = doc.tables[43]
    for r in t43.rows:
        for c in r.cells:
            if "25 collection" in c.text:
                c.text = c.text.replace("25 collection", "31 collection CSDL MongoDB")
                for p in c.paragraphs:
                    for run in p.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(9.5)

    # Table 40: Cập nhật dòng Kho và dòng Nâng cao
    t40 = doc.tables[40]
    if len(t40.rows) >= 9:
        t40.rows[6].cells[2].text = "UC20 – UC22, UC25"
        t40.rows[6].cells[4].text = "InventoryPage; StocktakePage; ReturnPage"
        t40.rows[8].cells[2].text = "UC26 – UC27"
        t40.rows[8].cells[4].text = "Tìm kiếm nhanh; Lọc dữ liệu; Phân trang; In hóa đơn theo mẫu kế toán; Xuất Excel (.xls XML)/CSV; Thống kê biểu đồ SVG; Thanh toán VietQR động chuẩn NAPAS; Gửi email hóa đơn; Tích điểm & Đổi voucher (CustomersPage); Nhật ký kiểm toán (AuditLogPage); Sao lưu và phục hồi dữ liệu (BackupPage)."
        for r in [t40.rows[6], t40.rows[8]]:
            style_row(r, font_size=9.5)

    # Lưu kết quả ra baocaobtl_fixed.docx
    output_filename = "baocaobtl_fixed.docx"
    print(f"Saving changes to {output_filename}...")
    doc.save(output_filename)
    print("SUCCESS: Phase 2 completed successfully!")

if __name__ == "__main__":
    main()
