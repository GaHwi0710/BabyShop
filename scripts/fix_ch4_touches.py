import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('baocaobtl_fixed.docx')

print("Fixing Chapter 4 remaining touches...")

for i, p in enumerate(doc.paragraphs):
    # Fix 4.2.10 barcode text
    if "quét mã vạch hoặc chọn sản phẩm" in p.text:
        print(f"Fixing barcode in P{i}...")
        p.text = p.text.replace(
            "quét mã vạch hoặc chọn sản phẩm (Add products), tự động tính tổng tiền (Calculate total), áp dụng chiết khấu/giảm giá (Apply discount), và chọn phương thức thanh toán (Payment method).",
            "tìm kiếm nhanh và chọn sản phẩm (Add products), tự động tính tổng tiền (Calculate total), áp dụng voucher tích điểm hoặc chiết khấu (Apply discount), và chọn phương thức thanh toán (Tiền mặt, VietQR động NAPAS)."
        )
    if "và quét mã vạch giúp đẩy nhanh tốc độ thanh toán" in p.text:
        print(f"Fixing barcode in P{i}...")
        p.text = p.text.replace(
            "hỗ trợ phím tắt và quét mã vạch giúp đẩy nhanh tốc độ thanh toán. Hóa đơn sau khi lưu có thể in trực tiếp cho khách.",
            "hỗ trợ các phím tắt chuyên dụng (F2 mở POS, F9 báo cáo) giúp đẩy nhanh tốc độ thanh toán tại quầy. Hóa đơn sau khi lưu có thể in trực tiếp cho khách."
        )

    # Fix 4.2.16 heading and 17 reports description
    if p.text.strip() == "4.2.16. Màn hình Báo cáo":
        print(f"Fixing 4.2.16 heading in P{i}...")
        p.text = "4.2.16. Màn hình Hệ thống 17 Báo cáo Kế toán & Quản trị (ReportPage)"
    if "Cung cấp nhiều loại báo cáo hình thành (Report types): Doanh thu, Tồn kho, Công nợ, Mua hàng, Sổ quỹ" in p.text:
        print(f"Fixing 4.2.16 description in P{i}...")
        p.text = (
            "Phân hệ Báo cáo cung cấp đầy đủ hệ thống 17 báo cáo tài chính, quản trị và chứng từ sổ sách theo chuẩn mực Chế độ kế toán:\n"
            "1. Báo cáo doanh thu bán hàng; 2. Báo cáo nhập – xuất kho tổng hợp; 3. Báo cáo tồn kho (Nhập - Xuất - Tồn); 4. Báo cáo công nợ tổng hợp (NCC và Khách hàng); 5. Sổ quỹ thu – chi tiền mặt tổng hợp; "
            "6. Báo cáo thu tiền mặt độc lập (8 cột Mẫu 01-TT); 7. Báo cáo chi tiền mặt độc lập (8 cột Mẫu 02-TT); 8. Báo cáo nhập kho độc lập (11 cột Mẫu 01-VT); 9. Báo cáo xuất kho độc lập (11 cột Mẫu 02-VT); "
            "10. Báo cáo thu tiền chuyển khoản (Giấy báo Có); 11. Báo cáo chi tiền chuyển khoản (Ủy nhiệm chi); 12. Báo cáo kết quả hoạt động kinh doanh (Mẫu B 02 - DN); 13. Sổ chi tiết vật liệu, dụng cụ, sản phẩm, hàng hóa (Mẫu S10-DN); "
            "14. Sổ nhật ký chung (Mẫu S03a-DNN); 15. Sổ tài sản cố định (Mẫu S21-DN) – [Ghi chú: Biểu mẫu khung trắng phục vụ hoàn thiện hệ thống chứng từ kế toán, hiện tại isModuleAvailable: false và chưa có thuật toán tính khấu hao]; "
            "16. Báo cáo doanh số bán hàng theo nhân viên; 17. Báo cáo kiểm kê và điều chỉnh kho."
        )

doc.save('baocaobtl_fixed.docx')
print("Successfully saved baocaobtl_fixed.docx!")
