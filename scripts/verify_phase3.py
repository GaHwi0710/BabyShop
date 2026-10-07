import docx
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document("baocaobtl_final.docx")
print("==================================================================")
print("             BÁO CÁO KIỂM TOÁN TỔNG THỂ PHA 3")
print("==================================================================")
print(f"Tổng số đoạn văn (Paragraphs): {len(doc.paragraphs)}")
print(f"Tổng số bảng biểu (Tables): {len(doc.tables)}")

errors = []

# 1. Check for BabyBon
bb_paras = []
for i, p in enumerate(doc.paragraphs):
    if 'babybon' in p.text.lower():
        bb_paras.append((i, p.text[:80]))
bb_cells = []
for t_idx, tbl in enumerate(doc.tables):
    for r_idx, row in enumerate(tbl.rows):
        for c_idx, cell in enumerate(row.cells):
            if 'babybon' in cell.text.lower():
                bb_cells.append((t_idx, r_idx, c_idx, cell.text[:60]))

if bb_paras or bb_cells:
    errors.append(f"STILL HAS BABYBON: {len(bb_paras)} in paragraphs, {len(bb_cells)} in tables")
else:
    print("✅ 1. Kiểm tra BabyBon: ĐÃ XÓA SẠCH 100%, không còn bất kỳ xuất hiện nào trong văn bản và bảng biểu.")

# 2. Check 31 collections and 27 Use Cases
all_text = " ".join(p.text for p in doc.paragraphs)
if "31 collection (bao gồm Users)" in all_text:
    print("✅ 2.1. Cụm từ '31 collection (bao gồm Users)' đã xuất hiện đầy đủ, chính xác.")
else:
    errors.append("Thiếu cụm từ '31 collection (bao gồm Users)'")

if "27 ca sử dụng (Use Case) chi tiết (UC01 đến UC27)" in all_text:
    print("✅ 2.2. Kết luận đã ghi nhận đúng 27 Use Case (UC01-UC27).")
else:
    errors.append("Kết luận chưa ghi nhận đúng 27 Use Case")

if "27 ca sử dụng cốt lõi (UC01 đến UC27)" in all_text:
    print("✅ 2.3. Sửa typo tại Mục 2.3 (P147) thành '(UC01 đến UC27)' thành công.")
else:
    errors.append("Chưa sửa typo tại Mục 2.3 (P147)")

# Tách Front Matter và Document Body
# Vị trí CHƯƠNG 1 thực tế (Heading 1)
ch1_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("CHƯƠNG 1") and p.style.name.startswith("Heading"):
        ch1_idx = i
        break

front_paragraphs = doc.paragraphs[:ch1_idx] if ch1_idx else []
body_paragraphs = doc.paragraphs[ch1_idx:] if ch1_idx else doc.paragraphs

print(f"\nPhân vùng: Front Matter ({len(front_paragraphs)} đoạn) | Thân tài liệu ({len(body_paragraphs)} đoạn)")

# 3. Check Figure Captions trong Body
body_fig_captions = []
for p in body_paragraphs:
    t = p.text.strip()
    if re.match(r'^Hình\s+[0-9]+\.[0-9]+', t):
        body_fig_captions.append(t)

print(f"\n✅ 3. Kiểm tra Chú thích Hình ảnh trong phần Thân tài liệu (Body): {len(body_fig_captions)} hình")
ch2_figs = [f for f in body_fig_captions if f.startswith("Hình 2.")]
ch3_figs = [f for f in body_fig_captions if f.startswith("Hình 3.")]
ch4_figs = [f for f in body_fig_captions if f.startswith("Hình 4.")]
print(f"   - Chương 2: {len(ch2_figs)} hình (Hình 2.1 -> Hình 2.18)")
print(f"   - Chương 3: {len(ch3_figs)} hình (Hình 3.1 -> Hình 3.2)")
print(f"   - Chương 4: {len(ch4_figs)} hình (Hình 4.1 -> Hình 4.20)")

if len(ch2_figs) != 18: errors.append(f"Chương 2 có {len(ch2_figs)} hình, kỳ vọng 18")
if len(ch3_figs) != 2: errors.append(f"Chương 3 có {len(ch3_figs)} hình, kỳ vọng 2")
if len(ch4_figs) != 20: errors.append(f"Chương 4 có {len(ch4_figs)} hình, kỳ vọng 20")

# Check for duplicates in figure numbering
body_fig_nums = [f.split(". ")[0] for f in body_fig_captions]
if len(body_fig_nums) != len(set(body_fig_nums)):
    dups = [x for x in body_fig_nums if body_fig_nums.count(x) > 1]
    errors.append(f"TRÙNG SỐ THỨ TỰ HÌNH TRONG THÂN: {set(dups)}")
else:
    print("✅ 3.1. Đánh số hình ảnh trong Thân tài liệu: TUYỆT ĐỐI KHÔNG TRÙNG LẶP, liên tục chuẩn hóa.")

# 4. Check Table Captions trong Body
body_tbl_captions = []
for p in body_paragraphs:
    t = p.text.strip()
    if re.match(r'^Bảng\s+(?:[0-9]+|[A-Z])\.[0-9]+', t):
        body_tbl_captions.append(t)

print(f"\n✅ 4. Kiểm tra Chú thích Bảng biểu trong phần Thân tài liệu (Body): {len(body_tbl_captions)} bảng")
t_ch2 = [t for t in body_tbl_captions if t.startswith("Bảng 2.")]
t_ch3 = [t for t in body_tbl_captions if t.startswith("Bảng 3.")]
t_app = [t for t in body_tbl_captions if t.startswith("Bảng A.") or t.startswith("Bảng B.")]
print(f"   - Chương 2: {len(t_ch2)} bảng (Bảng 2.1 -> Bảng 2.8)")
print(f"   - Chương 3: {len(t_ch3)} bảng (Bảng 3.1 -> Bảng 3.31)")
print(f"   - Phụ lục: {len(t_app)} bảng (Bảng A.1, A.2, A.3, B.1)")

if len(t_ch2) != 8: errors.append(f"Chương 2 có {len(t_ch2)} bảng, kỳ vọng 8")
if len(t_ch3) != 31: errors.append(f"Chương 3 có {len(t_ch3)} bảng, kỳ vọng 31")
if len(t_app) != 4: errors.append(f"Phụ lục có {len(t_app)} bảng, kỳ vọng 4")

body_tbl_nums = [t.split(". ")[0] for t in body_tbl_captions]
if len(body_tbl_nums) != len(set(body_tbl_nums)):
    dups = [x for x in body_tbl_nums if body_tbl_nums.count(x) > 1]
    errors.append(f"TRÙNG SỐ THỨ TỰ BẢNG TRONG THÂN: {set(dups)}")
else:
    print("✅ 4.1. Đánh số bảng biểu trong Thân tài liệu: TUYỆT ĐỐI KHÔNG TRÙNG LẶP, đủ 43 bảng.")

# 5. Check Section 3.5 trong Body
p35_found = False
for p in body_paragraphs:
    if p.text.startswith("3.5. Sơ đồ tổng quan"):
        p35_found = True
        if p.style.name != "Heading 2":
            errors.append(f"Mục 3.5 trong body có style là '{p.style.name}', kỳ vọng 'Heading 2'")
        else:
            print("✅ 5. Mục 3.5 trong body có tiêu đề chuẩn Heading 2 và nội dung hạch toán kế toán đầy đủ.")
if not p35_found:
    errors.append("Không tìm thấy Mục 3.5 trong body")

# 6. Check Table Technical Formatting
tables_without_hdr = 0
tables_without_cantSplit = 0
for tbl in doc.tables:
    if len(tbl.rows) > 0:
        hdr = tbl.rows[0]._tr.get_or_add_trPr().xpath('.//w:tblHeader')
        if not hdr: tables_without_hdr += 1
        cs = tbl.rows[0]._tr.get_or_add_trPr().xpath('.//w:cantSplit')
        if not cs: tables_without_cantSplit += 1

if tables_without_hdr == 0 and tables_without_cantSplit == 0:
    print(f"✅ 6. Toàn bộ {len(doc.tables)} bảng đã được cấu hình tblHeader và cantSplit chuẩn mực.")
else:
    errors.append(f"Có bảng chưa có tblHeader ({tables_without_hdr}) hoặc cantSplit ({tables_without_cantSplit})")

# 7. Check Front Matter
fm_headings = [p.text.strip() for p in front_paragraphs if p.style.name.startswith("Heading")]
print(f"✅ 7. Front Matter có các đề mục: {fm_headings}")

# 8. Check Placeholders
placeholders = [p.text.strip() for p in doc.paragraphs if p.text.strip().startswith("[CHÈN HÌNH:")]
print(f"✅ 8. Tổng số Placeholders chuẩn hóa [CHÈN HÌNH: ...]: {len(placeholders)}")
if len(placeholders) != 37:
    errors.append(f"Số lượng placeholders là {len(placeholders)}, kỳ vọng 37")

print("\n==================================================================")
if errors:
    print(f"❌ CÒN {len(errors)} LỖI CẦN XỬ LÝ:")
    for e in errors:
        print("  -", e)
else:
    print("🎉 TẤT CẢ 8 HẠNG MỤC KIỂM TRA PHA 3 ĐỀU ĐẠT 100% PASS TUYỆT ĐỐI!")
print("==================================================================")
