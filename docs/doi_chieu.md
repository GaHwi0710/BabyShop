# BẢNG ĐỐI CHIẾU SỰ THẬT TỪ MÃ NGUỒN VÀ BÁO CÁO

> Ngày lập: 2026-10-04  
> Căn cứ nguồn sự thật: Toàn bộ mã nguồn thực tế tại `backend/src`, `frontend/src`, `database/`, các file `package.json`, và `README.md`.

---

## 1. THÔNG SỐ CƠ SỞ DỮ LIỆU & CÔNG NGHỆ BACKEND

| Hạng mục | Trong báo cáo cũ (`baocaobtl.docx`) | Sự thật trong mã nguồn (`backend/`) | Căn cứ mã nguồn (file:dòng) | Đề xuất sửa trong báo cáo |
| :--- | :--- | :--- | :--- | :--- |
| **Tên cơ sở dữ liệu** | `mom_baby_store` | `baby_shop_management` | `backend/src/config/mongodb.js:4` (`process.env.MONGODB_DB \|\| "baby_shop_management"`) | Sửa thành `baby_shop_management` ở toàn bộ các chương |
| **Phiên bản MongoDB Driver** | Native driver v6.12.0 | `mongodb` ^7.5.0 | `backend/package.json:15` (`"mongodb": "^7.5.0"`) | Sửa thành MongoDB Driver phiên bản 7.5.0 |
| **ORM / ODM Mongoose** | Có một số chỗ nhắc Mongoose | KHÔNG dùng Mongoose (chỉ dùng thuần Native MongoDB Client) | `backend/package.json` không có `mongoose` | Xóa bỏ triệt để mọi từ "Mongoose" |
| **Thuật toán băm mật khẩu** | `bcryptjs` | `node:crypto` -> `scryptSync` kèm muối ngẫu nhiên (salt 16 bytes hex) | `backend/src/modules/auth/password.js:3-12` | Sửa trong UC01, UC03: dùng `scrypt` (Node.js crypto) |
| **Transaction & Schema Validation** | Ghi "Schema Validation khắt khe" | Không dùng MongoDB JSON Schema Validator khắt khe, xác thực trực tiếp tại tầng mã nguồn Controller/Middleware, hỗ trợ Transaction với `client.startSession()` | `backend/src/config/mongodb.js:37-57`, `backend/src/modules/business/business.route.js:19-40` | Bỏ nhận định "Schema Validation khắt khe", làm rõ xác thực tại tầng ứng dụng |

---

## 2. CÔNG NGHỆ & THƯ VIỆN FRONTEND

| Hạng mục | Trong báo cáo cũ | Sự thật trong mã nguồn (`frontend/`) | Căn cứ mã nguồn | Đề xuất sửa trong báo cáo |
| :--- | :--- | :--- | :--- | :--- |
| **Thư viện Biểu đồ** | `Recharts` | Tự lập trình Native SVG Charts (`LineChart`, `BarChart`, `PieChart`) thuần React | `frontend/package.json` không có `recharts`; file `frontend/src/components/Charts.jsx:18-629`, `BarChart.jsx` | Sửa trong UC23, Chương 4: Biểu đồ SVG tự dựng (Custom SVG Charts) |
| **Xuất Excel** | Thư viện `xlsx` (SheetJS) | Tiện ích thuần `exportToExcel` (HTML Excel `.xls` với XML namespace) & `exportToCsv` (UTF-8 BOM `\uFEFF`) | `frontend/package.json` không có `xlsx`; file `frontend/src/lib/exportUtils.js:12-70` | Sửa trong UC24, Chương 4: Tiện ích xuất Excel/CSV thuần |
| **Xuất PDF** | Chỉ ghi chung chung | Dùng `jspdf` (`^4.2.1`) và phương thức in ấn trình duyệt `window.print()` qua `DocumentPrintPreviewModal` | `frontend/package.json:14` (`"jspdf": "^4.2.1"`), `frontend/src/lib/exportUtils.js:130-180` | Bổ sung thư viện jsPDF và in ấn chứng từ trực tiếp |
| **Phiên bản React & Vite** | React 18.3.1, Vite 6.0.5 | React 18.2.0, Vite 5.1.4, React Router DOM 6.22.2 | `frontend/package.json:15-19` | Cập nhật chính xác phiên bản |

---

## 3. DANH SÁCH 31 COLLECTION THỰC TẾ TRONG MONGODB

Thay vì 25 collection tên tiếng Anh như báo cáo cũ, hệ thống thực tế dùng tên tiếng Việt chuẩn hóa gồm **31 collection** (kể cả các collection chi tiết `CT_*`):

| STT | Tên Collection thật | Trường chính | Khóa ngoại tham chiếu | Ý nghĩa nghiệp vụ |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `VaiTro` | `_id`, `MaVaiTro`, `TenVaiTro`, `MaKey`, `MoTa`, `QuyenHan`, `LaVaiTroHeThong` | Không | Danh mục vai trò và ma trận phân quyền RBAC |
| 2 | `NhanVien` | `_id`, `MaNV`, `HoTen`, `ChucVu`, `PhongBan`, `SDT`, `Email`, `DiaChi`, `TrangThai` | `MaVaiTro` -> `VaiTro` | Hồ sơ nhân sự cửa hàng |
| 3 | `TaiKhoan` (hoặc `Users`) | `_id`, `username`, `passwordHash`, `MaNV`, `MaVaiTro`, `TrangThai`, `createdAt` | `MaNV` -> `NhanVien`, `MaVaiTro` -> `VaiTro` | Tài khoản đăng nhập hệ thống |
| 4 | `KhachHang` | `_id`, `MaKH`, `HoTen`, `SDT`, `Email`, `DiaChi`, `MaSoThue`, `DiemTichLuy`, `CapThanhVien` | Không | Danh mục khách hàng, tích điểm thành viên |
| 5 | `NhaCungCap` | `_id`, `MaNCC`, `TenNCC`, `NguoiLienHe`, `SDT`, `Email`, `DiaChi`, `MaSoThue` | Không | Danh mục nhà cung cấp hàng hóa |
| 6 | `LoaiHang` | `_id`, `MaLoai`, `TenLoai`, `MoTa`, `TrangThai` | Không | Phân nhóm ngành hàng mẹ và bé |
| 7 | `SanPham` | `_id`, `MaSP`, `TenSP`, `MaLoai`, `DonViTinh`, `GiaNhap`, `GiaBan`, `HinhAnh`, `SoLuongToiThieu`, `stock` | `MaLoai` -> `LoaiHang` | Danh mục hàng hóa, giá bán, ảnh Base64 |
| 8 | `TonKho` | `_id`, `MaSP`, `SoLuongTon`, `SoLuong`, `NgayCapNhat`, `updatedAt` | `MaSP` -> `SanPham` | Quản lý số lượng tồn kho theo thời gian thực |
| 9 | `DonDatHang` | `_id`, `MaDDH`, `MaNCC`, `MaNV`, `NgayDat`, `TongTien`, `TrangThai`, `GhiChu` | `MaNCC` -> `NhaCungCap`, `MaNV` -> `NhanVien` | Đơn đặt hàng mua gửi nhà cung cấp |
| 10 | `CT_DonDatHang` | `_id`, `MaDDH`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien` | `MaDDH` -> `DonDatHang`, `MaSP` -> `SanPham` | Chi tiết mặt hàng đặt mua |
| 11 | `PhieuNhap` | `_id`, `MaPN`, `MaDDH`, `MaNCC`, `MaNV`, `NgayNhap`, `TongTien`, `TrangThai` | `MaDDH` -> `DonDatHang`, `MaNCC` -> `NhaCungCap` | Phiếu nhập kho hàng hóa thực tế |
| 12 | `CT_PhieuNhap` | `_id`, `MaPN`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien` | `MaPN` -> `PhieuNhap`, `MaSP` -> `SanPham` | Chi tiết mặt hàng nhập kho |
| 13 | `DonHang` | `_id`, `MaDH`, `MaKH`, `MaNV`, `NgayDat`, `TongTien`, `TienGiam`, `ThanhTien`, `TrangThai` | `MaKH` -> `KhachHang`, `MaNV` -> `NhanVien` | Đơn bán hàng tại quầy POS |
| 14 | `CT_DonHang` | `_id`, `MaDH`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien` | `MaDH` -> `DonHang`, `MaSP` -> `SanPham` | Chi tiết mặt hàng bán |
| 15 | `HoaDon` | `_id`, `MaHD`, `MaDH`, `MaKH`, `MaNV`, `NgayLap`, `TongTien`, `DaThanhToan`, `ConNo`, `TrangThai` | `MaDH` -> `DonHang`, `MaKH` -> `KhachHang` | Hóa đơn bán lẻ kiêm chứng từ thanh toán |
| 16 | `CT_HoaDon` | `_id`, `MaHD`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien` | `MaHD` -> `HoaDon`, `MaSP` -> `SanPham` | Chi tiết hóa đơn bán hàng |
| 17 | `PhieuXuat` | `_id`, `MaPX`, `MaDH`, `MaNV`, `NgayXuat`, `TongTien`, `LyDo`, `TrangThai` | `MaDH` -> `DonHang`, `MaNV` -> `NhanVien` | Phiếu xuất kho giao hàng |
| 18 | `CT_PhieuXuat` | `_id`, `MaPX`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien` | `MaPX` -> `PhieuXuat`, `MaSP` -> `SanPham` | Chi tiết hàng hóa xuất kho |
| 19 | `PhieuThu` | `_id`, `MaPT`, `MaHD`, `MaKH`, `MaNV`, `NgayThu`, `SoTien`, `HinhThucTT`, `LyDo` | `MaHD` -> `HoaDon`, `MaKH` -> `KhachHang` | Phiếu thu tiền mặt theo mẫu số 01-TT |
| 20 | `PhieuChi` | `_id`, `MaPC`, `MaPN`, `MaNCC`, `MaNV`, `NgayChi`, `SoTien`, `HinhThucTT`, `LyDo` | `MaPN` -> `PhieuNhap`, `MaNCC` -> `NhaCungCap` | Phiếu chi tiền mặt theo mẫu số 02-TT |
| 21 | `ThanhToan` | `_id`, `MaTT`, `MaHD`, `MaKH`, `NgayTT`, `SoTien`, `PhuongThucTT`, `GhiChu` | `MaHD` -> `HoaDon` | Nhật ký các lần thanh toán hóa đơn |
| 22 | `CongNo` | `_id`, `MaCN`, `MaNCC`, `MaPN`, `MaKH`, `MaHD`, `LoaiCongNo`, `SoTienPhaiTra`, `DaTra`, `ConNo` | `MaPN` -> `PhieuNhap`, `MaNCC` -> `NhaCungCap` | Sổ theo dõi công nợ chi tiết hai chiều |
| 23 | `KiemKe` | `_id`, `MaKK`, `MaNV`, `NgayKiemKe`, `TrangThai`, `GhiChu` | `MaNV` -> `NhanVien` | Phiếu kiểm kê hàng hóa định kỳ |
| 24 | `CT_KiemKe` | `_id`, `MaKK`, `MaSP`, `TonHeThong`, `TonThucTe`, `ChenhLech`, `LyDo` | `MaKK` -> `KiemKe`, `MaSP` -> `SanPham` | Chi tiết chênh lệch kiểm kê từng mặt hàng |
| 25 | `DieuChinhKho` | `_id`, `MaDC`, `MaKK`, `MaNV`, `NgayDieuChinh`, `LyDo`, `TrangThai` | `MaKK` -> `KiemKe`, `MaNV` -> `NhanVien` | Chứng từ cân bằng tồn kho sau kiểm kê |
| 26 | `PhieuTraHang` | `_id`, `MaPTH`, `MaHD`, `MaKH`, `MaNV`, `NgayTra`, `TongTienHoan`, `LyDo`, `HinhThucHoan` | `MaHD` -> `HoaDon`, `MaKH` -> `KhachHang` | Phiếu tiếp nhận hàng bán bị trả lại |
| 27 | `CT_PhieuTraHang` | `_id`, `MaPTH`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `TinhTrangHang` | `MaPTH` -> `PhieuTraHang`, `MaSP` -> `SanPham` | Chi tiết mặt hàng đổi trả nhập lại kho |
| 28 | `KhuyenMai` | `_id`, `MaKM`, `TenKM`, `LoaiKM`, `GiaTri`, `GiaTriDonToiThieu`, `NgayBatDau`, `NgayKetThuc` | Không | Quản lý chương trình khuyến mãi và voucher |
| 29 | `CT_KhuyenMai` | `_id`, `MaKM`, `MaSP` | `MaKM` -> `KhuyenMai`, `MaSP` -> `SanPham` | Danh sách sản phẩm áp dụng khuyến mãi |
| 30 | `AuditLogs` | `_id`, `timestamp`, `user`, `role`, `action`, `module`, `details`, `ipAddress` | Không | Nhật ký kiểm toán toàn bộ thao tác hệ thống |
| 31 | `Counters` | `_id`, `seq` | Không | Bộ đếm tự tăng quản lý sinh mã chứng từ tự động |

*(Lưu ý: Hệ thống còn có collection `SaoLuu` / `Backups` phục vụ tính năng sao lưu dữ liệu snapshot JSON kèm SHA256 checksum).*

---

## 4. DANH SÁCH VAI TRÒ & PHÂN QUYỀN RBAC THỰC TẾ

Căn cứ: `backend/src/config/seed.js:11-42` và `backend/src/modules/shared/permissions.js:38-80`.

1. **Quản trị hệ thống (`QuanTriHeThong`) / Quản lý (`QuanLy`)**:
   - Mã vai trò: `1`.
   - Quyền hạn: Toàn quyền (FULL - Xem, Tạo, Sửa, Xóa) trên tất cả 24 module của hệ thống.
2. **Nhân viên bán hàng (`NhanVienBanHang`)**:
   - Mã vai trò: `2`.
   - Ghi (Toàn quyền): `customers`, `sales-orders`, `invoices`, `payments`, `returns`, `promotions`, `cash-receipts`.
   - Đọc (Chỉ xem): `dashboard`, `products`, `product-categories`, `inventory`.
3. **Nhân viên kho (`NhanVienKho` / `ThuKho`)**:
   - Mã vai trò: `3`.
   - Ghi (Toàn quyền): `products`, `product-categories`, `goods-receipts`, `goods-issues`, `inventory`, `stocktakes`.
   - Đọc (Chỉ xem): `dashboard`, `purchase-orders`, `sales-orders`, `returns`.
4. **Kế toán (`KeToan`)**:
   - Mã vai trò: `4`.
   - Ghi (Toàn quyền): `invoices`, `payments`, `debts`, `reports`, `cash-receipts`, `cash-payments`.
   - Đọc (Chỉ xem): `dashboard`, `customers`, `suppliers`, `products`, `purchase-orders`, `goods-receipts`, `sales-orders`, `returns`, `inventory`.
5. **Nhân viên mua hàng (`NhanVienMuaHang`)**:
   - Mã vai trò: `5`.
   - Ghi (Toàn quyền): `suppliers`, `purchase-orders`, `goods-receipts`.
   - Đọc (Chỉ xem): `dashboard`, `products`, `product-categories`, `inventory`, `debts`.

---

## 5. DANH SÁCH TRANG FRONTEND THỰC TẾ (`frontend/src/pages/modules/`)

| STT | File Component Frontend | Đường dẫn Route | Tên chức năng hiển thị | Vai trò được phép truy cập |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `DashboardPage.jsx` (ngoài thư mục) | `/` | Tổng quan Dashboard | Mọi vai trò |
| 2 | `LoginPage.jsx` (ngoài thư mục) | `/login` | Đăng nhập | Công khai (có nút đăng nhập nhanh 5 vai trò) |
| 3 | `CustomersPage.jsx` | `/customers` | Quản lý Khách hàng & Điểm tích lũy | Quản lý, Nhân viên bán hàng |
| 4 | `SuppliersPage.jsx` | `/suppliers` | Quản lý Nhà cung cấp | Quản lý, Nhân viên mua hàng |
| 5 | `ProductsPage.jsx` | `/products` | Quản lý Sản phẩm | Quản lý, Bán hàng, Kho |
| 6 | `CategoriesPage.jsx` | `/products/categories` | Quản lý Loại hàng | Quản lý, Bán hàng, Kho |
| 7 | `PurchaseOrderPage.jsx` | `/purchase-orders` | Đặt hàng Nhà cung cấp | Quản lý, Nhân viên mua hàng |
| 8 | `WarehouseDocumentsPage.jsx` | `/goods-receipts`, `/goods-issues` | Chứng từ kho (Nhập kho / Xuất kho tích hợp tab) | Quản lý, Kho, Mua hàng |
| 9 | `SalesPOSPage.jsx` | `/sales-orders` | Bán hàng POS tại quầy | Quản lý, Nhân viên bán hàng |
| 10 | `InvoicePage.jsx` | `/invoices` | Hóa đơn & Thanh toán | Quản lý, Bán hàng, Kế toán |
| 11 | `InventoryPage.jsx` | `/inventory` | Quản lý Tồn kho & Điều chỉnh kho | Quản lý, Kho |
| 12 | `StocktakePage.jsx` | `/stocktakes` | Kiểm kê kho hàng | Quản lý, Kho |
| 13 | `ReturnPage.jsx` | `/returns` | Quản lý Đổi trả hàng | Quản lý, Nhân viên bán hàng |
| 14 | `CashVouchersPage.jsx` | `/cash-receipts`, `/cash-payments` | Quản lý Thu chi (Phiếu thu 01-TT / Phiếu chi 02-TT) | Quản lý, Kế toán, Bán hàng |
| 15 | `DebtsPage.jsx` | `/debts` | Quản lý Công nợ Nhà cung cấp | Quản lý, Kế toán |
| 16 | `PromotionsPage.jsx` | `/promotions` | Khuyến mãi & Voucher | Quản lý, Nhân viên bán hàng |
| 17 | `ReportPage.jsx` | `/reports` | Hệ thống 17 Báo cáo tài chính & quản trị | Quản lý, Kế toán |
| 18 | `AdminPage.jsx` | `/admin/employees`, `/admin/roles`, `/admin/accounts` | Quản trị hệ thống (Nhân viên, Phân quyền, Người dùng) | Quản lý, Quản trị hệ thống |
| 19 | `AuditLogPage.jsx` | `/admin/audit-logs` | Nhật ký kiểm toán | Quản lý, Quản trị hệ thống |
| 20 | `BackupPage.jsx` | `/admin/backup` | Sao lưu & Phục hồi dữ liệu | Quản lý, Quản trị hệ thống |

---

## 6. DANH MỤC 17 BÁO CÁO KẾ TOÁN & QUẢN TRỊ THỰC TẾ (`reports.route.js`)

1. `GET /api/reports/revenue`: Báo cáo doanh thu (theo ngày/tháng/năm, khách hàng, sản phẩm, ngành hàng)
2. `GET /api/reports/warehouse`: Báo cáo nhập - xuất - tồn kho
3. `GET /api/reports/inventory`: Báo cáo tồn kho hiện tại (giá trị vốn tồn kho, số lượng)
4. `GET /api/reports/debts`: Báo cáo tổng hợp & chi tiết công nợ (phải thu KH, phải trả NCC)
5. `GET /api/reports/cash-flow`: Báo cáo lưu chuyển tiền tệ (dòng tiền thuần)
6. `GET /api/reports/cash-receipts`: Bảng kê thu tiền mặt (Mẫu số 01-TT)
7. `GET /api/reports/cash-payments`: Bảng kê chi tiền mặt (Mẫu số 02-TT)
8. `GET /api/reports/warehouse-receipts`: Bảng kê phiếu nhập kho (Mẫu số 01-VT)
9. `GET /api/reports/warehouse-issues`: Bảng kê phiếu xuất kho (Mẫu số 02-VT)
10. `GET /api/reports/bank-receipts`: Báo cáo thu tiền gửi ngân hàng (Giấy báo Có)
11. `GET /api/reports/bank-payments`: Báo cáo chi tiền gửi ngân hàng (Ủy nhiệm chi / Giấy báo Nợ)
12. `GET /api/reports/income-statement`: Báo cáo kết quả hoạt động kinh doanh (P&L: Doanh thu, Giá vốn, Lợi nhuận)
13. `GET /api/reports/product-ledger`: Sổ chi tiết hàng hóa / Thẻ kho
14. `GET /api/reports/general-journal`: Sổ nhật ký chung kế toán
15. `GET /api/reports/fixed-assets`: Báo cáo theo dõi công cụ dụng cụ / tài sản cửa hàng
16. `GET /api/reports/sales-by-employee`: Báo cáo doanh số bán lẻ theo nhân viên thu ngân
17. `GET /api/reports/stocktake-adjustments`: Báo cáo chênh lệch và điều chỉnh kiểm kê kho

---

## 7. QUY TẮC SINH MÃ CHỨNG TỪ THỰC TẾ (`businessCode.js`)

Quản lý tự động qua collection `Counters` với atomic `$inc`:
- Khách hàng: `KH` (ví dụ `KH001`)
- Nhà cung cấp: `NCC` (ví dụ `NCC001`)
- Sản phẩm: `SP` (ví dụ `SP001`)
- Loại hàng: `LH` (ví dụ `LH001`)
- Đơn đặt hàng mua: `DDH` (ví dụ `DDH001`)
- Phiếu nhập kho: `PN` (ví dụ `PN001`)
- Đơn hàng bán lẻ: `DH` (ví dụ `DH001`)
- Hóa đơn bán lẻ: `HD` (ví dụ `HD001`)
- Phiếu xuất kho: `PX` (ví dụ `PX001`)
- Phiếu kiểm kê: `KK` (ví dụ `KK001`)
- Phiếu điều chỉnh kho: `DC` (ví dụ `DC001`)
- Phiếu trả hàng: `PTH` (ví dụ `PTH001`)
- Khuyến mãi: `KM` (ví dụ `KM001`)
- Sổ công nợ: `CN` (ví dụ `CN001`)
- Nhật ký thanh toán: `TT` (ví dụ `TT001`)
- Phiếu thu tiền mặt: `PT` (ví dụ `PT001`)
- Phiếu chi tiền mặt: `PC` (ví dụ `PC001`)
- Nhân viên: `NV` (ví dụ `NV001`)
- Vai trò: `VT` (ví dụ `VT001`)

---

## 8. CÁC TÍNH NĂNG CÓ THẬT HOẶC CẦN LÀM RÕ TRONG BÁO CÁO

1. **Quét mã vạch**: Mã nguồn KHÔNG có chức năng quét barcode bằng camera/thiết bị riêng. Tại màn hình POS, nhân viên tìm kiếm nhanh qua input text (phím tắt F2). Báo cáo cần xóa claim quét mã vạch và chuyển vào Hướng phát triển.
2. **VietQR**: Hệ thống có **VietQR ĐỘNG** chuẩn NAPAS (`img.vietqr.io`) tự sinh theo số tiền và mã hóa đơn tại màn hình POS và Hóa đơn. Báo cáo cũ nói "chỉ là QR tĩnh" là sai sự thật, cần sửa lại.
3. **Tải ảnh sản phẩm**: Xử lý nén ảnh Base64 trực tiếp trên trình duyệt bằng HTML5 Canvas và lưu vào trường `HinhAnh` của collection `SanPham`. Không có endpoint upload multipart.
4. **Cảnh báo tồn kho**: Kiểm tra theo trường `SoLuongToiThieu` của từng sản phẩm hoặc ngưỡng mặc định `LOW_STOCK_THRESHOLD = 10`. Không có route `/inventory/alerts` riêng mà lọc trực tiếp trong `InventoryPage.jsx`.
5. **Hạch toán Nợ/Có tự động**: Hệ thống tự động gán `TkNo`, `TkCo` (111, 112, 131, 156, 331, 511, 632) khi phát sinh hóa đơn, phiếu nhập, phiếu xuất, phiếu thu, phiếu chi và tổng hợp vào Sổ nhật ký chung.
6. **Đổi trả hàng & Hoàn tiền**: Có thật (`ReturnPage.jsx` và `/api/returns`), tự động nhập lại kho và hoàn tiền hoặc giảm trừ công nợ.
7. **Kiểm kê & Điều chỉnh kho**: Có thật (`StocktakePage.jsx`), sau khi kiểm đếm thực tế, bấm "Điều chỉnh kho" hệ thống gọi `POST /api/stocktakes/:id/adjust` để tự động cân bằng tồn kho.
8. **Sao lưu & Phục hồi**: Có thật (`BackupPage.jsx` và `/api/admin/backup`), xuất snapshot JSON, tính mã băm SHA256 checksum, tự động tạo safety backup trước khi phục hồi.
9. **Nhật ký kiểm toán**: Có thật (`AuditLogPage.jsx` và collection `AuditLogs`).

---

## 9. ĐỐI CHIẾU PHÂN CÔNG THÀNH VIÊN VÀ MÂU THUẪN VỚI README

- **Thống kê Git Commit**: Toàn bộ commit trên git repository được thực hiện bởi account `GaHwi0710` (Ngô Gia Huy / Kiều Gia Huy).
- **Mâu thuẫn giữa Google Docs và README mục XV**:
  + Trong Google Docs: Kiều Gia Huy làm Mua hàng, Báo cáo; Ngô Gia Huy làm Phân tích nghiệp vụ, Sản phẩm; Đinh Tiến Đạt làm Giao diện, Đăng nhập; Nguyễn Duy Anh làm CSDL, NCC, Khách hàng.
  + Trong README mục XV: Kiều Gia Huy làm Nhóm trưởng, Kiến trúc hệ thống, Backend API, CSDL MongoDB; Ngô Gia Huy làm Giao diện bán lẻ POS; Nguyễn Trung Đức làm Mua hàng, Nhập kho; Đinh Tiến Đạt làm Kiểm kê kho; Nguyễn Duy Anh làm Thu chi tiền mặt, Công nợ; Nguyễn Đình Tiền Hải làm Dashboard, Báo cáo tài chính.
  + **Đánh dấu `[CẦN XÁC NHẬN]`** trong báo cáo để nhóm thống nhất phiên bản chính thức khi nộp cho thầy Vũ Minh Tâm.
