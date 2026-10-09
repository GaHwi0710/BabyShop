# -*- coding: utf-8 -*-
"""
apply_to_original.py
Sao chép bản báo cáo hoàn thiện Nhom1_BCBTL_HoanThien.docx 
ghi đè vào Nhom1_BCBTL.docx và Nhom1_BCBTL_DaSua.docx khi Microsoft Word đã đóng.
"""
import shutil
import sys
import os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/BabyShop")
SRC = ROOT / "Nhom1_BCBTL_HoanThien.docx"
DST_ORIG = ROOT / "Nhom1_BCBTL.docx"
DST_DASUA = ROOT / "Nhom1_BCBTL_DaSua.docx"

def main():
    if not SRC.exists():
        print(f"❌ Không tìm thấy tệp nguồn: {SRC}")
        return

    print(f"📁 Tệp nguồn hoàn thiện: {SRC} ({SRC.stat().st_size} bytes)")
    
    # Thử copy vào Nhom1_BCBTL.docx
    try:
        shutil.copy2(SRC, DST_ORIG)
        print(f"✅ Đã ghi đè thành công vào: {DST_ORIG}")
    except PermissionError:
        print(f"⚠️ {DST_ORIG} đang được mở trong ứng dụng khác. Vui lòng đóng Word và chạy lại.")
    except Exception as e:
        print(f"❌ Lỗi khi ghi đè {DST_ORIG}: {e}")

    # Thử copy vào Nhom1_BCBTL_DaSua.docx
    try:
        shutil.copy2(SRC, DST_DASUA)
        print(f"✅ Đã ghi đè thành công vào: {DST_DASUA}")
    except PermissionError:
        print(f"⚠️ {DST_DASUA} đang được mở trong ứng dụng khác. Vui lòng đóng Word và chạy lại.")
    except Exception as e:
        print(f"❌ Lỗi khi ghi đè {DST_DASUA}: {e}")

if __name__ == "__main__":
    main()
