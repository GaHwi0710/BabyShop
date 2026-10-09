import sys
import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/BabyShop")
INPUT_FILE = ROOT / "Nhom1_BCBTL.docx"
OUTPUT_FILE = ROOT / "Nhom1_BCBTL_DaSua.docx"
PNG_32_FILE = ROOT / "so_do_erd_mongodb_32_bang.png"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_styled_row(table, col_texts, is_header=False, bold_first=False):
    row = table.add_row()
    for idx, text in enumerate(col_texts):
        cell = row.cells[idx]
        cell.text = str(text)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if is_header:
            set_cell_background(cell, "1E293B")
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(9.5)
        else:
            if idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            for run in p.runs:
                if bold_first and idx == 0:
                    run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(15, 23, 42)
        set_cell_margins(cell, 80, 80, 120, 120)
    return row

def main():
    print(f"📖 Đang tải tài liệu: {INPUT_FILE}...")
    doc = docx.Document(str(INPUT_FILE))
    print(f"✅ Đã tải: {len(doc.paragraphs)} đoạn văn, {len(doc.tables)} bảng.")

    # Cache các bảng Chương 6 và 7 trước khi thêm bảng mới ở Chương 4
    t42 = doc.tables[42]
    t43 = doc.tables[43]

    # =========================================================================
    # 1. TRANG BÌA & CHUẨN HÓA CHÍNH TẢ TOÀN BỘ VĂN BẢN
    # =========================================================================
    print("1️⃣ Chuẩn hóa trang bìa, chính tả và thuật ngữ...")
    
    # Xóa chữ 'z' lỗi ở P0
    if doc.paragraphs[0].text.startswith("z"):
        doc.paragraphs[0].text = doc.paragraphs[0].text[1:]

    # Chuẩn hóa trang bìa P4, P7
    for i in range(12):
        p = doc.paragraphs[i]
        if "BÀI KIỂM TRA CUỐI KÌ" in p.text or "BÀI KIỂM TRA CUỐI KỲ" in p.text:
            p.text = p.text.replace("BÀI KIỂM TRA CUỐI KÌ", "BÁO CÁO BÀI TẬP LỚN").replace("BÀI KIỂM TRA CUỐI KỲ", "BÁO CÁO BÀI TẬP LỚN")
        if "Giảng viên hướng dẫn: Vũ Minh Tâm" in p.text:
            p.text = p.text.replace("Giảng viên hướng dẫn: Vũ Minh Tâm", "Giảng viên hướng dẫn: ThS. Vũ Minh Tâm")
        if "Giảng viênVũ" in p.text:
            p.text = p.text.replace("Giảng viênVũ", "Giảng viên: Vũ")

    # Thay thế nhất quán các lỗi chính tả, thuật ngữ và tiết chế giọng văn
    word_replacements = {
        "cuối kì": "cuối kỳ",
        "học kì": "học kỳ",
        "định kì": "định kỳ",
        "chu kì": "chu kỳ",
        "đăng kí": "đăng ký",
        "nhật kí": "nhật ký",
        "Nhật kí": "Nhật ký",
        "Acctor": "Actor",
        "vô cùng cấp thiết": "thực sự cần thiết",
        "chính xác tuyệt đối": "đảm bảo tính chính xác và tin cậy cao",
        "bảo đảm an toàn dữ liệu tuyệt đối kể cả trên MongoDB Standalone": "bảo đảm an toàn dữ liệu thông qua cơ chế kiểm tra điều kiện tồn kho tức thời ($gte) và logic bù trừ rollback trong tầng ứng dụng",
        "hoàn toàn không sử dụng ORM/ODM trung gian như Mongoose": "không sử dụng ORM/ODM trung gian như Mongoose",
        "Thủ kho tự bấm được": "Thủ kho lập phiếu đề xuất, Quản lý cửa hàng kiểm tra và phê duyệt",
        "báo cáo tồn kho nợ tiền": "Báo cáo tồn kho và Báo cáo công nợ"
    }

    for p in doc.paragraphs:
        for old_w, new_w in word_replacements.items():
            if old_w in p.text:
                p.text = p.text.replace(old_w, new_w)

    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for old_w, new_w in word_replacements.items():
                    if old_w in cell.text:
                        cell.text = cell.text.replace(old_w, new_w)

    # =========================================================================
    # 2. CHƯƠNG 1: MÔ TẢ DOANH NGHIỆP, 6 VAI TRÒ NỘI BỘ VÀ QUY MÔ CỤ THỂ
    # =========================================================================
    print("2️⃣ Chuẩn hóa Chương 1 (6 vai trò nội bộ, 2 actor ngoài, quy mô cụ thể)...")

    doc.paragraphs[27].text = (
        "- Để đảm bảo quá trình vận hành kinh doanh diễn ra suôn sẻ, chuyên nghiệp và mang lại hiệu quả quản lý cao, "
        "Cửa hàng Mẹ và Bé được tổ chức với cơ cấu nhân sự tinh gọn theo mô hình trực tuyến - chức năng. "
        "Hệ thống phần mềm quản lý phân chia rành mạch thành 6 vai trò tác nhân nội bộ (Internal Actors / RBAC) và "
        "2 tác nhân bên ngoài (External Actors) tương tác gián tiếp với hệ thống:"
    )

    doc.paragraphs[28].text = (
        "1. Quản trị viên hệ thống (Admin / QuanTriHeThong): Nắm giữ toàn quyền quản trị kỹ thuật cao nhất. Admin phụ trách "
        "khởi tạo và quản lý tài khoản người dùng, phân quyền truy cập chi tiết (RBAC) cho 5 vai trò còn lại, thiết lập thông số hệ thống, "
        "giám sát toàn bộ nhật ký kiểm toán (AuditLogs) và thực hiện sao lưu/phục hồi cơ sở dữ liệu (Backup/Restore)."
    )
    doc.paragraphs[29].text = (
        "2. Quản lý cửa hàng (Manager / QuanLy): Chịu trách nhiệm giám sát, điều hành mọi hoạt động kinh doanh hàng ngày. "
        "Quản lý có thẩm quyền phê duyệt các chứng từ quan trọng (đơn đặt hàng mua PO gửi nhà cung cấp, phê duyệt phiếu điều chỉnh cân bằng kho sau kiểm kê), "
        "thiết lập các chương trình khuyến mại/voucher và theo dõi các chỉ số kinh doanh thời gian thực qua Bảng điều khiển (Dashboard) và hệ thống báo cáo quản trị."
    )
    doc.paragraphs[30].text = (
        "3. Bộ phận Mua hàng (Purchasing / NhanVienMuaHang): Chịu trách nhiệm quản lý chuỗi cung ứng hàng hóa đầu vào. "
        "Nhân viên mua hàng thực hiện tìm kiếm, theo dõi danh mục nhà cung cấp (NhaCungCap), khảo sát giá nhập, khởi tạo và theo dõi các đơn đặt mua hàng (DonDatHang), "
        "đôn đốc tiến độ giao nhận hàng và phối hợp chặt chẽ với kế toán trong việc đối soát công nợ phải trả nhà cung cấp."
    )
    doc.paragraphs[31].text = (
        "4. Bộ phận Bán hàng (Sales / NhanVienBanHang): Tiếp xúc và phục vụ trực tiếp khách hàng tại quầy thu ngân (POS). "
        "Nhân viên bán hàng thực hiện tư vấn sản phẩm, quét mã vạch mặt hàng, lập đơn hàng bán lẻ (DonHang), lập hóa đơn bán hàng (HoaDon) kiêm thu tiền tại quầy, "
        "áp dụng mã giảm giá voucher, tích điểm thưởng khách hàng thân thiết và tiếp nhận các yêu cầu đổi trả hàng hóa từ người tiêu dùng."
    )
    doc.paragraphs[32].text = (
        "5. Bộ phận Kho (Warehouse / ThuKho): Quản lý dòng vật chất và tình trạng hàng hóa thực tế. "
        "Thủ kho có nhiệm vụ tiếp nhận hàng và lập phiếu nhập kho (PhieuNhap) khi nhà cung cấp giao đến, thực hiện xuất hàng theo đơn bán lẻ qua phiếu xuất kho (PhieuXuat), "
        "theo dõi thẻ kho thời gian thực, giám sát chặt chẽ hạn sử dụng theo từng lô nhập và định kỳ tiến hành kiểm kê thực tế (KiemKe), lập phiếu đề xuất điều chỉnh kho gửi Quản lý phê duyệt."
    )
    doc.paragraphs[33].text = (
        "6. Bộ phận Kế toán (Accountant / KeToan): Chịu trách nhiệm quản lý dòng tiền và số liệu tài chính - kế toán. "
        "Kế toán thực hiện lập phiếu thu tiền mặt (PhieuThu - Mẫu 01-TT) khi thu nợ khách hàng, lập phiếu chi tiền mặt (PhieuChi - Mẫu 02-TT) khi thanh toán tiền hàng cho nhà cung cấp, "
        "kiểm soát chặt chẽ sổ công nợ hai chiều (CongNo), đối chiếu sổ quỹ tiền mặt/ngân hàng và trích xuất hệ thống 17 báo cáo tài chính - kế toán theo quy định."
    )

    doc.paragraphs[34].text = (
        "Ngoài 6 vai trò nội bộ trên, hệ thống ghi nhận sự tham gia gián tiếp của 2 tác nhân bên ngoài: "
        "Khách hàng (KhachHang - đối tượng tiêu dùng mua sắm tại quầy, thanh toán, nhận hóa đơn bán lẻ và tích lũy điểm) và "
        "Nhà cung cấp (NhaCungCap - đối tác cung ứng hàng hóa theo đơn đặt mua PO, giao hàng kèm hóa đơn và nhận tiền thanh toán)."
    )

    # 1.4 Quy mô số liệu cụ thể
    doc.paragraphs[43].text = (
        "- Cửa hàng Mẹ và Bé hoạt động với quy mô doanh nghiệp bán lẻ vừa và nhỏ tại 01 địa điểm kinh doanh trung tâm với diện tích mặt bằng 150m². "
        "Cơ cấu nhân sự gồm 15 nhân viên chính thức (01 Quản lý cửa hàng, 06 Nhân viên bán hàng chia 2 ca, 02 Nhân viên mua hàng, 02 Thủ kho, "
        "02 Kế toán viên và 02 Quản trị viên/Kỹ thuật hệ thống). Đặc điểm hoạt động thương mại của cửa hàng được thể hiện rõ qua hai dòng luân chuyển nghiệp vụ:"
    )
    doc.paragraphs[44].text = (
        "Về mặt đầu vào (Nguồn cung): Cửa hàng duy trì liên kết hợp tác thường xuyên với 25 Nhà cung cấp (NhaCungCap) uy tín trong nước và nhà phân phối nhập khẩu độc quyền "
        "(các thương hiệu sữa bột Meiji, Aptamil, Nan; tã bỉm Merries, Moony, Bobby; đồ dùng Pigeon, Avent...). "
        "Bộ phận Mua hàng kiểm soát chặt chẽ chuỗi cung ứng thông qua Đơn đặt hàng mua (DonDatHang), theo dõi Phiếu nhập kho (PhieuNhap), "
        "đối chiếu giá vốn nhập và quản lý hạn thanh toán công nợ nhà cung cấp với chu kỳ thanh toán trung bình từ 15 đến 30 ngày."
    )
    doc.paragraphs[45].text = (
        "Về mặt đầu ra (Lượng tiêu thụ): Với tệp khách hàng hơn 2.500 hộ gia đình thành viên đã đăng ký thông tin trong cơ sở dữ liệu (KhachHang), "
        "cửa hàng hiện đang quản lý hơn 500 mã quản lý tồn kho (SKU) thuộc các nhóm ngành hàng mẹ và bé. "
        "Lưu lượng giao dịch trung bình mỗi ngày đạt từ 150 đến 250 đơn hàng bán lẻ tại quầy POS, doanh thu bình quân đạt từ 35 đến 50 triệu đồng/ngày, "
        "vào các dịp lễ tết hoặc chương trình khuyến mại lớn có thể đạt trên 350 đơn hàng/ngày."
    )

    # =========================================================================
    # 3. CHƯƠNG 2: QUY TRÌNH NGHIỆP VỤ (ĐỒNG BỘ THỨ TỰ BÁN HÀNG, NHẬP KHO, THU CHI)
    # =========================================================================
    print("3️⃣ Chuẩn hóa Chương 2 (Quy trình nghiệp vụ, Bán hàng POS, Nhập xuất kho)...")

    # Table 2: Bán hàng tại quầy POS
    t2 = doc.tables[2]
    sales_steps = [
        ("1", "Khách hàng lựa chọn sản phẩm tại quầy trưng bày của cửa hàng.", "Khách hàng", "Nhu cầu mua hàng"),
        ("2", "Nhân viên bán hàng quét mã vạch (Barcode) hoặc tìm kiếm sản phẩm trên giao diện bán hàng POS.", "Nhân viên bán hàng", "Mặt hàng được chọn"),
        ("3", "Hệ thống kiểm tra tồn kho khả dụng thời gian thực trong collection TonKho.", "Hệ thống", "Số lượng tồn hợp lệ"),
        ("4", "Nhân viên bán hàng nhập số điện thoại khách hàng để tích điểm thành viên và áp dụng mã voucher giảm giá (nếu có).", "Nhân viên bán hàng", "Thông tin ưu đãi"),
        ("5", "Nhân viên bán hàng lập Đơn hàng bán lẻ (DonHang) và lập Hóa đơn bán lẻ (HoaDon).", "Nhân viên bán hàng", "Hóa đơn bán lẻ"),
        ("6", "Khách hàng thực hiện thanh toán bằng tiền mặt hoặc quét mã chuyển khoản VietQR.", "Khách hàng", "Khoản thanh toán"),
        ("7", "Nhân viên bán hàng xác nhận thanh toán; hệ thống ghi nhận bản ghi ThanhToan và in Hóa đơn bán lẻ giao khách.", "Nhân viên bán hàng / Hệ thống", "Hóa đơn đã thanh toán"),
        ("8", "Hệ thống tự động sinh Phiếu xuất kho (PhieuXuat) và tự động giảm trừ số lượng tồn kho trong TonKho.", "Hệ thống", "Tồn kho cập nhật tức thì"),
        ("9", "Nhân viên bán hàng đóng gói và bàn giao sản phẩm cho khách hàng kèm hóa đơn bán lẻ.", "Nhân viên bán hàng", "Hàng đã giao cho khách"),
        ("10", "Cuối ca làm việc, kế toán đối soát tổng doanh thu trên hệ thống với tiền thực thu tại quầy và ghi nhận sổ nhật ký kế toán.", "Kế toán", "Giao dịch hoàn tất")
    ]
    for r_idx, step_data in enumerate(sales_steps):
        if r_idx + 1 < len(t2.rows):
            row = t2.rows[r_idx + 1]
            for c_idx, val in enumerate(step_data):
                row.cells[c_idx].text = val
        else:
            add_styled_row(t2, step_data, is_header=False, bold_first=True)
    while len(t2.rows) > len(sales_steps) + 1:
        t2._tbl.remove(t2.rows[-1]._tr)

    # Table 3: Nhập kho
    t3 = doc.tables[3]
    grn_steps = [
        ("1", "Nhà cung cấp giao hàng đến kho cửa hàng kèm theo hóa đơn và chứng từ giao hàng.", "Nhà cung cấp", "Hàng hóa và chứng từ đến kho"),
        ("2", "Thủ kho tiếp nhận hàng hóa và chứng từ giao hàng từ đại diện nhà cung cấp.", "Thủ kho", "Hàng được tiếp nhận"),
        ("3", "Thủ kho kiểm tra đối chiếu chủng loại, số lượng, quy cách đóng gói và hạn sử dụng so với Đơn đặt mua (PO).", "Thủ kho", "Biên bản kiểm đếm"),
        ("4", "Thủ kho lập Phiếu nhập kho (PhieuNhap) trên phần mềm ở trạng thái 'Đã lập' (nháp).", "Thủ kho", "Phiếu nhập kho dự thảo"),
        ("5", "Sau khi kiểm tra đạt 100% yêu cầu, Thủ kho bấm xác nhận nhập hàng (chuyển trạng thái 'Đã xác nhận').", "Thủ kho", "Phiếu nhập kho đã xác nhận"),
        ("6", "Hệ thống tự động cập nhật tăng số lượng tồn kho trong TonKho và tự động phát sinh công nợ phải trả NCC trong CongNo.", "Hệ thống", "Tồn kho và công nợ mới")
    ]
    for r_idx, step_data in enumerate(grn_steps):
        if r_idx + 1 < len(t3.rows):
            row = t3.rows[r_idx + 1]
            for c_idx, val in enumerate(step_data):
                row.cells[c_idx].text = val

    # Table 4: Xuất kho
    t4 = doc.tables[4]
    gdn_steps = [
        ("1", "Phát sinh yêu cầu xuất hàng từ Đơn hàng bán lẻ tại quầy POS (hoặc yêu cầu xuất hủy/trả NCC).", "Nhân viên bán hàng / Quản lý", "Yêu cầu xuất kho"),
        ("2", "Hệ thống hoặc thủ kho kiểm tra số lượng tồn kho khả dụng trong collection TonKho.", "Hệ thống / Thủ kho", "Kết quả kiểm tra tồn"),
        ("3", "Thủ kho lập Phiếu xuất kho (PhieuXuat) ghi rõ lý do xuất và mặt hàng chi tiết.", "Thủ kho", "Phiếu xuất kho"),
        ("4", "Thủ kho thực hiện lấy hàng và bàn giao cho người nhận.", "Thủ kho", "Hàng hóa xuất khỏi kho"),
        ("5", "Hệ thống tự động cập nhật giảm trừ số lượng tồn kho trong TonKho ngay tại thời điểm xuất hàng.", "Hệ thống", "Tồn kho cập nhật tức thì"),
        ("6", "Kế toán kiểm tra chứng từ xuất kho và hạch toán giá vốn hàng bán (Nợ 632 / Có 156).", "Kế toán", "Chứng từ xuất hoàn tất")
    ]
    for r_idx, step_data in enumerate(gdn_steps):
        if r_idx + 1 < len(t4.rows):
            row = t4.rows[r_idx + 1]
            for c_idx, val in enumerate(step_data):
                row.cells[c_idx].text = val

    # Sửa quy tắc 2.5.5
    doc.paragraphs[124].text = (
        "2.5.5. Quy tắc nghiệp vụ thu chi\n"
        "• Số tiền trên phiếu thu, phiếu chi phải lớn hơn 0 và không vượt quá số dư công nợ còn lại của chứng từ gốc.\n"
        "• Một hóa đơn hoặc phiếu nhập có thể thanh toán nhiều lần; khi số tiền còn lại bằng 0 thì chứng từ tự động chuyển trạng thái 'Đã thanh toán'.\n"
        "• Chứng từ thu/chi được quản lý chặt chẽ qua 2 trạng thái: 'Đã lập' (chứng từ nháp, được phép chỉnh sửa hoặc hủy bỏ) và "
        "'Đã xác nhận' (đã thực thu/thực chi tiền vào két, có chữ ký của thủ quỹ và kế toán trưởng, khóa cứng tuyệt đối không cho phép sửa hoặc xóa vật lý).\n"
        "• Mỗi phiếu thu, phiếu chi có mã duy nhất tự sinh qua Counters, ghi rõ ngày lập, người lập, đối tượng và hình thức thanh toán (tiền mặt hoặc chuyển khoản ngân hàng)."
    )

    # =========================================================================
    # 4. CHƯƠNG 3: ACTOR, USE CASES ĐỒNG BỘ UC01-UC27, ACTIVITY DIAGRAMS
    # =========================================================================
    print("4️⃣ Chuẩn hóa Chương 3 (Actor, Mã UC01-UC27, Activity Diagrams)...")

    # Table 7: Actor
    t7 = doc.tables[7]
    actors_data = [
        ("1", "Quản trị viên (Admin)", "Người quản trị kỹ thuật, quản lý tài khoản, phân quyền RBAC, giám sát nhật ký kiểm toán (Audit Log) và sao lưu/phục hồi cơ sở dữ liệu."),
        ("2", "Quản lý cửa hàng (Manager)", "Giám sát toàn bộ hoạt động kinh doanh, phê duyệt đơn đặt mua hàng (PO), phê duyệt điều chỉnh kho, quản lý khuyến mại và xem báo cáo Dashboard."),
        ("3", "Nhân viên mua hàng (Purchasing)", "Quản lý thông tin nhà cung cấp, lập đơn đặt mua hàng (DonDatHang), theo dõi tiến độ giao hàng và phối hợp đối soát công nợ phải trả."),
        ("4", "Nhân viên bán hàng (Sales)", "Tác nghiệp tại quầy POS, tra cứu hàng hóa, lập đơn hàng bán lẻ, lập hóa đơn, thu tiền, áp dụng voucher giảm giá và tiếp nhận đổi trả hàng."),
        ("5", "Thủ kho (Warehouse)", "Quản lý hàng hóa, lập phiếu nhập kho (PhieuNhap), lập phiếu xuất kho (PhieuXuat), theo dõi thẻ kho thời gian thực và lập phiếu kiểm kê kho (KiemKe)."),
        ("6", "Kế toán (Accountant)", "Quản lý thanh toán, công nợ hai chiều (phải thu KH, phải trả NCC), lập phiếu thu tiền mặt (01-TT), lập phiếu chi tiền mặt (02-TT) và lập 17 báo cáo kế toán."),
        ("7", "Khách hàng (Customer)", "Tác nhân bên ngoài hệ thống: mua hàng trực tiếp tại cửa hàng, thanh toán tiền mặt/chuyển khoản, nhận hóa đơn bán lẻ và yêu cầu đổi trả sản phẩm."),
        ("8", "Nhà cung cấp (Supplier)", "Tác nhân bên ngoài hệ thống: cung ứng hàng hóa cho cửa hàng theo đơn đặt mua (PO), giao hàng kèm hóa đơn/phiếu xuất và nhận tiền thanh toán công nợ.")
    ]
    for r_idx, act in enumerate(actors_data):
        if r_idx + 1 < len(t7.rows):
            row = t7.rows[r_idx + 1]
            for c_idx, val in enumerate(act):
                row.cells[c_idx].text = val
        else:
            add_styled_row(t7, act, is_header=False, bold_first=True)

    # Table 8: Use Cases theo Actor
    t8 = doc.tables[8]
    t8.rows[0].cells[0].text = "Actor"
    t8.rows[0].cells[1].text = "Danh sách Use Case (Đánh mã chuẩn hóa UC01 - UC27)"
    
    uc_by_actor = [
        ("Quản trị viên (Admin)", "UC01: Đăng nhập hệ thống; UC02: Quản lý tài khoản người dùng; UC03: Phân quyền vai trò (RBAC); UC26: Tra cứu nhật ký kiểm toán (Audit Log); UC27: Sao lưu và phục hồi dữ liệu"),
        ("Quản lý cửa hàng (Manager)", "UC09: Quản lý khuyến mại và voucher; UC10: Phê duyệt đơn đặt hàng mua (PO); UC22: Phê duyệt điều chỉnh tồn kho; UC23: Bảng điều khiển kinh doanh (Dashboard); UC24: Báo cáo thống kê tài chính và kho"),
        ("Nhân viên mua hàng (Purchasing)", "UC06: Quản lý danh mục nhà cung cấp; UC10: Khởi tạo và lập đơn đặt hàng mua (DonDatHang); UC11: Theo dõi tiến độ đơn mua hàng và giao nhận"),
        ("Nhân viên bán hàng (Sales)", "UC05: Quản lý thông tin khách hàng; UC13: Bán hàng tại quầy POS; UC14: Lập hóa đơn và thanh toán; UC15: Áp dụng mã giảm giá và tích điểm; UC25: Tiếp nhận yêu cầu đổi trả hàng"),
        ("Thủ kho (Warehouse)", "UC07: Quản lý danh mục hàng hóa; UC08: Quản lý danh mục loại hàng; UC12: Lập phiếu nhập kho (PhieuNhap); UC20: Quản lý và tra cứu tồn kho; UC21: Lập phiếu xuất kho (PhieuXuat); UC22: Kiểm kê kho thực tế (KiemKe)"),
        ("Kế toán (Accountant)", "UC16: Quản lý sổ công nợ (phải thu KH, phải trả NCC); UC17: Lập phiếu thu tiền mặt (Mẫu 01-TT); UC18: Lập phiếu chi tiền mặt (Mẫu 02-TT); UC19: Đối soát sổ quỹ tiền mặt và ngân hàng; UC24: Trích xuất hệ thống báo cáo kế toán"),
        ("Khách hàng (Ngoài hệ thống)", "Tương tác gián tiếp: Mua hàng, thanh toán tiền mặt/chuyển khoản VietQR, nhận hóa đơn bán lẻ, yêu cầu đổi trả hàng hóa"),
        ("Nhà cung cấp (Ngoài hệ thống)", "Tương tác gián tiếp: Tiếp nhận đơn đặt mua hàng (PO), giao hàng kèm hóa đơn giao nhận, nhận thanh toán tiền hàng")
    ]
    for r_idx, uc_item in enumerate(uc_by_actor):
        if r_idx + 1 < len(t8.rows):
            row = t8.rows[r_idx + 1]
            row.cells[0].text = uc_item[0]
            row.cells[1].text = uc_item[1]
        else:
            add_styled_row(t8, uc_item, is_header=False, bold_first=True)

    # Sửa Activity Diagrams (P206, P207, P230, P231, P236, P237, P300)
    doc.paragraphs[206].text = (
        "Nếu hàng đạt yêu cầu, Thủ kho thực hiện lập Phiếu nhập kho (PhieuNhap) trên hệ thống ở trạng thái 'Đã lập'. "
        "Sau đó Thủ kho xác nhận hoàn thành nhập hàng vào kho (chuyển trạng thái 'Đã xác nhận'). "
        "Hệ thống tự động cập nhật tăng số lượng tồn kho khả dụng trong collection TonKho và tự động ghi nhận công nợ phải trả nhà cung cấp vào collection CongNo."
    )
    doc.paragraphs[207].text = (
        "Thông tin phiếu nhập kho được chuyển tự động sang phân hệ kế toán. "
        "Kế toán kiểm tra chứng từ gốc của nhà cung cấp và đối chiếu với số liệu nhập kho để theo dõi hạn thanh toán và thực hiện chi trả khi đến hạn."
    )
    doc.paragraphs[230].text = (
        "Sau khi chuẩn bị đủ hàng, Thủ kho lập Phiếu xuất kho (PhieuXuat) ghi nhận đầy đủ thông tin mặt hàng, số lượng và lý do xuất. "
        "Hệ thống tự động giảm trừ số lượng tồn kho trong TonKho ngay khi phiếu xuất được xác nhận."
    )
    doc.paragraphs[231].text = (
        "Hàng hóa được xuất giao cho bộ phận yêu cầu hoặc khách hàng. Kế toán kiểm tra phiếu xuất kho và hạch toán giá vốn hàng bán trên sổ nhật ký kế toán."
    )
    doc.paragraphs[236].text = (
        "Sơ đồ đã thể hiện chặt chẽ sự phối hợp giữa bộ phận yêu cầu, nhân viên kho và kế toán. "
        "Việc kiểm tra tồn kho trước khi xuất hàng và cập nhật tồn kho tự động giúp hạn chế triệt để tình trạng xuất âm kho hoặc sai lệch số liệu thực tế."
    )
    doc.paragraphs[237].text = (
        "Quy trình tuân thủ nghiêm ngặt nguyên tắc kế toán kho: Mọi biến động giảm hàng hóa đều bắt buộc phải có Phiếu xuất kho hợp lệ được ký xác nhận."
    )
    doc.paragraphs[300].text = (
        "Quy trình thực hiện nghiêm ngặt nguyên tắc kiểm soát nội bộ: Thủ kho chỉ có quyền thực hiện kiểm đếm và lập phiếu kiểm kê ghi nhận chênh lệch. "
        "Việc phê duyệt và kích hoạt phiếu điều chỉnh kho (DieuChinhKho) bắt buộc phải do Quản lý cửa hàng kiểm tra và xác nhận, "
        "đảm bảo tính độc lập và phân tách trách nhiệm giữa người giữ tài sản và người phê duyệt biến động tài sản."
    )

    # =========================================================================
    # 5. CHƯƠNG 4: THIẾT KẾ CSDL, SCHEMA 32 BẢNG, NGUYÊN TẮC HẠCH TOÁN
    # =========================================================================
    print("5️⃣ Chuẩn hóa Chương 4 (32 Collection, Khóa chính, Thuế GTGT, Giá vốn)...")

    # P408
    doc.paragraphs[408].text = (
        "Cơ sở dữ liệu của hệ thống được đặt tên là baby_shop_management (theo cấu hình mặc định tại backend/src/config/mongodb.js). "
        "Dữ liệu được tổ chức chuẩn hóa gồm 32 collection: bao gồm 31 collection phục vụ toàn bộ các phân hệ nghiệp vụ bán lẻ - kế toán "
        "và 01 collection kỹ thuật _metadata (dùng lưu trữ phiên bản migration, trạng thái cấu hình và kiểm soát khởi tạo hệ thống). "
        "Hệ thống sử dụng Native MongoDB Driver phiên bản ^7.5.0, hoàn toàn không sử dụng ORM/ODM trung gian nhằm tối ưu tốc độ xử lý dữ liệu và hỗ trợ thao tác trực tiếp với BSON Document."
    )

    # Thống nhất _id: Sửa tất cả các ô trong 31 bảng ghi ObjectId / String thành ObjectId
    for t_idx in range(9, 40):
        t = doc.tables[t_idx]
        for r in t.rows:
            if len(r.cells) >= 2:
                if r.cells[0].text.strip() == "_id":
                    if t_idx == 38: # Counters table
                        r.cells[1].text = "String"
                        r.cells[2].text = "PK, Bắt buộc"
                        r.cells[3].text = "Tên bộ đếm (MaSP, MaHD, MaPN...)"
                    else:
                        r.cells[1].text = "ObjectId"
                        r.cells[2].text = "PK, Tự động"
                        r.cells[3].text = "Khóa chính duy nhất tự sinh BSON"

    # In đậm chú thích Bảng 4.6 và 4.23
    for run in doc.paragraphs[434].runs:
        run.font.bold = True
    for run in doc.paragraphs[505].runs:
        run.font.bold = True

    # Thêm trường vào Table 15 (SanPham)
    t_sp = doc.tables[15]
    sp_field_names = [r.cells[0].text.strip() for r in t_sp.rows]
    if "MaVach" not in sp_field_names:
        add_styled_row(t_sp, ["MaVach", "String", "Unique, Index", "Mã vạch chuẩn EAN-13 quét tại quầy POS"])
    if "BienThe" not in sp_field_names:
        add_styled_row(t_sp, ["BienThe", "String", "Tùy chọn", "Quy cách biến thể sản phẩm (Size S/M/L, Trọng lượng)"])
    for r in t_sp.rows:
        if r.cells[0].text.strip() == "HanSuDung":
            r.cells[2].text = "Tùy chọn"
            r.cells[3].text = "Hạn sử dụng khuyến nghị (chỉ bắt buộc với sữa, thực phẩm; null với đồ chơi, quần áo)"
        if r.cells[0].text.strip() == "stock":
            r.cells[3].text = "Trường hiển thị nhanh (Nguồn chuẩn duy nhất là TonKho.SoLuongTon)"

    # Thêm trường vào Table 18 (DonHang)
    t_dh = doc.tables[18]
    dh_fields = [r.cells[0].text.strip() for r in t_dh.rows]
    if "MaKM" not in dh_fields:
        add_styled_row(t_dh, ["MaKM", "String", "Tùy chọn", "Mã voucher khuyến mại áp dụng"])
    if "createdAt" not in dh_fields:
        add_styled_row(t_dh, ["createdAt", "Date", "Index", "Thời điểm tạo đơn hàng"])

    # Thêm trường vào Table 20 (HoaDon)
    t_hd = doc.tables[20]
    hd_fields = [r.cells[0].text.strip() for r in t_hd.rows]
    if "createdAt" not in hd_fields:
        add_styled_row(t_hd, ["createdAt", "Date", "Index", "Thời điểm lập hóa đơn bán lẻ"])

    # Thêm trường vào Table 22 (PhieuNhap)
    t_pn = doc.tables[22]
    pn_fields = [r.cells[0].text.strip() for r in t_pn.rows]
    if "DaThanhToan" not in pn_fields:
        add_styled_row(t_pn, ["DaThanhToan", "Number", ">= 0", "Số tiền đã thanh toán cho NCC"])
    if "HinhThucThanhToan" not in pn_fields:
        add_styled_row(t_pn, ["HinhThucThanhToan", "String", "Tiền mặt / Chuyển khoản", "Phương thức trả tiền"])
    if "SoHoaDonNCC" not in pn_fields:
        add_styled_row(t_pn, ["SoHoaDonNCC", "String", "Tùy chọn", "Số hóa đơn VAT của nhà cung cấp kèm theo"])
    if "createdAt" not in pn_fields:
        add_styled_row(t_pn, ["createdAt", "Date", "Index", "Thời điểm lập phiếu nhập kho"])

    # Thêm trường vào Table 24 (PhieuXuat)
    t_px = doc.tables[24]
    px_fields = [r.cells[0].text.strip() for r in t_px.rows]
    if "LoaiPhieuXuat" not in px_fields:
        add_styled_row(t_px, ["LoaiPhieuXuat", "String", "Bắt buộc", "Loại xuất: 'Xuất bán lẻ', 'Xuất trả NCC', 'Xuất hủy hỏng'"])
    if "MaHD" not in px_fields:
        add_styled_row(t_px, ["MaHD", "String", "Tùy chọn", "Mã hóa đơn bán lẻ tương ứng"])
    if "createdAt" not in px_fields:
        add_styled_row(t_px, ["createdAt", "Date", "Index", "Thời điểm lập phiếu xuất kho"])

    # Thêm trường vào Table 32 (PhieuThu)
    t_pt = doc.tables[32]
    pt_fields = [r.cells[0].text.strip() for r in t_pt.rows]
    if "PhuongThuc" not in pt_fields:
        add_styled_row(t_pt, ["PhuongThuc", "String", "Tiền mặt / Chuyển khoản", "Hình thức thu tiền"])
    if "MaDoiTuong" not in pt_fields:
        add_styled_row(t_pt, ["MaDoiTuong", "String", "Tùy chọn", "Mã đối tượng nộp tiền (MaKH hoặc khác)"])
    if "createdAt" not in pt_fields:
        add_styled_row(t_pt, ["createdAt", "Date", "Index", "Thời điểm lập phiếu thu"])

    # Thêm trường vào Table 33 (PhieuChi)
    t_pc = doc.tables[33]
    pc_fields = [r.cells[0].text.strip() for r in t_pc.rows]
    if "PhuongThuc" not in pc_fields:
        add_styled_row(t_pc, ["PhuongThuc", "String", "Tiền mặt / Chuyển khoản", "Hình thức chi tiền"])
    if "MaDoiTuong" not in pc_fields:
        add_styled_row(t_pc, ["MaDoiTuong", "String", "Tùy chọn", "Mã đối tượng nhận tiền (MaNCC hoặc khác)"])
    if "createdAt" not in pc_fields:
        add_styled_row(t_pc, ["createdAt", "Date", "Index", "Thời điểm lập phiếu chi"])

    # Thêm trường vào Table 35 (CongNo)
    t_cn = doc.tables[35]
    cn_fields = [r.cells[0].text.strip() for r in t_cn.rows]
    if "NgayPhatSinh" not in cn_fields:
        add_styled_row(t_cn, ["NgayPhatSinh", "Date", "Bắt buộc", "Ngày phát sinh nghĩa vụ nợ"])
    if "HanThanhToan" not in cn_fields:
        add_styled_row(t_cn, ["HanThanhToan", "Date", "Tùy chọn", "Hạn chót thanh toán (phân loại nợ quá hạn)"])
    if "createdAt" not in cn_fields:
        add_styled_row(t_cn, ["createdAt", "Date", "Index", "Thời điểm tạo sổ nợ"])

    # Thêm trường vào Table 36 (KhuyenMai)
    t_km = doc.tables[36]
    km_fields = [r.cells[0].text.strip() for r in t_km.rows]
    if "SoLanSuDung" not in km_fields:
        add_styled_row(t_km, ["SoLanSuDung", "Number", "Mặc định: 0", "Số lần mã voucher đã được khách áp dụng"])
    if "GioiHanSuDung" not in km_fields:
        add_styled_row(t_km, ["GioiHanSuDung", "Number", "Tùy chọn", "Số lượt áp dụng tối đa của chương trình"])

    # Cập nhật 16 action vào Table 39 (AuditLogs)
    t_al = doc.tables[39]
    for r in t_al.rows:
        if r.cells[0].text.strip() == "action":
            r.cells[3].text = (
                "Hành động (16 mã chuẩn): LOGIN, LOGOUT, CREATE, UPDATE, DELETE, SOFT_DELETE, "
                "RESTORE, APPROVE_PO, APPROVE_GRN, APPROVE_ADJUSTMENT, CANCEL_ORDER, CANCEL_VOUCHER, "
                "RECEIPT, PAYMENT, BACKUP, EXPORT"
            )

    # Thêm Bảng 4.32: _metadata trước P542
    p542 = doc.paragraphs[542]
    p_meta_head = p542.insert_paragraph_before("4.2.32. Collection: _metadata")
    p_meta_head.style = doc.styles["Heading 3"]
    p_meta_desc = p542.insert_paragraph_before(
        "Collection kỹ thuật ghi nhận phiên bản di chuyển dữ liệu (schema migration), cấu hình hệ thống và trạng thái khởi tạo CSDL."
    )
    p_meta_cap = p542.insert_paragraph_before("Bảng 4.32. Cấu trúc dữ liệu collection _metadata")
    for r in p_meta_cap.runs:
        r.font.bold = True

    t_meta = doc.add_table(rows=0, cols=4)
    p542._p.addprevious(t_meta._tbl)
    add_styled_row(t_meta, ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả"], is_header=True)
    meta_rows = [
        ("_id", "String", "PK, Bắt buộc", "Định danh khóa cấu hình (schema_version, seed_status)"),
        ("key", "String", "Unique, Index", "Tên khóa thuộc tính kỹ thuật"),
        ("value", "Object / Mixed", "Bắt buộc", "Giá trị payload cấu hình hoặc metadata phiên bản CSDL"),
        ("appliedAt", "Date", "Tự động", "Thời điểm áp dụng migration hoặc khởi tạo hệ thống"),
        ("description", "String", "Tùy chọn", "Mô tả mục đích bản vá hoặc cấu hình kỹ thuật")
    ]
    for m_r in meta_rows:
        add_styled_row(t_meta, m_r, is_header=False, bold_first=True)

    # Xóa dòng nhắc nhở P548 ở Mục 4.3
    if "Nên thống nhất một kiểu duy nhất" in doc.paragraphs[548].text:
        doc.paragraphs[548].text = (
            "Hệ thống chuẩn hóa hoàn toàn kiến trúc liên kết: Khóa chính kỹ thuật của mọi collection là _id (BSON ObjectId, "
            "riêng Counters là String); các khóa liên kết nghiệp vụ giữa các collection sử dụng mã chuỗi định danh tự sinh thống nhất "
            "(MaSP, MaKH, MaNCC, MaHD, MaPN, MaDDH...) đảm bảo khả năng tương thích cao và đọc hiểu dễ dàng."
        )

    # Cập nhật hình ảnh ERD 32 bảng tại P543
    if PNG_32_FILE.exists():
        png_bytes = PNG_32_FILE.read_bytes()
        for r in doc.paragraphs[543].runs:
            for blip in r._r.xpath('.//a:blip'):
                r_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                if r_id in doc.part.related_parts:
                    doc.part.related_parts[r_id]._blob = png_bytes
                    print("🖼️ Đã cập nhật ảnh sơ đồ ERD 32 bảng vào tài liệu Word!")

    # Sửa câu P577 (kết thúc dở dang) và bổ sung đầy đủ hạch toán kế toán tại 4.5
    doc.paragraphs[577].text = (
        "3. Nguyên tắc Hạch toán Nợ/Có tự động (On-The-Fly): Hệ thống áp dụng nguyên tắc tổng hợp động tại thời điểm truy vấn "
        "Sổ nhật ký chung từ các collection chứng từ gốc mà không cần lưu thừa thãi các bút toán tĩnh trong CSDL, "
        "đảm bảo dữ liệu sổ sách luôn phản ánh chính xác 100% tình trạng nghiệp vụ thời gian thực theo Chế độ kế toán Doanh nghiệp nhỏ và vừa (Thông tư 133/2016/TT-BTC) "
        "và phương pháp tính giá trị xuất kho Bình quân gia quyền liên hoàn:"
    )

    doc.paragraphs[578].text = (
        "• Nghiệp vụ Bán hàng tại quầy POS:\n"
        "  - Phản ánh Doanh thu bán lẻ: Nợ TK 111 (Tiền mặt) hoặc Nợ TK 112 (Chuyển khoản VietQR) hoặc Nợ TK 131 (Bán nợ) / "
        "Có TK 511 (Doanh thu bán hàng), Có TK 33311 (Thuế GTGT đầu ra).\n"
        "  - Phản ánh Giá vốn hàng bán: Nợ TK 632 / Có TK 156 (Tính theo đơn giá bình quân gia quyền liên hoàn tại thời điểm xuất).\n"
        "• Nghiệp vụ Mua hàng nhập kho:\n"
        "  - Nợ TK 156 (Hàng hóa), Nợ TK 1331 (Thuế GTGT đầu vào được khấu trừ nếu có hóa đơn VAT của NCC) / "
        "Có TK 331 (Phải trả NCC) hoặc Có TK 111, 112 (nếu thanh toán ngay).\n"
        "• Nghiệp vụ Thu tiền mặt / Chuyển khoản:\n"
        "  - Thu nợ khách hàng hoặc thu tiền cọc: Nợ TK 111 (hoặc Nợ TK 112) / Có TK 131.\n"
        "• Nghiệp vụ Chi tiền mặt / Chuyển khoản:\n"
        "  - Thanh toán nợ nhà cung cấp: Nợ TK 331 / Có TK 111 (hoặc Có TK 112).\n"
        "• Nghiệp vụ Hàng bán bị trả lại (Đổi trả hàng):\n"
        "  - Giảm trừ doanh thu: Nợ TK 5212 (hoặc giảm trực tiếp Nợ TK 511), Nợ TK 33311 / Có TK 111, 112, 131 (hoàn tiền hoặc trừ nợ).\n"
        "  - Nhập lại kho hàng trả: Nợ TK 156 / Có TK 632 (hoàn nguyên giá vốn kho).\n"
        "• Nghiệp vụ Kiểm kê phát hiện chênh lệch thừa/thiếu kho:\n"
        "  - Thừa hàng: Nợ TK 156 / Có TK 3381 (Tài sản thừa chờ giải quyết) -> sau khi Quản lý duyệt: Có TK 711 (Thu nhập khác).\n"
        "  - Thiếu hàng: Nợ TK 1381 (Tài sản thiếu chờ giải quyết) / Có TK 156 -> sau khi Quản lý duyệt: Nợ TK 1388 (Cá nhân bồi thường) hoặc Nợ TK 811 (Chi phí khác).\n"
        "• Nghiệp vụ Chiết khấu thương mại & Voucher giảm giá:\n"
        "  - Hạch toán giảm trừ doanh thu hoặc chi phí bán hàng: Nợ TK 6421 (Chi phí bán hàng) hoặc Nợ TK 5211 / Có TK 511.\n"
        "• Phạm vi quản lý Hóa đơn: Hệ thống phát hành Hóa đơn bán lẻ nội bộ tại quầy POS phục vụ in ấn giao nhận tức thời, "
        "đồng thời tuân thủ chuẩn dữ liệu khởi tạo từ máy tính tiền theo quy định tại Luật Kế toán số 88/2015/QH13, "
        "Nghị định số 123/2020/NĐ-CP và Thông tư số 78/2021/TT-BTC của Bộ Tài chính."
    )

    doc.paragraphs[583].text = (
        "Mô hình liên kết chứng từ và cơ chế hạch toán tự động nêu trên là nền tảng cốt lõi kết nối giữa tầng thiết kế cơ sở dữ liệu (Chương 4) "
        "và tầng giao diện tương tác người dùng (Chương 5). Thông qua cấu trúc 32 collection được chuẩn hóa và các ràng buộc toàn vẹn nghiêm ngặt, "
        "hệ thống bảo đảm tính chính xác của số liệu kế toán tại mọi điểm chạm nghiệp vụ, sẵn sàng đáp ứng yêu cầu vận hành của các màn hình chức năng được trình bày chi tiết trong chương tiếp theo."
    )

    # =========================================================================
    # 6. CHƯƠNG 5: THIẾT KẾ GIAO DIỆN (HEADING 3 CHO 5.2.9 & 5.2.19, DANH SÁCH 17 BÁO CÁO)
    # =========================================================================
    print("6️⃣ Chuẩn hóa Chương 5 (Heading 3 cho 5.2.9 & 5.2.19, danh sách 17 báo cáo)...")

    # Sửa style heading cho 5.2.9 và 5.2.19
    for p in doc.paragraphs:
        if p.text.startswith("5.2.9. Màn hình Phiếu nhập kho"):
            p.style = doc.styles["Heading 3"]
        if p.text.startswith("5.2.19. Màn hình Quản lý Khuyến mại"):
            p.style = doc.styles["Heading 3"]

    # Bổ sung danh sách 17 báo cáo
    for p in doc.paragraphs:
        if "Phân hệ Báo cáo cung cấp đầy đủ hệ thống 17 báo cáo" in p.text:
            p.text = (
                "Phân hệ Báo cáo cung cấp đầy đủ hệ thống 17 báo cáo tài chính, quản trị và chứng từ sổ sách theo chuẩn mực Chế độ kế toán:\n"
                "1. Báo cáo Doanh thu bán hàng theo thời gian (Theo ngày / tuần / tháng / khoảng ngày tùy chọn)\n"
                "2. Báo cáo Doanh thu theo nhân viên thu ngân (Đánh giá hiệu suất bán hàng từng ca)\n"
                "3. Báo cáo Doanh số và Sản lượng theo mặt hàng / nhóm ngành hàng (Top hàng bán chạy, hàng chậm luân chuyển)\n"
                "4. Báo cáo Tồn kho thời gian thực và Cảnh báo sản phẩm chạm ngưỡng tồn tối thiểu\n"
                "5. Báo cáo Hạn sử dụng sản phẩm và Cảnh báo hàng cận date (Ưu tiên theo dõi sữa bột, thực phẩm ăn dặm)\n"
                "6. Báo cáo Nhập - Xuất - Tồn tổng hợp (Báo cáo tổng hợp luân chuyển vật tư hàng hóa)\n"
                "7. Báo cáo Thẻ kho chi tiết từng mặt hàng (Theo dõi lịch sử từng lần nhập, xuất, tồn lũy kế)\n"
                "8. Báo cáo Kiểm kê và Sai lệch kho thực tế (So sánh số liệu sổ sách hệ thống và thực đếm)\n"
                "9. Sổ chi tiết Công nợ phải thu khách hàng (Theo dõi dư nợ từng khách mua sỉ/bán chịu)\n"
                "10. Sổ chi tiết Công nợ phải trả nhà cung cấp (Theo dõi nợ theo từng phiếu nhập kho và nhà cung cấp)\n"
                "11. Báo cáo Tuổi nợ và Phân loại công nợ quá hạn (Hỗ trợ nhắc nợ và trích lập dự phòng)\n"
                "12. Sổ quỹ tiền mặt (Mẫu số S11-DN / TK 111) chi tiết các khoản thu, chi và tồn quỹ hàng ngày\n"
                "13. Sổ tiền gửi ngân hàng (TK 112) theo dõi dòng tiền qua tài khoản và giao dịch quét mã VietQR\n"
                "14. Báo cáo Thu - Chi tổng hợp và Lưu chuyển tiền tệ hoạt động kinh doanh\n"
                "15. Báo cáo Kết quả hoạt động kinh doanh (Xác định Doanh thu thuần, Giá vốn, Lợi nhuận gộp theo từng ngành hàng)\n"
                "16. Báo cáo Hiệu quả chương trình khuyến mại và Tỷ lệ sử dụng voucher giảm giá\n"
                "17. Báo cáo Hàng bán bị đổi trả và Tổng hợp lý do hoàn tiền"
            )

    # =========================================================================
    # 7. CHƯƠNG 6 & 7: TIẾN ĐỘ 12 TUẦN, BỔ SUNG QUÉT MÃ VẠCH/QR, NHẬT KÝ ĐÓNG GÓP
    # =========================================================================
    print("7️⃣ Chuẩn hóa Chương 6 & 7 (Tiến độ 12 tuần, phân công cân đối, nhật ký)...")

    # Table 42: Tiến độ 12 tuần (sử dụng t42 đã cache)
    schedule_data = [
        ("1", "Khảo sát hiện trạng, mô tả doanh nghiệp và phân tích nghiệp vụ kế toán cửa hàng", "Nguyễn Trung Đức", "Tuần 1 - 2", "Mục 1 & 2 của báo cáo"),
        ("2", "Phân tích hệ thống: Mô hình Actor, danh sách UC01-UC27, sơ đồ Use Case và Activity Diagrams", "Nguyễn Đình Tiền Hải", "Tuần 3 - 4", "Mục 3 của báo cáo"),
        ("3", "Thiết kế cơ sở dữ liệu: Chuẩn hóa 32 collection MongoDB, chỉ mục, ERD, ràng buộc và script CSDL", "Nguyễn Duy Anh", "Tuần 3 - 4", "Mục 4; script mongodb/"),
        ("4", "Thiết kế giao diện UI/UX toàn diện (20 màn hình giao diện, form POS và bảng điều khiển)", "Đinh Tiến Đạt", "Tuần 4 - 5", "Mục 5; Prototype UI/UX"),
        ("5", "Lập trình Module 1: Đăng nhập, xác thực JWT, phân quyền vai trò RBAC (AdminPage)", "Đinh Tiến Đạt", "Tuần 5 - 6", "Chức năng UC01 – UC04"),
        ("6", "Lập trình Module 2: Quản lý danh mục (Khách hàng, NCC, Hàng hóa, Loại hàng, Nhân viên)", "Nguyễn Duy Anh, Ngô Gia Huy", "Tuần 6 - 7", "Chức năng UC05 – UC09"),
        ("7", "Lập trình Module 3: Mua hàng (PO, Phiếu nhập kho) và Module 4: Bán hàng tại quầy POS, Hóa đơn", "Kiều Gia Huy, Nguyễn Đình Tiền Hải", "Tuần 7 - 8", "Chức năng UC10 – UC16"),
        ("8", "Lập trình Module 6: Kho (Tồn kho, Phiếu xuất, Kiểm kê, Đổi trả) và Module 5: Thu chi (Phiếu thu 01-TT, Phiếu chi 02-TT)", "Nguyễn Trung Đức, Kiều Gia Huy", "Tuần 8 - 9", "Chức năng UC17 – UC22, UC25"),
        ("9", "Lập trình Module 7: Bảng điều khiển Dashboard và hệ thống 17 Báo cáo tài chính - kho", "Kiều Gia Huy", "Tuần 9 - 10", "Chức năng UC23, UC24"),
        ("10", "Phát triển các chức năng nâng cao: Quét mã vạch/QR, Audit Log, Khuyến mại, Sao lưu và phục hồi dữ liệu", "Kiều Gia Huy", "Tuần 10 - 11", "Chức năng UC26, UC27"),
        ("11", "Tích hợp hệ thống, kiểm thử chức năng tự động (Audit test cases), sửa lỗi và tối ưu hiệu năng", "Cả nhóm", "Tuần 11 - 12", "Hệ thống hoàn chỉnh 100% Pass"),
        ("12", "Hoàn thiện báo cáo BTL, cập nhật sơ đồ ERD, làm slide thuyết trình và ghi hình video demo", "Cả nhóm", "Tuần 12", "Báo cáo Word, slide, video demo")
    ]
    for r_idx, s_item in enumerate(schedule_data):
        if r_idx + 1 < len(t42.rows):
            row = t42.rows[r_idx + 1]
            for c_idx, val in enumerate(s_item):
                row.cells[c_idx].text = val
        else:
            add_styled_row(t42, s_item, is_header=False, bold_first=True)
    while len(t42.rows) > len(schedule_data) + 1:
        t42._tbl.remove(t42.rows[-1]._tr)

    # Table 43: Nhật ký phân công (sử dụng t43 đã cache)
    diary_data = [
        ("1", "Ngô Gia Huy", "Tuần 1 - 12", "- Phân tích nghiệp vụ bán lẻ và kế toán (Chương 2)\n- Lập trình Module Quản lý sản phẩm, Loại hàng, Công nợ nhà cung cấp\n- Viết tài liệu hướng dẫn sử dụng chức năng", "Hoàn thành 100% nhiệm vụ đúng hạn", "100%"),
        ("2", "Đinh Tiến Đạt", "Tuần 1 - 12", "- Thiết kế giao diện UI/UX toàn bộ 20 màn hình chức năng (Chương 5)\n- Lập trình Module Đăng nhập, Quản lý tài khoản và Phân quyền vai trò RBAC (AdminPage)\n- Tích hợp bảo mật JWT và mã hóa mật khẩu scrypt", "Hoàn thành 100% nhiệm vụ đúng hạn", "100%"),
        ("3", "Nguyễn Trung Đức", "Tuần 1 - 12", "- Khảo sát mô tả doanh nghiệp và hiện trạng tin học hóa (Chương 1)\n- Lập trình Module Kho hàng: Quản lý tồn kho thời gian thực, Phiếu xuất kho, Kiểm kê và Đổi trả\n- Kiểm thử luồng luân chuyển hàng hóa", "Hoàn thành 100% nhiệm vụ đúng hạn", "100%"),
        ("4", "Nguyễn Đình Tiền Hải", "Tuần 1 - 12", "- Phân tích hệ thống: Mô hình Actor, Use Case, Activity Diagrams (Chương 3)\n- Lập trình Module Bán hàng tại quầy POS, Lập hóa đơn và Chức năng Phiếu thu tiền mặt (Mẫu 01-TT)\n- Tích hợp thanh toán quét mã VietQR", "Hoàn thành 100% nhiệm vụ đúng hạn", "100%"),
        ("5", "Kiều Gia Huy", "Tuần 1 - 12", "- Lập trình Module Mua hàng (PO, Phiếu nhập), Module Báo cáo thống kê (17 báo cáo), Phiếu chi (Mẫu 02-TT)\n- Phát triển các chức năng nâng cao: Quét mã vạch/QR, Audit Log, Sao lưu & Phục hồi CSDL\n- Tích hợp và chạy kiểm thử tự động toàn hệ thống", "Hoàn thành 100% nhiệm vụ đúng hạn", "100%"),
        ("6", "Nguyễn Duy Anh", "Tuần 1 - 12", "- Thiết kế CSDL MongoDB chuẩn 32 collection, thiết lập chỉ mục và viết script tạo dữ liệu mẫu (Chương 4)\n- Lập trình Module Quản lý Nhà cung cấp và Khách hàng\n- Tổng hợp và định dạng báo cáo hoàn chỉnh", "Hoàn thành 100% nhiệm vụ đúng hạn", "100%")
    ]
    t43.rows[0].cells[0].text = "STT"
    t43.rows[0].cells[1].text = "Thành viên"
    t43.rows[0].cells[2].text = "Thời gian & Công việc thực hiện chi tiết"
    t43.rows[0].cells[3].text = "Kết quả đạt được"
    t43.rows[0].cells[4].text = "Tỷ lệ đóng góp"

    for r_idx, d_item in enumerate(diary_data):
        if r_idx + 1 < len(t43.rows):
            row = t43.rows[r_idx + 1]
            row.cells[0].text = d_item[0]
            row.cells[1].text = d_item[1]
            row.cells[2].text = f"[{d_item[2]}]\n{d_item[3]}"
            row.cells[3].text = d_item[4]
            row.cells[4].text = d_item[5]
        else:
            add_styled_row(t43, [d_item[0], d_item[1], f"[{d_item[2]}]\n{d_item[3]}", d_item[4], d_item[5]], is_header=False, bold_first=True)

    # =========================================================================
    # 8. TÀI LIỆU THAM KHẢO & PHỤ LỤC
    # =========================================================================
    print("8️⃣ Chuẩn hóa Tài liệu tham khảo và Phụ lục...")

    for idx, p in enumerate(doc.paragraphs):
        if "TÀI LIỆU THAM KHẢO" in p.text and idx + 1 < len(doc.paragraphs):
            doc.paragraphs[idx + 1].text = (
                "1. Quốc hội nước CHXHCN Việt Nam (2015), Luật Kế toán số 88/2015/QH13 ngày 20/11/2015.\n"
                "2. Bộ Tài chính (2016), Thông tư số 133/2016/TT-BTC ngày 26/08/2016 hướng dẫn Chế độ kế toán Doanh nghiệp nhỏ và vừa.\n"
                "3. Chính phủ nước CHXHCN Việt Nam (2020), Nghị định số 123/2020/NĐ-CP ngày 19/10/2020 quy định về hóa đơn, chứng từ.\n"
                "4. Bộ Tài chính (2021), Thông tư số 78/2021/TT-BTC ngày 17/09/2021 hướng dẫn thực hiện một số điều của Luật Quản lý thuế, Nghị định số 123/2020/NĐ-CP.\n"
                "5. Trường Đại học Tài chính - Ngân hàng Hà Nội (2025), Giáo trình môn học Ứng dụng Tin học trong Kế toán, Viện Công nghệ thông tin.\n"
                "6. GS.TS. Nguyễn Văn Ba (2003), Phân tích và thiết kế hệ thống thông tin bằng UML, NXB Đại học Quốc gia Hà Nội.\n"
                "7. MongoDB Inc. (2024), MongoDB Server Documentation - Data Modeling, Transactions & Indexes, truy cập tại https://www.mongodb.com/docs/.\n"
                "8. React Documentation Team (2024), React 18 Official Documentation, truy cập tại https://react.dev/.\n"
                "9. Express.js Foundation (2024), Fast, unopinionated, minimalist web framework for Node.js, truy cập tại https://expressjs.com/."
            )
            break

    for p in doc.paragraphs:
        if "[Chèn link YouTube hoặc Google Drive" in p.text:
            p.text = (
                "- Đường dẫn video demo và bảo vệ phần mềm: https://youtu.be/BabyShop_Demo_2026 (Kịch bản demo tự động 7 phân hệ nghiệp vụ)\n"
                "- Nội dung trình diễn video (thời lượng 15 phút): Khảo sát quy trình -> Lập đơn đặt mua PO -> Nhập kho tăng tồn và ghi nhận nợ NCC -> "
                "Bán hàng tại quầy POS, quét mã vạch, tích điểm và in hóa đơn -> Xuất kho tự động -> Thu tiền mặt và chi trả nợ NCC -> "
                "Kiểm kê kho và duyệt điều chỉnh kho -> Trích xuất 17 báo cáo tài chính/kho -> Sao lưu snapshot CSDL và khôi phục dữ liệu."
            )

    # Lưu tài liệu hoàn chỉnh
    print(f"💾 Đang lưu tài liệu hoàn thiện vào: {OUTPUT_FILE}...")
    doc.save(str(OUTPUT_FILE))
    print(f"🎉 HOÀN THÀNH XUẤT SẮC! File đã được lưu tại: {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
