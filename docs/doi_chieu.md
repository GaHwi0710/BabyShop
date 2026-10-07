# BẢNG ĐỐI CHIẾU SỰ THẬT TỪ MÃ NGUỒN VÀ BÁO CÁO

> **Phiên bản hoàn thiện**: 2.1 (Cập nhật sau kiểm chứng chi tiết mã nguồn và tài liệu dự án)  
> **Căn cứ nguồn sự thật (Code-First)**:
> 1. Mã nguồn Backend: `backend/src/` (`app.js`, `routes/index.js`, `config/mongodb.js`, `config/ensure-indexes.js`, `config/seed.js`, các module `business`, `reports`, `accounts`, `roles`, `audit`, `backup`, `email`, `shared/createCrudModule.js`, `shared/detailCollections.js`, `shared/businessCode.js`, `shared/permissions.js`).
> 2. Mã nguồn Frontend: `frontend/src/` (`package.json`, `pages/modules/*.jsx`, `layouts/AppLayout.jsx`, `components/Charts.jsx`, `components/NotificationPopover.jsx`, `components/ShortcutsHelpModal.jsx`, `lib/exportUtils.js`, `lib/permissions.js`).
> 3. Cấu hình & phụ thuộc: `backend/package.json`, `frontend/package.json`, `package.json` (root).
> 4. Tài liệu đối chiếu: `README.md`, Phụ lục A.1, A.2, A.3 của báo cáo hiện tại (`baocaobtl.docx`).

---

## 1. THÔNG SỐ CƠ SỞ DỮ LIỆU & CÔNG NGHỆ BACKEND

| Hạng mục | Trong báo cáo cũ (`baocaobtl.docx`) | Sự thật trong mã nguồn (`backend/`) | Căn cứ mã nguồn (file:dòng) | Đề xuất sửa trong báo cáo |
| :--- | :--- | :--- | :--- | :--- |
| **Tên cơ sở dữ liệu** | `mom_baby_store` | `baby_shop_management` | `backend/src/config/mongodb.js:4` (`process.env.MONGODB_DB \|\| "baby_shop_management"`) | Sửa thành `baby_shop_management` tại toàn bộ các chương |
| **Phiên bản MongoDB Driver** | Native driver v6.12.0 | `mongodb` ^7.5.0 | `backend/package.json:15` (`"mongodb": "^7.5.0"`) | Sửa thành MongoDB Driver phiên bản 7.5.0 |
| **ORM / ODM Mongoose** | Có một số chỗ nhắc Mongoose | KHÔNG dùng Mongoose (chỉ dùng thuần Native MongoDB Client) | `backend/package.json` không có `mongoose` | Xóa bỏ triệt để mọi từ "Mongoose" trong toàn bộ tài liệu |
| **Thuật toán băm mật khẩu** | `bcryptjs` | `node:crypto` -> `scryptSync` kèm muối ngẫu nhiên (salt 16 bytes hex) | `backend/src/modules/auth/password.js:3-12` | Sửa trong UC01, UC03, Chương 3: dùng thuật toán `scrypt` (Node.js native crypto) |
| **Xác thực dữ liệu & Transaction** | Ghi "Schema Validation khắt khe trong MongoDB" | Xác thực nghiệp vụ tại tầng ứng dụng (Controller/Middleware), hỗ trợ Transaction qua `client.startSession()` kèm cơ chế graceful fallback tự phục hồi nếu chạy MongoDB Standalone | `backend/src/config/mongodb.js:37-58`, `backend/src/modules/shared/createCrudModule.js:61-105` | Sửa lại: xác thực tầng ứng dụng, cơ chế tự bảo vệ dữ liệu 2 lớp |

---

## 2. CÔNG NGHỆ & THƯ VIỆN FRONTEND

| Hạng mục | Trong báo cáo cũ | Sự thật trong mã nguồn (`frontend/`) | Căn cứ mã nguồn (file:dòng) | Đề xuất sửa trong báo cáo |
| :--- | :--- | :--- | :--- | :--- |
| **Thư viện Biểu đồ** | `Recharts` | Tự lập trình Native SVG Charts thuần React (`LineChart`, `BarChart`, `PieChart`, `DonutChart`) | `frontend/package.json` (không có recharts); `frontend/src/components/Charts.jsx:18-629` | Sửa trong UC23, Chương 4: Biểu đồ SVG tự dựng (Custom SVG Charts) |
| **Xuất Excel** | Thư viện `xlsx` (SheetJS) | Tiện ích xuất bảng tính **HTML/XML Spreadsheet (.xls) với Microsoft Office Namespace** (`exportToExcel`) và CSV UTF-8 kèm BOM (`exportToCsv`) | `frontend/package.json` (không có xlsx); `frontend/src/lib/exportUtils.js:12-70` | Sửa trong UC24, Chương 4: Xuất bảng tính chuẩn HTML/XML Spreadsheet (.xls) và CSV |
| **Xuất PDF & In ấn** | (không nêu) | Dùng thư viện `jspdf` (`^4.2.1`) và phương thức in ấn trình duyệt `window.print()` qua modal xem trước `DocumentPrintPreviewModal` | `frontend/package.json:14`, `frontend/src/lib/exportUtils.js:130-180`, `DocumentPrintPreviewModal.jsx` | Bổ sung thư viện jsPDF và in ấn chứng từ trực tiếp theo mẫu biểu kế toán |
| **Phiên bản React & Vite** | (không nêu) | React `18.2.0`, Vite `5.1.4`, React Router DOM `6.22.2` | `frontend/package.json:15-19` | Bổ sung chính xác thông số kỹ thuật thực tế vào Chương 4 |
| **Kiểm tra các thư viện phổ biến** | | **axios**: CÓ (`^1.6.7` trong `frontend/package.json:13`)<br>**tailwind**: KHÔNG CÓ (dùng CSS thuần tùy biến)<br>**bcryptjs**: KHÔNG CÓ<br>**xlsx**: KHÔNG CÓ<br>**recharts**: KHÔNG CÓ | `frontend/package.json`, `backend/package.json` | Làm rõ cấu hình thư viện chuẩn xác, không bịa thư viện |

---

## 3. DANH SÁCH 31 COLLECTION THỰC TẾ TRONG MONGODB

### 3.1. Tổng kết số lượng và chốt tên Collection
- **Chốt tên bảng tài khoản**: Collection trong MongoDB thực tế là **`Users`** (không phải `TaiKhoan`). Toàn bộ các truy vấn tài khoản trong mã nguồn đều trực tiếp gọi `database.collection("Users")` (`accounts.route.js:43`, `auth.route.js:174`, `seed.js:540`, `ensure-indexes.js:83`).
- **Chốt vấn đề Sao lưu (Backup)**: Hệ thống **KHÔNG có collection `SaoLuu` hay `Backups` trong MongoDB**. Các bản sao lưu được lưu trữ dưới dạng **tệp JSON vật lý** trên đĩa tại thư mục `backups/` (`backend/src/modules/backup/backup.route.js:12-15`).
- **Phân loại chính xác 31 Collection**:
  + **20 collection nghiệp vụ & danh mục**: `Users`, `VaiTro`, `NhanVien`, `KhachHang`, `NhaCungCap`, `LoaiHang`, `SanPham`, `TonKho`, `DonDatHang`, `PhieuNhap`, `DonHang`, `HoaDon`, `PhieuXuat`, `PhieuThu`, `PhieuChi`, `ThanhToan`, `CongNo`, `KiemKe`, `DieuChinhKho`, `PhieuTraHang`, `KhuyenMai`. (Lưu ý: 20 bảng cơ sở này + `Users` là 20 bảng độc lập).
  + **8 collection chi tiết chứng từ (`CT_*`)**: `CT_DonDatHang`, `CT_DonHang`, `CT_HoaDon`, `CT_PhieuNhap`, `CT_PhieuXuat`, `CT_KiemKe`, `CT_PhieuTraHang`, `CT_KhuyenMai`.
  + **3 collection hệ thống**: `Users` (đã tính ở trên), `Counters` (mã tự tăng), `AuditLogs` (nhật ký kiểm toán).
  + Tổng số lượng collection nghiệp vụ và quản trị được backup trong `BACKUP_COLLECTIONS` (`backend/src/modules/backup/backup.route.js:20-52`) là **ĐÚNG 31 COLLECTION**.
  + *(Ngoài ra, MongoDB có collection kỹ thuật nội bộ `_metadata` dùng để lưu các cờ migration `strict-permissions-v4/v5/v6`, `initial-seed-v1` tại `seed.js:469,478,495,529`, không phải bảng dữ liệu do người dùng quản lý).*

### 3.2. Đặc điểm liên kết dữ liệu trong hệ thống
1. **Tham chiếu bằng Mã nghiệp vụ dạng chuỗi (String Business Code)**:
   - Các bảng trong CSDL liên kết với nhau chủ yếu thông qua **MÃ CHUỖI NGHIỆP VỤ** do hệ thống tự sinh qua `Counters` (`MaSP`, `MaLoai`, `MaKH`, `MaNCC`, `MaDDH`, `MaPN`, `MaDH`, `MaHD`, `MaPX`, `MaKK`, `MaPTH`, `MaCN`, `MaPT`, `MaPC`...), **KHÔNG dùng ObjectId làm khóa ngoại bắt buộc**.
2. **Cơ chế lưu trữ kép chi tiết chứng từ (Dual-Storage Pattern)**:
   - Toàn bộ danh sách hàng hóa trong chứng từ (`details` / `items`) vừa được **nhúng trực tiếp (embedded)** dưới dạng mảng JSON trong document cha (giúp tối ưu tốc độ đọc đơn lẻ, in ấn không cần $lookup), vừa được **lưu trữ song song sang collection chi tiết độc lập `CT_*`** qua hàm `replaceDetails` (`backend/src/modules/shared/detailCollections.js:26-42`) phục vụ cho các câu lệnh truy vấn phân tích, báo cáo tổng hợp và kiểm kê.

### 3.3. Bảng kê chi tiết 31 Collection và Khóa ngoại thực tế từ mã nguồn

| STT | Tên Collection thực tế | Khóa chính | Trường liên kết / Khóa ngoại THỰC TẾ TRONG CODE | Các trường dữ liệu chính từ mã nguồn |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **`Users`** | `_id` | `role` (chuỗi tên vai trò, map qua `VaiTro.MaKey`), liên kết `NhanVien` qua `username` | `username`, `passwordHash`, `fullName`, `role`, `status`, `email`, `phone`, `CCCD`, `createdAt`, `updatedAt` |
| 2 | **`VaiTro`** | `_id` | Không có (bảng danh mục vai trò gốc) | `MaVaiTro` (1-5), `TenVaiTro`, `MaKey`, `LaVaiTroHeThong`, `MoTa`, `QuyenHan`, `createdAt` |
| 3 | **`NhanVien`** | `_id` | `MaVaiTro` (số nguyên tham chiếu `VaiTro.MaVaiTro`), `username` (tham chiếu `Users.username`) | `MaNV`, `HoTen`, `ChucVu`, `PhongBan`, `SDT`, `Email`, `DiaChi`, `CCCD`, `TrangThai`, `username`, `VaiTro`, `MaVaiTro` |
| 4 | **`KhachHang`** | `_id` | Không có (bảng danh mục khách hàng gốc) | `MaKH`, `HoTen`, `SDT`, `Email`, `DiaChi`, `MaSoThue`, `DiemTichLuy`, `CapThanhVien`, `TrangThai`, `createdAt` |
| 5 | **`NhaCungCap`** | `_id` | Không có (bảng danh mục nhà cung cấp gốc) | `MaNCC`, `TenNCC`, `NguoiLienHe`, `SDT`, `Email`, `DiaChi`, `MaSoThue`, `TrangThai`, `createdAt` |
| 6 | **`LoaiHang`** | `_id` | Không có (bảng danh mục loại hàng gốc) | `MaLoai`, `TenLoai`, `MoTa`, `TrangThai`, `createdAt` |
| 7 | **`SanPham`** | `_id` | `MaLoai` (ObjectId/chuỗi tham chiếu `LoaiHang._id` hoặc `LoaiHang.MaLoai`) | `MaSP`, `TenSP`, `MaLoai`, `DonViTinh`, `GiaNhap`, `GiaBan`, `HanSuDung`, `TrangThai`, `stock`, `SoLuongToiThieu`, `HinhAnh`, `createdAt` |
| 8 | **`TonKho`** | `_id` | `MaSP` (ObjectId tham chiếu `SanPham._id`) | `MaSP`, `SoLuongTon`, `SoLuong`, `NgayCapNhat`, `updatedAt` |
| 9 | **`DonDatHang`** | `_id` | `MaNCC` (chuỗi/ObjectId tham chiếu `NhaCungCap`), `MaNV` (tham chiếu `NhanVien`) | `MaDDH`, `MaNCC`, `MaNV`, `NgayDat`, `TongTien`, `TrangThai`, `NguoiLap`, `GhiChu`, `details` |
| 10 | **`CT_DonDatHang`** | `_id` | `MaDDH` (tham chiếu `DonDatHang._id` hoặc `MaDDH`), `MaSP` (tham chiếu `SanPham`) | `MaDDH`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `createdAt` |
| 11 | **`PhieuNhap`** | `_id` | `MaDDH` (tham chiếu `DonDatHang`), `MaNCC` (tham chiếu `NhaCungCap`), `MaNV` (tham chiếu `NhanVien`) | `MaPN`, `MaDDH`, `MaNCC`, `MaNV`, `NgayNhap`, `TongTien`, `TrangThai`, `NguoiLap`, `details` |
| 12 | **`CT_PhieuNhap`** | `_id` | `MaPN` (tham chiếu `PhieuNhap._id` hoặc `MaPN`), `MaSP` (tham chiếu `SanPham`) | `MaPN`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `createdAt` |
| 13 | **`DonHang`** | `_id` | `MaKH` (tham chiếu `KhachHang`), `MaNV` (tham chiếu `NhanVien`) | `MaDH`, `MaKH`, `MaNV`, `NgayDat`, `TongTien`, `TienGiam`, `ThanhTien`, `TrangThai`, `details` |
| 14 | **`CT_DonHang`** | `_id` | `MaDH` (tham chiếu `DonHang._id` hoặc `MaDH`), `MaSP` (tham chiếu `SanPham`) | `MaDH`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `createdAt` |
| 15 | **`HoaDon`** | `_id` | `MaDH` (tham chiếu `DonHang`), `MaKH` (tham chiếu `KhachHang`) | `MaHD`, `MaDH`, `MaKH`, `TenKH`, `MaKHCode`, `NgayLap`, `TongTien`, `SoTienDaTra`, `ConNo`, `TrangThai`, `details` |
| 16 | **`CT_HoaDon`** | `_id` | `MaHD` (tham chiếu `HoaDon._id` hoặc `MaHD`), `MaSP` (tham chiếu `SanPham`) | `MaHD`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `createdAt` |
| 17 | **`PhieuXuat`** | `_id` | `MaDH` (tham chiếu `DonHang`), `MaNV` (tham chiếu `NhanVien`) | `MaPX`, `MaDH`, `MaNV`, `NgayXuat`, `TongTien`, `LyDo`, `TrangThai`, `details` |
| 18 | **`CT_PhieuXuat`** | `_id` | `MaPX` (tham chiếu `PhieuXuat._id` hoặc `MaPX`), `MaSP` (tham chiếu `SanPham`) | `MaPX`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `createdAt` |
| 19 | **`PhieuThu`** | `_id` | `ChungTuGoc` (chuỗi mã chứng từ tham chiếu như `"HD001"`, `"CN002"`, `"DH005"`) | `MaPT`, `NgayLap`, `NguoiNopTien`, `DiaChi`, `LyDo`, `SoTien`, `ChungTuGoc`, `KemTheo`, `TrangThai`, `NguoiLap` |
| 20 | **`PhieuChi`** | `_id` | `ChungTuGoc` (chuỗi mã chứng từ tham chiếu như `"PN001"`) | `MaPC`, `NgayLap`, `NguoiNhanTien`, `DiaChi`, `LyDo`, `SoTien`, `ChungTuGoc`, `KemTheo`, `TrangThai`, `NguoiLap` |
| 21 | **`ThanhToan`** | `_id` | `MaHD` (tham chiếu `HoaDon._id` hoặc `MaHD`) | `MaTT`, `MaHD`, `SoTien`, `PhuongThuc`, `NgayThanhToan`, `TrangThai`, `createdAt` |
| 22 | **`CongNo`** | `_id` | `MaPN` (tham chiếu `PhieuNhap`), `MaNCC` (tham chiếu `NhaCungCap`), `MaHD` (tham chiếu `HoaDon`), `MaKH` (tham chiếu `KhachHang`) | `MaCN`, `MaPN`, `MaNCC`, `TenNCC`, `MaHD`, `MaKH`, `LoaiCongNo` ("Nhà cung cấp"/"Khách hàng"), `SoTien`, `SoTienDaTra`, `SoTienConLai`, `TrangThai` |
| 23 | **`KiemKe`** | `_id` | Không có trường FK riêng (người kiểm kê/điều chỉnh lưu chuỗi `NguoiKiemKe`, `NguoiDieuChinh`) | `MaKK`, `NgayKiemKe`, `TrangThai`, `GhiChu`, `NguoiKiemKe`, `NguoiDieuChinh`, `NgayDieuChinh`, `details` |
| 24 | **`CT_KiemKe`** | `_id` | `MaKK` (tham chiếu `KiemKe._id` hoặc `MaKK`), `MaSP` (tham chiếu `SanPham`) | `MaKK`, `MaSP`, `SoLuongHeThong`, `SoLuongThucTe`, `ChenhLech`, `LyDo`, `createdAt` |
| 25 | **`DieuChinhKho`** | `_id` | `MaKK` (tham chiếu `KiemKe`) | `MaDC`, `MaKK`, `NgayDieuChinh`, `NguoiThucHien`, `LyDo`, `details`, `createdAt` |
| 26 | **`PhieuTraHang`** | `_id` | `MaDH` (tham chiếu `DonHang`), `MaHD` (tham chiếu `HoaDon`), `MaKH` (tham chiếu `KhachHang`), `MaNV` (tham chiếu `NhanVien`) | `MaPTH`, `MaDH`, `MaHD`, `MaKH`, `MaNV`, `NguoiLap`, `NgayTra`, `LyDo`, `TrangThai`, `SoLuong`, `details` |
| 27 | **`CT_PhieuTraHang`** | `_id` | `MaPTH` (tham chiếu `PhieuTraHang._id` hoặc `MaPTH`), `MaSP` (tham chiếu `SanPham`) | `MaPTH`, `MaSP`, `SoLuong`, `DonGia`, `ThanhTien`, `createdAt` |
| 28 | **`KhuyenMai`** | `_id` | Không có (danh mục khuyến mãi gốc) | `MaKM`, `TenKM`, `LoaiKM`, `GiaTriGiam`, `PhanTramGiam`, `DonHangToiThieu`, `NgayBatDau`, `NgayKetThuc`, `TrangThai` |
| 29 | **`CT_KhuyenMai`** | `_id` | `MaKM` (tham chiếu `KhuyenMai._id` hoặc `MaKM`), `MaSP` (tham chiếu `SanPham`) | `MaKM`, `MaSP`, `createdAt` |
| 30 | **`Counters`** | `_id` | Không có (bảng sinh mã tự tăng hệ thống) | `_id` (tiền tố mã: `HD`, `SP`, `KH`, `PN`...), `seq` (số tự tăng) |
| 31 | **`AuditLogs`** | `_id` | Không có (bảng nhật ký kiểm toán hệ thống) | `timestamp`, `userId`, `username`, `role`, `action`, `module`, `entity`, `entityId`, `description`, `metadata`, `ip` |

### 3.4. Danh mục Giá trị Enum `TrangThai` thực tế trong mã nguồn

| Thực thể / Bảng | Danh sách giá trị `TrangThai` thật | Căn cứ mã nguồn (file:dòng) |
| :--- | :--- | :--- |
| **`DonDatHang`** | `"Chờ duyệt"`, `"Đang giao"`, `"Hoàn thành"`, `"Đã hủy"` | `seed.js:456`, `createCrudModule.js:961`, `WarehouseDocumentsPage.jsx:48` |
| **`PhieuNhap`** | `"Đã lưu"`, `"Hoàn thành"`, `"Đã hủy"` | `WarehouseDocumentsPage.jsx:273,848`, `createCrudModule.js:961` |
| **`HoaDon`** | `"Đã thanh toán"`, `"Chưa thanh toán"`, `"Thanh toán 1 phần"`, `"Đã hủy"` | `SalesPOSPage.jsx:1295-1298`, `reports.route.js:2138,2176` |
| **`DonHang`** | `"Hoàn thành"`, `"Đã hủy"` | `SalesPOSPage.jsx:411`, `createCrudModule.js:961` |
| **`KiemKe`** | `"Đang kiểm kê"`, `"Đã điều chỉnh"`, `"Chờ điều chỉnh"`, `"Khớp hoàn toàn"` | `business.route.js:1420,1488`, `StocktakePage.jsx:531,547` |
| **`PhieuTraHang`**| `"Đã xử lý"`, `"Đã hoàn tiền"`, `"Đã hủy"` | `business.route.js:1725`, `ReturnPage.jsx` |
| **`PhieuThu` / `PhieuChi`** | `"Đã lập"`, `"Đã xác nhận"`, `"Đã hủy"` | `seed.js:511-518`, `business.route.js:1841,1899` |
| **`CongNo`** | `"Còn nợ"`, `"Đã thanh toán"`, `"Quá hạn"` | `NotificationPopover.jsx:118`, `business.route.js:548,1215` |
| **`SanPham`** | `"Đang bán"`, `"Ngừng bán"` | `createCrudModule.js:64,88`, `seed.js:728`, `SalesPOSPage.jsx:192` |
| **`KhachHang` / `NhaCungCap`** | `"Đang hoạt động"`, `"Ngưng hoạt động"` | `createCrudModule.js:873,917`, `SuppliersPage.jsx:37,413` |
| **`KhuyenMai`** | `"Đang áp dụng"`, `"Đã kết thúc"`, `"Chưa kích hoạt"` | `seed.js:643,659`, `SalesPOSPage.jsx:213` |
| **`Users` / `NhanVien`** | `"Hoạt động"`, `"Đã khóa"`, `"Đã nghỉ việc"` | `accounts.route.js:56,219,281` |

---

## 4. DANH MỤC TOÀN BỘ ROUTE API BACKEND THỰC TẾ

Hệ thống cung cấp tổng cộng **103 endpoint API RESTful** (bao gồm các endpoint CRUD danh mục, endpoint nghiệp vụ chuyên biệt, báo cáo và quản trị):

### 4.1. Nhóm Xác thực & Hệ thống (Auth & System)
1. `GET  /api/health` | Quyền: Công khai | Kiểm tra kết nối MongoDB ping (`backend/src/app.js:16`)
2. `POST /api/auth/login` | Quyền: Công khai | Đăng nhập tài khoản, trả về JWT & user profile (`auth.route.js:12`)
3. `POST /api/auth/logout` | Quyền: Đã xác thực | Đăng xuất người dùng (`auth.route.js:98`)
4. `GET  /api/auth/me` | Quyền: Đã xác thực | Lấy hồ sơ tài khoản hiện tại (`auth.route.js:110`)
5. `PUT  /api/auth/change-password` | Quyền: Đã xác thực | Đổi mật khẩu cá nhân (tối thiểu 6 ký tự) (`auth.route.js:208`)
6. `POST /api/auth/change-password` | Quyền: Đã xác thực | Alias đổi mật khẩu (`auth.route.js:209`)
7. `POST /api/email/invoice` | Quyền: Đã xác thực | Gửi hóa đơn kèm file PDF qua thư điện tử (`email.route.js:10`)

### 4.2. Nhóm Quản trị hệ thống (Admin: Accounts, Roles, Audit, Backup)
*(Áp dụng middleware `allowRoles("QuanLy", "QuanTriHeThong")` tại `routes/index.js:37`)*
8. `GET    /api/admin/accounts` | Quyền: `admin-accounts: xem` | Danh sách tài khoản người dùng (`accounts.route.js:40`)
9. `POST   /api/admin/accounts` | Quyền: `admin-accounts: tao` | Tạo tài khoản mới (`accounts.route.js:68`)
10. `PUT    /api/admin/accounts/:id` | Quyền: `admin-accounts: sua` | Chỉnh sửa thông tin tài khoản (`accounts.route.js:119`)
11. `PATCH  /api/admin/accounts/:id/toggle-lock` | Quyền: `admin-accounts: sua` | Khóa/Mở khóa tài khoản (chặn tự khóa chính mình) (`accounts.route.js:204`)
12. `DELETE /api/admin/accounts/:id` | Quyền: `admin-accounts: xoa` | Xóa tài khoản (chặn tự xóa, chuyển trạng thái NV) (`accounts.route.js:256`)
13. `GET    /api/admin/roles` | Quyền: `admin-roles: xem` | Danh mục vai trò và ma trận quyền (`roles.route.js:38`)
14. `POST   /api/admin/roles` | Quyền: `admin-roles: tao` | Thêm vai trò mới (`roles.route.js:56`)
15. `PUT    /api/admin/roles/:id` | Quyền: `admin-roles: sua` | Cập nhật quyền hạn cho vai trò (`roles.route.js:96`)
16. `DELETE /api/admin/roles/:id` | Quyền: `admin-roles: xoa` | Xóa vai trò tùy biến (`roles.route.js:139`)
17. `GET    /api/admin/audit-logs` | Quyền: `audit-logs: xem` | Truy vấn nhật ký thao tác kiểm toán (`audit.route.js:7`)
18. `DELETE /api/admin/audit-logs*` | Quyền: Chặn toàn bộ (403) | Bảo đảm tính bất biến append-only của nhật ký (`audit.route.js:27`)
19. `POST   /api/admin/backup` | Quyền: `backup: tao` | Xuất snapshot 31 collections ra file JSON có SHA-256 (`backup.route.js:57`)
20. `GET    /api/admin/backup/list` | Quyền: `backup: xem` | Danh sách các bản sao lưu trên đĩa (`backup.route.js:122`)
21. `GET    /api/admin/backup/download/:filename` | Quyền: `backup: xem` | Tải file sao lưu về máy (`backup.route.js:149`)
22. `POST   /api/admin/backup/restore/preview` | Quyền: `backup: sua` | Xem trước nội dung trước khi phục hồi (`backup.route.js:170`)
23. `POST   /api/admin/backup/restore` | Quyền: `backup: sua` | Phục hồi dữ liệu (tự tạo bản safety pre-restore backup) (`backup.route.js:211`)
24. `DELETE /api/admin/backup*` | Quyền: Chặn toàn bộ (403) | Chặn xóa bản sao lưu (`backup.route.js:379`)

### 4.3. Nhóm Danh mục & Khách hàng, NCC, Nhân viên
25. `GET    /api/customers` | Quyền: `customers: xem` | Danh sách khách hàng (`createCrudModule.js`)
26. `POST   /api/customers` | Quyền: `customers: tao` | Thêm khách hàng mới (`createCrudModule.js`)
27. `PUT    /api/customers/:id` | Quyền: `customers: sua` | Sửa thông tin khách hàng (`createCrudModule.js`)
28. `DELETE /api/customers/:id` | Quyền: `customers: xoa` | Soft-delete khách hàng nếu có chứng từ (`createCrudModule.js:845`)
29. `POST   /api/customers/:id/redeem-voucher` | Quyền: `customers: sua` | Đổi điểm tích lũy thành voucher giảm giá (`business.route.js:1785`)
30. `GET    /api/suppliers` | Quyền: `suppliers: xem` | Danh sách nhà cung cấp (`createCrudModule.js`)
31. `POST   /api/suppliers` | Quyền: `suppliers: tao` | Thêm nhà cung cấp (`createCrudModule.js`)
32. `PUT    /api/suppliers/:id` | Quyền: `suppliers: sua` | Sửa thông tin NCC (`createCrudModule.js`)
33. `DELETE /api/suppliers/:id` | Quyền: `suppliers: xoa` | Soft-delete NCC nếu có chứng từ (`createCrudModule.js:896`)
34. `GET    /api/products` | Quyền: `products: xem` | Danh sách sản phẩm, tồn kho, HSD (`createCrudModule.js`)
35. `POST   /api/products` | Quyền: `products: tao` | Thêm sản phẩm, ảnh Base64 Canvas (`createCrudModule.js`)
36. `PUT    /api/products/:id` | Quyền: `products: sua` | Sửa thông tin sản phẩm (`createCrudModule.js`)
37. `DELETE /api/products/:id` | Quyền: `products: xoa` | Soft-delete sang "Ngừng bán" nếu có chứng từ (`createCrudModule.js:923`)
38. `GET    /api/product-categories` | Quyền: `product-categories: xem` | Danh sách loại hàng (`createCrudModule.js`)
39. `POST   /api/product-categories` | Quyền: `product-categories: tao` | Thêm loại hàng (`createCrudModule.js`)
40. `PUT    /api/product-categories/:id` | Quyền: `product-categories: sua` | Sửa loại hàng (`createCrudModule.js`)
41. `DELETE /api/product-categories/:id` | Quyền: `product-categories: xoa` | Chặn xóa nếu có SP liên kết (`createCrudModule.js:879`)
42. `GET    /api/admin/employees` | Quyền: `admin-employees: xem` | Danh sách nhân viên (`createCrudModule.js`)
43. `POST   /api/admin/employees` | Quyền: `admin-employees: tao` | Thêm nhân viên (`createCrudModule.js`)
44. `PUT    /api/admin/employees/:id` | Quyền: `admin-employees: sua` | Sửa nhân viên (`createCrudModule.js`)
45. `DELETE /api/admin/employees/:id` | Quyền: `admin-employees: xoa` | Xóa nhân viên (`createCrudModule.js`)
46. `GET    /api/promotions` | Quyền: `promotions: xem` | Danh sách khuyến mãi & voucher (`createCrudModule.js`)
47. `POST   /api/promotions` | Quyền: `promotions: tao` | Tạo khuyến mãi mới (`createCrudModule.js`)
48. `PUT    /api/promotions/:id` | Quyền: `promotions: sua` | Sửa chương trình khuyến mãi (`createCrudModule.js`)
49. `DELETE /api/promotions/:id` | Quyền: `promotions: xoa` | Xóa khuyến mãi (`createCrudModule.js`)

### 4.4. Nhóm Mua hàng & Nhập kho
50. `GET    /api/purchase-orders` | Quyền: `purchase-orders: xem` | Danh sách đơn đặt hàng NCC (`createCrudModule.js`)
51. `POST   /api/purchase-orders` | Quyền: `purchase-orders: tao` | Tạo đơn đặt hàng NCC (`createCrudModule.js`)
52. `PUT    /api/purchase-orders/:id` | Quyền: `purchase-orders: sua` | Cập nhật đơn đặt hàng (`createCrudModule.js`)
53. `DELETE /api/purchase-orders/:id` | Quyền: `purchase-orders: xoa` | Chặn xóa vật lý chứng từ kế toán (`createCrudModule.js:961`)
54. `GET    /api/purchase-orders/:id/receipts` | Quyền: `goods-receipts: xem` | Xem phiếu nhập kho của đơn mua (`business.route.js:1063`)
55. `POST   /api/purchase-orders/:id/receive` | Quyền: `goods-receipts: tao` | Nhập kho trực tiếp từ đơn mua (`business.route.js:1103`)
56. `GET    /api/goods-receipts` | Quyền: `goods-receipts: xem` | Danh sách phiếu nhập kho (`createCrudModule.js`)
57. `POST   /api/goods-receipts` | Quyền: `goods-receipts: tao` | Nhập kho, tự tăng TonKho và ghi nợ NCC (`business.route.js:74`)
58. `PUT    /api/goods-receipts/:id` | Quyền: `goods-receipts: sua` | Sửa thông tin phiếu nhập kho (`createCrudModule.js`)
59. `DELETE /api/goods-receipts/:id` | Quyền: `goods-receipts: xoa` | Chặn xóa vật lý (`createCrudModule.js:961`)

### 4.5. Nhóm Bán lẻ POS, Hóa đơn & Xuất kho
60. `GET    /api/sales-orders` | Quyền: `sales-orders: xem` | Danh sách đơn bán lẻ (`createCrudModule.js`)
61. `POST   /api/sales-orders` | Quyền: `sales-orders: tao` | Tạo đơn hàng POS, trừ tồn kho, sinh Hóa đơn & Phiếu xuất (`business.route.js:373`)
62. `PUT    /api/sales-orders/:id` | Quyền: `sales-orders: sua` | Cập nhật đơn hàng (`createCrudModule.js`)
63. `DELETE /api/sales-orders/:id` | Quyền: `sales-orders: xoa` | Chặn xóa vật lý (`createCrudModule.js:961`)
64. `GET    /api/invoices` | Quyền: `invoices: xem` | Danh sách hóa đơn bán lẻ (`createCrudModule.js`)
65. `POST   /api/invoices` | Quyền: `invoices: tao` | Tạo hóa đơn bán lẻ (`createCrudModule.js`)
66. `PUT    /api/invoices/:id` | Quyền: `invoices: sua` | Cập nhật hóa đơn (`createCrudModule.js`)
67. `DELETE /api/invoices/:id` | Quyền: `invoices: xoa` | Chặn xóa vật lý (`createCrudModule.js:961`)
68. `GET    /api/goods-issues` | Quyền: `goods-issues: xem` | Danh sách phiếu xuất kho (`createCrudModule.js`)
69. `POST   /api/goods-issues` | Quyền: `goods-issues: tao` | Tạo phiếu xuất kho giao hàng (`business.route.js:322`)
70. `PUT    /api/goods-issues/:id` | Quyền: `goods-issues: sua` | Sửa phiếu xuất kho (`createCrudModule.js`)
71. `DELETE /api/goods-issues/:id` | Quyền: `goods-issues: xoa` | Chặn xóa vật lý (`createCrudModule.js:961`)
72. `GET    /api/payments` | Quyền: `payments: xem` | Lịch sử thanh toán hóa đơn (`createCrudModule.js`)
73. `POST   /api/payments` | Quyền: `payments: tao` | Thu tiền hóa đơn, cập nhật DaThanhToan, trừ nợ (`business.route.js:657`)
74. `PUT    /api/payments/:id` | Quyền: `payments: sua` | Cập nhật bản ghi thanh toán (`createCrudModule.js`)
75. `DELETE /api/payments/:id` | Quyền: `payments: xoa` | Xóa bản ghi thanh toán (`createCrudModule.js`)
76. `GET    /api/returns` | Quyền: `returns: xem` | Danh sách phiếu đổi trả hàng (`createCrudModule.js`)
77. `POST   /api/returns` | Quyền: `returns: tao` | Tiếp nhận trả hàng, cộng hoàn lại số lượng tồn kho (`business.route.js:1666`)
78. `PUT    /api/returns/:id` | Quyền: `returns: sua` | Cập nhật phiếu trả hàng (`createCrudModule.js`)
79. `DELETE /api/returns/:id` | Quyền: `returns: xoa` | Xóa phiếu trả hàng (`createCrudModule.js`)

### 4.6. Nhóm Kho & Kiểm kê
80. `GET    /api/inventory` | Quyền: `inventory: xem` | Xem tồn kho thời gian thực (`business.route.js:1748`)
81. `POST   /api/inventory/adjust` | Quyền: `inventory: sua` | Điều chỉnh tồn kho thủ công (`business.route.js:1539`)
82. `GET    /api/inventory/adjustments` | Quyền: `inventory: xem` | Xem lịch sử điều chỉnh tồn lẻ (`business.route.js:1630`)
83. `GET    /api/stocktakes` | Quyền: `stocktakes: xem` | Danh sách các đợt kiểm kê kho (`createCrudModule.js`)
84. `POST   /api/stocktakes` | Quyền: `stocktakes: tao` | Lập phiếu kiểm kê kho (`business.route.js:1312`)
85. `PUT    /api/stocktakes/:id` | Quyền: `stocktakes: sua` | Cập nhật số lượng kiểm kê thực tế (`createCrudModule.js`)
86. `DELETE /api/stocktakes/:id` | Quyền: `stocktakes: xoa` | Hủy phiếu kiểm kê (`createCrudModule.js`)
87. `POST   /api/stocktakes/:id/adjust` | Quyền: `stocktakes: sua` | Cân bằng tồn kho thực tế (Thủ kho tự bấm được) (`business.route.js:1408`)
88. `GET    /api/stocktakes/adjustments` | Quyền: `stocktakes: xem` | Lịch sử phiếu kiểm kê đã cân bằng (`business.route.js:1648`)

### 4.7. Nhóm Tài chính, Thu chi & Công nợ
89. `GET    /api/debts` | Quyền: `debts: xem` | Danh sách sổ công nợ nhà cung cấp (`createCrudModule.js`)
90. `PUT    /api/debts/:id` | Quyền: `debts: sua` | Cập nhật công nợ (`createCrudModule.js`)
91. `DELETE /api/debts/:id` | Quyền: Chặn trực tiếp (400) | Chặn xóa công nợ (`createCrudModule.js:835`)
92. `POST   /api/debts/:id/pay` | Quyền: `debts: sua` | Trả nợ NCC, tự sinh Phiếu chi (`business.route.js:726`)
93. `GET    /api/cash-receipts` | Quyền: `cash-receipts: xem` | Danh sách phiếu thu tiền mặt Mẫu 01-TT (`createCrudModule.js`)
94. `POST   /api/cash-receipts` | Quyền: `cash-receipts: tao` | Lập phiếu thu tiền mặt (`createCrudModule.js`)
95. `PUT    /api/cash-receipts/:id` | Quyền: `cash-receipts: sua` | Cập nhật phiếu thu (`createCrudModule.js`)
96. `DELETE /api/cash-receipts/:id` | Quyền: `cash-receipts: xoa` | Hủy phiếu thu (`createCrudModule.js`)
97. `POST   /api/cash-receipts/:id/confirm` | Quyền: `cash-receipts: sua` | Xác nhận duyệt phiếu thu tiền mặt (`business.route.js:1841`)
98. `GET    /api/cash-payments` | Quyền: `cash-payments: xem` | Danh sách phiếu chi tiền mặt Mẫu 02-TT (`createCrudModule.js`)
99. `POST   /api/cash-payments` | Quyền: `cash-payments: tao` | Lập phiếu chi tiền mặt (`createCrudModule.js`)
100. `PUT   /api/cash-payments/:id` | Quyền: `cash-payments: sua` | Cập nhật phiếu chi (`createCrudModule.js`)
101. `DELETE /api/cash-payments/:id` | Quyền: `cash-payments: xoa` | Hủy phiếu chi (`createCrudModule.js`)
102. `POST  /api/cash-payments/:id/confirm` | Quyền: `cash-payments: sua` | Xác nhận duyệt phiếu chi tiền mặt (`business.route.js:1899`)

### 4.8. Báo cáo & Dashboard
103. `GET   /api/reports/dashboard` | Quyền: `dashboard: xem` (mọi vai trò) | API Dashboard tổng quan (được tài liệu hóa theo UC23; phía client gọi tổng hợp dữ liệu song song qua Promise.allSettled) (`DashboardPage.jsx:56-64`)
104. `GET   /api/reports/revenue` | Quyền: `reports: xem` | Báo cáo doanh thu bán hàng theo ngày/tháng/năm (`reports.route.js:32`)
105. `GET   /api/reports/warehouse` | Quyền: `reports: xem` | Báo cáo nhập – xuất kho tổng hợp (`reports.route.js:310`)
106. `GET   /api/reports/inventory` | Quyền: `reports: xem` | Báo cáo tồn kho (Nhập - Xuất - Tồn) (`reports.route.js:484`)
107. `GET   /api/reports/debts` | Quyền: `reports: xem` | Báo cáo công nợ nhà cung cấp tổng hợp (`reports.route.js:733`)
108. `GET   /api/reports/cash-flow` | Quyền: `reports: xem` | Sổ quỹ thu – chi tổng hợp dòng tiền (`reports.route.js:855`)
109. `GET   /api/reports/cash-receipts` | Quyền: `reports: xem` | Báo cáo thu tiền mặt 8 cột theo Mẫu 01-TT (`reports.route.js:954`)
110. `GET   /api/reports/cash-payments` | Quyền: `reports: xem` | Báo cáo chi tiền mặt 8 cột theo Mẫu 02-TT (`reports.route.js:1089`)
111. `GET   /api/reports/warehouse-receipts` | Quyền: `reports: xem` | Báo cáo nhập kho 11 cột Mẫu 01-VT (`reports.route.js:1224`)
112. `GET   /api/reports/warehouse-issues` | Quyền: `reports: xem` | Báo cáo xuất kho 11 cột Mẫu 02-VT (`reports.route.js:1385`)
113. `GET   /api/reports/bank-receipts` | Quyền: `reports: xem` | Báo cáo thu tiền chuyển khoản ngân hàng (`reports.route.js:1538`)
114. `GET   /api/reports/bank-payments` | Quyền: `reports: xem` | Báo cáo chi tiền chuyển khoản ủy nhiệm chi (`reports.route.js:1624`)
115. `GET   /api/reports/income-statement` | Quyền: `reports: xem` | Báo cáo kết quả HĐKD Mẫu B 02 - DN (`reports.route.js:1695`)
116. `GET   /api/reports/product-ledger` | Quyền: `reports: xem` | Sổ chi tiết hàng hóa Mẫu S10-DN (`reports.route.js:1849`)
117. `GET   /api/reports/general-journal` | Quyền: `reports: xem` | Sổ nhật ký chung Mẫu S03a-DNN (`reports.route.js:2129`)
118. `GET   /api/reports/fixed-assets` | Quyền: `reports: xem` | Sổ tài sản cố định Mẫu S21-DN (Khung mẫu, chưa có dữ liệu) (`reports.route.js:2377`)
119. `GET   /api/reports/sales-by-employee` | Quyền: `reports: xem` | Báo cáo doanh số bán lẻ theo nhân viên (`reports.route.js:2420`)
120. `GET   /api/reports/stocktake-adjustments` | Quyền: `reports: xem` | Báo cáo kiểm kê và điều chỉnh kho (`reports.route.js:2489`)

---

## 5. QUY TẮC TÍCH ĐIỂM & ĐỔI VOUCHER THÀNH VIÊN

Hệ thống triển khai cơ chế khách hàng thân thiết tự động:
1. **Tỷ lệ tích điểm**:
   - Mỗi **10.000 VNĐ** giá trị thanh toán đơn hàng bán lẻ = **1 điểm tích lũy** (`earnedPoints = Math.floor(total / 10000)` tại `backend/src/modules/business/business.route.js:629`).
2. **Phân hạng thành viên** (`business.route.js:412`):
   - Dưới 100 điểm: **Hạng Đồng**
   - Từ 100 đến 499 điểm: **Hạng Bạc**
   - Từ 500 đến 999 điểm: **Hạng Vàng**
   - Từ 1.000 điểm trở lên: **Hạng Kim Cương**
3. **Ngưỡng đổi điểm lấy Voucher** (`POST /api/customers/:id/redeem-voucher` tại `business.route.js:1790-1815`):
   - **`BAC50K`**: Cần **100 điểm** -> Nhận voucher chiết khấu **50.000 VNĐ**.
   - **`VANG100K`**: Cần **500 điểm** -> Nhận voucher chiết khấu **100.000 VNĐ**.
   - **`KC200K`**: Cần **1.000 điểm** -> Nhận voucher VIP chiết khấu **200.000 VNĐ**.

---

## 6. HẠCH TOÁN NỢ / CÓ KẾ TOÁN THỰC TẾ TRONG CODE

### 6.1. Cơ chế sinh Sổ Nhật ký chung
- **TỔNG HỢP ĐỘNG KHI LẬP BÁO CÁO (On-the-fly)**: Hệ thống **KHÔNG CÓ collection lưu sẵn từng bút toán** (không có collection `accounting_entries`).
- Khi người dùng gửi request `GET /api/reports/general-journal` (`reports.route.js:2129-2375`), controller tự động đọc đồng thời 4 collection chứng từ gốc (`HoaDon`, `PhieuNhap`, `PhieuThu`, `PhieuChi`) để sinh các cặp định khoản Nợ/Có theo chuẩn Thông tư 133/2016/TT-BTC.

### 6.2. Chi tiết tình trạng xác minh định khoản trong mã nguồn

| Nghiệp vụ | Định khoản Nợ / Có | Tình trạng xác minh trong mã nguồn | Căn cứ mã nguồn (file:dòng) & Ghi chú |
| :--- | :--- | :---: | :--- |
| **Bán hàng: Doanh thu** | Nợ 111 (đã thanh toán) hoặc Nợ 131 (chưa thanh toán) / Có 511 | **ĐÃ XÁC MINH** | `reports.route.js:2176-2200`. **Lưu ý**: Code kiểm tra `inv.TrangThai === "Đã thanh toán" ? "111" : "131"`. Bán hàng thu tiền qua VietQR/chuyển khoản **KHÔNG dùng TK 112** trong Sổ nhật ký chung, mà ghi nhận vào TK 111. |
| **Bán hàng: Giá vốn** | Nợ 632 / Có 156 | **ĐÃ XÁC MINH** | `reports.route.js:2204-2232`. Giá vốn được tính theo `GiaNhap` sản phẩm nhân với số lượng xuất bán. |
| **Nhập kho hàng hóa** | Nợ 156 / Có 331 | **ĐÃ XÁC MINH** | `reports.route.js:2235-2270`. Ghi tăng giá trị kho hàng đối ứng tăng công nợ phải trả NCC. |
| **Thu tiền mặt** | Nợ 111 / Có 131 | **ĐÃ XÁC MINH** | `reports.route.js:2273-2305`. Ghi nhận từ các chứng từ `PhieuThu`. |
| **Chi tiền mặt** | Nợ 331 (trả nợ NCC) hoặc Nợ 641/642 (chi phí) / Có 111 | **ĐÃ XÁC MINH** | `reports.route.js:2308-2344`. Phân loại tài khoản Nợ dựa trên nội dung lý do chi tiền. |
| **Đổi trả hàng (`PhieuTraHang`)** | Nhập hoàn lại kho / Giảm trừ doanh thu | **CHƯA XÁC MINH SINH BÚT TOÁN NỢ/CÓ** | `business.route.js:1739`. Code chỉ gọi `adjustStock(lines, 1)` để **cộng hoàn lại số lượng tồn kho**; **KHÔNG SINH BÚT TOÁN Nợ 521 / Có 111/131 hay Nợ 156 / Có 632** vào Sổ nhật ký chung. |
| **Kiểm kê thừa/thiếu kho** | Cân bằng kho / Xử lý chênh lệch | **CHƯA XÁC MINH SINH BÚT TOÁN NỢ/CÓ** | `business.route.js:1451-1469`, `reports.route.js:2489`. Code chỉ cập nhật số lượng tồn thực tế vào `TonKho` và ghi vào `DieuChinhKho`; **KHÔNG ĐỊNH KHOẢN Nợ 1381/Có 156 hay Nợ 156/Có 3381** vào Sổ nhật ký chung. |

---

## 7. HỆ THỐNG 17 BÁO CÁO KẾ TOÁN & QUẢN TRỊ THỰC TẾ

| STT | Route API Backend | Tên hiển thị nguyên văn (`ReportPage.jsx` / `reports.route.js`) | Bản chất nghiệp vụ & Dữ liệu thực tế |
| :---: | :--- | :--- | :--- |
| 1 | `GET /revenue` | **Báo cáo doanh thu bán hàng** | Doanh thu thuần, tiền giảm giá, lợi nhuận gộp theo ngày/tháng/năm, nhóm hàng và khách hàng |
| 2 | `GET /warehouse` | **Báo cáo nhập – xuất kho (Tổng hợp)** | Tổng hợp lượng nhập/xuất/tồn đầu kỳ và cuối kỳ toàn bộ mặt hàng |
| 3 | `GET /inventory` | **Báo cáo tồn kho (Nhập - Xuất - Tồn)** | Chi tiết số lượng tồn, giá trị vốn tồn kho, cảnh báo tồn dưới định mức an toàn |
| 4 | `GET /debts` | **Báo cáo công nợ tổng hợp** | Chi tiết công nợ phải trả NCC theo phiếu nhập, tuổi nợ và phân loại trạng thái thanh toán |
| 5 | `GET /cash-flow` | **Sổ quỹ thu – chi (Tổng hợp)** | Sổ quỹ tiền mặt tổng hợp, tồn quỹ đầu kỳ, tổng thu, tổng chi, tồn quỹ cuối kỳ |
| 6 | `GET /cash-receipts` | **Báo cáo thu tiền mặt (8 cột độc lập)** | Bảng kê chi tiết chứng từ thu tiền mặt theo chuẩn biểu mẫu kế toán Mẫu 01-TT |
| 7 | `GET /cash-payments` | **Báo cáo chi tiền mặt (8 cột độc lập)** | Bảng kê chi tiết chứng từ chi tiền mặt theo chuẩn biểu mẫu kế toán Mẫu 02-TT |
| 8 | `GET /warehouse-receipts` | **Báo cáo nhập kho (11 cột độc lập)** | Bảng kê phiếu nhập kho theo chuẩn Thông tư Mẫu số 01-VT |
| 9 | `GET /warehouse-issues` | **Báo cáo xuất kho (11 cột độc lập)** | Bảng kê phiếu xuất kho theo chuẩn Thông tư Mẫu số 02-VT |
| 10 | `GET /bank-receipts` | **Báo cáo thu tiền chuyển khoản (Ngân hàng)** | **Bản chất**: Lọc các giao dịch thanh toán hóa đơn (`ThanhToan`) có hình thức chuyển khoản/ngân hàng. **Không kết nối ngân hàng trực tuyến**, không phải sao kê online tự động |
| 11 | `GET /bank-payments` | **Báo cáo chi tiền chuyển khoản (Ủy nhiệm chi)** | **Bản chất**: Lọc các giao dịch xuất quỹ (`PhieuChi`) có hình thức chuyển khoản/UNC thanh toán cho nhà cung cấp |
| 12 | `GET /income-statement` | **Báo cáo kết quả HĐKD (Mẫu B 02 - DN)** | Báo cáo tài chính P&L: Doanh thu bán hàng (511), Giảm trừ (521), Giá vốn (632), Lợi nhuận gộp, Chi phí bán hàng & quản lý (641, 642) |
| 13 | `GET /product-ledger` | **Sổ chi tiết hàng hóa (Mẫu S10-DN)** | Thẻ kho chi tiết từng mặt hàng: ngày chứng từ, diễn giải, đơn giá, số lượng nhập/xuất/tồn tức thời |
| 14 | `GET /general-journal` | **Sổ nhật ký chung (Mẫu S03a-DNN)** | Sổ cái kế toán tổng hợp toàn bộ các cặp định khoản Nợ/Có (111, 131, 156, 331, 511, 632, 641, 642) theo chuẩn TT 133/2016/TT-BTC |
| 15 | `GET /fixed-assets` | **Sổ tài sản cố định (Mẫu S21-DN)** | **Bản chất: STUB MẪU (Chưa khả dụng)**: Code trả về `isModuleAvailable: false`, `data: []`. **MÃ NGUỒN KHÔNG THỰC SỰ TÍNH KHẤU HAO TSCĐ**. Báo cáo ghi trung thực: 16 báo cáo đầy đủ dữ liệu + 1 biểu mẫu khung TSCĐ |
| 16 | `GET /sales-by-employee` | **Báo cáo doanh số bán hàng theo nhân viên** | Thống kê số lượng đơn và doanh thu bán lẻ phân bổ theo từng nhân viên thu ngân |
| 17 | `GET /stocktake-adjustments` | **Báo cáo kiểm kê và điều chỉnh kho** | Bảng kê chênh lệch thừa/thiếu giữa tồn thực tế và tồn hệ thống kèm giá trị quy đổi và lý do điều chỉnh |

---

## 8. XÁC MINH CÁC TÍNH NĂNG ĐẶC THÙ & QUY TẮC TOÀN VẸN

| Tính năng | Trạng thái thực tế | Bằng chứng mã nguồn (file:dòng) | Giải thích kỹ thuật |
| :--- | :---: | :--- | :--- |
| **Quản lý Hạn sử dụng (HSD) & Hàng cận date** | **CÓ** | `createCrudModule.js:64,89`, `seed.js:142-340`, `NotificationPopover.jsx:82-107` | Mỗi sản phẩm bắt buộc có trường `HanSuDung` (YYYY-MM-DD). Hệ thống tự động quét và phát cảnh báo: "Quá hạn sử dụng" (khi ngày âm) và "Cận date" (còn dưới 60 ngày). |
| **Đổi điểm tích lũy lấy Voucher** | **CÓ** | `business.route.js:1785-1839`, `CustomersPage.jsx` | Có route riêng `POST /api/customers/:id/redeem-voucher`. Trừ điểm tích lũy và cấp các mã voucher: `BAC50K` (50.000đ), `VANG100K` (100.000đ), `KC200K` (200.000đ). |
| **Các collection `price_history`, `notifications`, `settings`, `accounting_entries`** | **KHÔNG CÓ** | Toàn bộ `backend/src/` không có | Hệ thống không tạo collection MongoDB riêng cho các đối tượng này. Thông báo được tính realtime phía client; cấu hình lưu tại `storeConfig.js`; nhật ký chung tổng hợp on-the-fly. |
| **Quy định độ dài mật khẩu tối thiểu** | **CÓ (>= 6)** | `accounts.route.js:35`, `auth.route.js:150` | Mật khẩu tạo mới và đổi mật khẩu bắt buộc phải từ 6 ký tự trở lên. |
| **Chặn tự khóa / tự xóa tài khoản của chính mình** | **CÓ** | `accounts.route.js:213-216, 264-265` | Chặn người dùng tự khóa hoặc tự xóa tài khoản của mình. Chặn khóa/xóa quản trị viên `QuanLy` duy nhất của hệ thống (`accounts.route.js:221-229, 267-275`). |
| **Chặn xóa Loại hàng & NCC có ràng buộc** | **CÓ** | `createCrudModule.js:879-894, 896-921` | Không cho phép xóa Loại hàng nếu đang có sản phẩm. Với NCC, Khách hàng, Sản phẩm đã phát sinh chứng từ, hệ thống tự động chuyển sang cơ chế xóa mềm (Soft-delete: `TrangThai: "Ngưng hoạt động"` hoặc `"Ngừng bán"`). |
| **Chặn xóa vật lý chứng từ kế toán** | **CÓ** | `createCrudModule.js:960-973` | Danh sách `PROTECTED_VOUCHERS` (`PhieuNhap`, `HoaDon`, `DonHang`, `PhieuXuat`, `DonDatHang`) bị chặn xóa vật lý tuyệt đối; chứng từ sai sót chỉ được hủy qua trạng thái. |
| **Chặn bán âm kho & Rollback giao dịch** | **CÓ** | `business.route.js:42-72`, `mongodb.js:37-58` | Hàm `adjustStock` sử dụng atomic update `$inc` kèm điều kiện `$gte: quantity`. Nếu thiếu hàng lập tức ném lỗi 409 và thực hiện rollback thủ công hoàn lại các mặt hàng đã trừ trước đó. |
| **Quét mã vạch (Barcode Scanner)** | **KHÔNG CÓ** | `SalesPOSPage.jsx:75-88` | Không có thư viện quét camera/mã vạch. Tìm kiếm sản phẩm tại quầy bằng nhập liệu ô tìm kiếm hoặc phím tắt F2. |
| **VietQR thanh toán** | **CÓ (ĐỘNG)** | `frontend/src/config/storeConfig.js:45-60`, `SalesPOSPage.jsx` | Tự động sinh mã VietQR động chuẩn NAPAS qua API `img.vietqr.io` với đúng số tiền thanh toán và mã hóa đơn bán lẻ. |

---

## 9. PHÂN QUYỀN VAI TRÒ & QUY TRÌNH DUYỆT CÂN BẰNG KHO

### 9.1. Ma trận 5 vai trò hệ thống (`VaiTro`)
Hệ thống lưu trữ 5 vai trò nghiệp vụ với mã số chuẩn từ 1 đến 5 (`backend/src/config/seed.js:12-18`):
1. **Mã 1 - Quản lý (`QuanLy`)**: Toàn quyền xem, tạo, sửa, xóa trên toàn bộ 24 phân hệ của hệ thống.
   *(Lưu ý: `QuanTriHeThong` không phải vai trò độc lập riêng biệt trong DB mà là alias quyền lực cao nhất được tích hợp song song với `QuanLy` trong mã nguồn backend để bypass kiểm tra quyền).*
2. **Mã 2 - Nhân viên bán hàng (`NhanVienBanHang`)**:
   - Ghi (Toàn quyền): `customers`, `sales-orders`, `invoices`, `payments`, `returns`, `promotions`, `cash-receipts`.
   - Đọc (Chỉ xem): `dashboard`, `products`, `product-categories`, `inventory`.
3. **Mã 3 - Nhân viên kho (`NhanVienKho` / `ThuKho`)**:
   - Ghi (Toàn quyền): `products`, `product-categories`, `goods-receipts`, `goods-issues`, `inventory`, `stocktakes`.
   - Đọc (Chỉ xem): `dashboard`, `purchase-orders`, `sales-orders`, `returns`.
4. **Mã 4 - Kế toán (`KeToan`)**:
   - Ghi (Toàn quyền): `invoices`, `payments`, `debts`, `reports`, `cash-receipts`, `cash-payments`.
   - Đọc (Chỉ xem): `dashboard`, `customers`, `suppliers`, `products`, `purchase-orders`, `goods-receipts`, `sales-orders`, `returns`, `inventory`.
5. **Mã 5 - Nhân viên mua hàng (`NhanVienMuaHang`)**:
   - Ghi (Toàn quyền): `suppliers`, `purchase-orders`, `goods-receipts`.
   - Đọc (Chỉ xem): `dashboard`, `products`, `product-categories`, `inventory`, `debts`.

### 9.2. Thủ kho có được tự bấm Cân bằng kho không?
- **KẾT LUẬN: THỦ KHO ĐƯỢC PHÉP TỰ BẤM CÂN BẰNG KHO**.
- **Căn cứ mã nguồn**:
  + Route xử lý: `POST /api/stocktakes/:id/adjust` yêu cầu quyền `requirePermission("stocktakes", "sua")` (`business.route.js:1408`).
  + Trong cấu hình phân quyền `permissions.js:45, 49`: `NhanVienKho` (và `ThuKho`) được gán danh sách quyền ghi (`write`) gồm có `stocktakes`.
  + Do đó, Nhân viên kho có đầy đủ quyền `"sua"` trên module `stocktakes` và có thể trực tiếp bấm nút "Cân bằng kho" trên giao diện `StocktakePage.jsx:531-533` mà **không bắt buộc phải chờ tài khoản Quản lý phê duyệt**.

### 9.3. Danh mục Phím tắt hệ thống thực tế
- **Tại màn hình POS Bán hàng** (`SalesPOSPage.jsx:75-88`):
  + **`F2`**: Focus và bôi đen ô tìm kiếm sản phẩm.
  + **`F4`**: Mở danh sách và focus tìm kiếm khách hàng.
  + **`F8`**: Focus ô nhập mã khuyến mãi / voucher.
- **Toàn hệ thống** (`AppLayout.jsx:157-183`, `ShortcutsHelpModal.jsx:5-24`):
  + **`Ctrl + K`**: Mở thanh tìm kiếm nhanh (Command Palette).
  + **`Ctrl + B`**: Thu gọn hoặc mở rộng Sidebar menu.
  + **`?`**: Mở modal hướng dẫn phím tắt hệ thống.
  + **`F2`**: Điều hướng nhanh vào màn hình Bán hàng POS (`/sales-orders`).
  + **`F9`**: Điều hướng nhanh vào phân hệ Báo cáo (`/reports`).
  + **`Esc`**: Đóng modal / hủy thao tác.
  + **`Enter`**: Xác nhận hộp thoại.

---

## 10. ĐỐI CHIẾU PHÂN CÔNG ĐỦ 6 THÀNH VIÊN VÀ MÂU THUẪN VỚI README

Toàn bộ commit trên kho lưu trữ chỉ ghi nhận 1 tài khoản Git duy nhất là `GaHwi0710`. Dưới đây là bảng đối chiếu nguyên văn phân công của đủ 6 thành viên giữa Phụ lục A (Báo cáo Word) và Mục XV (README):

| STT | Họ và tên & MSSV | Phân công trong Phụ lục A (Báo cáo Word cũ `baocaobtl.docx`) | Phân công nguyên văn trong `README.md` (Mục XV) |
| :---: | :--- | :--- | :--- |
| 1 | **Kiều Gia Huy**<br>MSSV: 2354800081 | Lập trình Module Mua hàng, Báo cáo thống kê, Phiếu Chi và gói 10 chức năng nâng cao (tìm kiếm nhanh, lọc, phân trang, in HĐ, xuất Excel/PDF, biểu đồ, QR, email, audit log, sao lưu). | **Kiến trúc hệ thống, Backend API, CSDL MongoDB, Tích hợp RBAC & Báo cáo** *(Nhóm trưởng)* |
| 2 | **Ngô Gia Huy**<br>MSSV: 2354800106 | Phân tích nghiệp vụ; Lập trình Module Quản lý sản phẩm, Loại hàng, Công nợ nhà cung cấp. | **Phát triển giao diện bán lẻ POS, Quản lý khách hàng & Tích điểm thành viên** |
| 3 | **Nguyễn Trung Đức**<br>MSSV: 2354800027 | Mô tả doanh nghiệp; Lập trình Module Kho hàng, Thẻ kho và Kiểm kê định kỳ. | **Nghiệp vụ Mua hàng, Nhập kho, Quản lý nhà cung cấp & Thủ kho** |
| 4 | **Đinh Tiến Đạt**<br>MSSV: 2354800079 | Thiết kế giao diện người dùng; Lập trình Module Đăng nhập, phân quyền xác thực JWT. | **Nghiệp vụ Kiểm kê kho, Cân bằng chênh lệch & Điều chỉnh tồn kho** |
| 5 | **Nguyễn Duy Anh**<br>MSSV: 2354800063 | Thiết kế CSDL MongoDB; Lập trình Module Quản lý Nhà cung cấp và Khách hàng. | **Nghiệp vụ Thu chi tiền mặt, Chứng từ mẫu 01-TT, 02-TT & Quản lý công nợ** |
| 6 | **Nguyễn Đình Tiền Hải**<br>MSSV: 2354800071 | Phân tích hệ thống (UML: Actor, Use Case, Activity Diagram); Lập trình Module Bán hàng tại quầy và chức năng Phiếu Thu. | **Xây dựng Dashboard thống kê, Biểu đồ trực quan hóa & Báo cáo tài chính** |

> `[CẦN XÁC NHẬN: Nhóm thống nhất lựa chọn giữ nguyên danh sách phân công theo Phụ lục A của báo cáo Word hay chuyển theo Mục XV của README trước khi nộp bản in chính thức cho Giảng viên hướng dẫn]`.

---

## 11. TỔNG HỢP LỖI CỦA BÁO CÁO WORD VÀ LỖI CỦA README

### 11.1. Các lỗi sai trong Báo cáo Word cũ (`baocaobtl.docx`)
1. **Tên cơ sở dữ liệu**: Báo cáo ghi `mom_baby_store` -> Thực tế code kết nối `baby_shop_management` (`backend/src/config/mongodb.js:4`).
2. **Số lượng và tên bảng**: Báo cáo ghi "25 collection tiếng Anh" (`users`, `products`, `orders`...) -> Thực tế code dùng 31 collection tiếng Việt chuẩn hóa + `Users` (`ensure-indexes.js`, `backup.route.js:20-52`).
3. **ORM/ODM Mongoose**: Báo cáo nhắc Mongoose ở một số đoạn -> Thực tế code dùng MongoDB Native Driver 7.5.0, không cài Mongoose.
4. **Thuật toán băm mật khẩu**: Báo cáo ghi `bcryptjs` -> Thực tế code dùng `scryptSync` từ module chuẩn `node:crypto`.
5. **Thư viện biểu đồ**: Báo cáo ghi `Recharts` -> Thực tế code tự dựng các component SVG thuần React trong `Charts.jsx`.
6. **Thư viện xuất Excel**: Báo cáo ghi thư viện `xlsx` (SheetJS) -> Thực tế code dùng tiện ích thuần `exportToExcel` tạo HTML/XML Spreadsheet `.xls`.
7. **Quét mã vạch Barcode**: Báo cáo mô tả quét barcode bằng camera/thiết bị -> Thực tế code chỉ có ô tìm kiếm bằng text (phím tắt F2).
8. **VietQR thanh toán**: Báo cáo ghi QR tĩnh -> Thực tế là VietQR động chuẩn NAPAS sinh tự động theo số tiền hóa đơn (`storeConfig.js:45-60`).
9. **Khấu hao Tài sản cố định**: Báo cáo mô tả tính khấu hao TSCĐ -> Thực tế endpoint `/reports/fixed-assets` chỉ là stub mẫu (`isModuleAvailable: false`), code không có logic tính khấu hao.
10. **Bảng không tồn tại**: Báo cáo thiết kế các bảng `accounting_entries`, `price_history`, `notifications`, `settings`, `backups` -> Thực tế mã nguồn không có các bảng này.

### 11.2. Các điểm lỗi thời hoặc không khớp trong `README.md`
1. **Thuật toán băm mật khẩu**: README dòng 242 ghi "thuật toán SHA-256 kết hợp mã muối Salt" -> Thực tế code dùng hàm `scryptSync` (kdf `scrypt`) từ `node:crypto` (`backend/src/modules/auth/password.js:3-12`).
2. **Định dạng xuất Excel**: README dòng 200 ghi "file Excel (.xlsx / .csv)" -> Thực tế hàm `exportToExcel` (`exportUtils.js:42`) tạo tệp HTML/XML Spreadsheet với đuôi `.xls` (không phải file nhị phân nén `.xlsx`).
3. **Lưu trữ ảnh sản phẩm**: README dòng 139 ghi "Lưu trữ liên kết ảnh sản phẩm..." -> Thực tế khi người dùng thêm sản phẩm và chọn ảnh, client nén Canvas thành chuỗi Base64 và lưu trực tiếp chuỗi Base64 đó vào trường `HinhAnh` của MongoDB.
4. **Phím tắt hệ thống**: README dòng 220 ghi "F1: Mở bán hàng POS, F2: Nhập kho, F3: Danh mục sản phẩm" -> Thực tế trong code: `F2` là Mở bán hàng POS, `F9` là Báo cáo, `Ctrl+K` là Command Palette (`AppLayout.jsx:173-178`), không có phím `F1` hay `F3`.
5. **Luồng Cân bằng kho**: README dòng 687 vẽ sơ đồ "Quản lý duyệt Cân bằng kho?" -> Thực tế Thủ kho (`NhanVienKho`) có quyền `"sua"` trên module `stocktakes` nên tự bấm nút Cân bằng kho trực tiếp, không bắt buộc Quản lý duyệt.
6. **Collection hệ thống**: README dòng 268 ghi `Backups, _metadata` thuộc System Collections -> Thực tế `Backups` không phải là collection MongoDB mà là thư mục file JSON trên đĩa `backups/`.
7. **Quản lý công nợ hai chiều**: README dòng 55 ghi công nợ hai chiều -> Trong code, bảng `CongNo` có trường `LoaiCongNo` ("Nhà cung cấp" / "Khách hàng"), tuy nhiên giao diện phân hệ Công nợ (`DebtsPage.jsx`) chỉ quản lý công nợ NCC; nợ khách hàng được theo dõi trực tiếp qua `HoaDon.ConNo` và thu nợ tại trang Hóa đơn.

---

## 12. CĂN CỨ NỘI DUNG CHƯƠNG 3 (ĐỐI CHIẾU MÃ NGUỒN THỰC TẾ)

### 12.1. Cấu trúc trường thực tế của Collection `CongNo`
- **Căn cứ mã nguồn**:
  - `backend/src/modules/business/business.route.js:194-211`: Phát sinh công nợ phải trả khi lập Phiếu nhập kho (`LoaiCongNo: "Nhà cung cấp"`, `type: "suppliers"`, `MaCN`, `MaNCC`, `MaDDH`, `MaPN`, `MaNV`, `partnerName`, `TenNCC`, `NgayPhatSinh`, `SoTien`, `SoTienDaTra`, `SoTienConLai`, `TrangThai: debtStatus`, `createdAt`).
  - `backend/src/modules/business/business.route.js:536-552`: Phát sinh công nợ phải thu khi bán chịu POS (`LoaiCongNo: "Khách hàng"`, `MaCN`, `MaKH`, `MaKHCode`, `TenKH`, `MaDH`, `MaHD`, `MaNV`, `SoTien`, `SoTienDaTra: 0`, `SoTienConLai: total`, `TrangThai: "Còn nợ"`, `NgayPhatSinh`, `createdAt`, `updatedAt`).
  - `backend/src/modules/business/business.route.js:726-975`: Thanh toán công nợ (`POST /api/debts/:id/pay`) xử lý thanh toán cho cả 2 chiều:
    + Trả nợ NCC: Giảm trừ công nợ `CongNo`, đồng bộ `PhieuNhap.SoTienDaTra`, tự sinh bản ghi `ThanhToan` (`LoaiThanhToan: "Chi trả NCC"`) và tự động tạo `PhieuChi`.
    + Thu nợ KH: Giảm trừ công nợ `CongNo`, đồng bộ `HoaDon.SoTienDaTra`, tự sinh bản ghi `ThanhToan` (`LoaiThanhToan: "Thu nợ KH"`) và tự động tạo `PhieuThu`.
- **Kết luận đối chiếu**: Collection `CongNo` trong CSDL thật sự hỗ trợ cấu trúc hai chiều (`LoaiCongNo`: "Nhà cung cấp" | "Khách hàng"). Bảng 3.2.27 trong báo cáo phản ánh chính xác cấu trúc dữ liệu backend này. Tuy nhiên, về mặt trải nghiệm UI, màn hình `DebtsPage.jsx` tập trung quản lý công nợ NCC; công nợ khách hàng được theo dõi song song qua trường `HoaDon.SoTienConLai` và thu nợ tại `InvoicePage.jsx`.

### 12.2. Các quy tắc ràng buộc toàn vẹn dữ liệu (Mục 3.4)
- **Căn cứ mã nguồn**:
  - **CCCD 12 chữ số**: `backend/src/modules/accounts/accounts.route.js:36` (`!/^[0-9]{12}$/.test(String(body.CCCD).trim())` -> "Số CCCD phải gồm đúng 12 chữ số hợp lệ").
  - **Số điện thoại 10–11 số bắt đầu bằng 0**: `backend/src/modules/shared/createCrudModule.js:99` (`!/^0\d{9,10}$/.test(String(body.SDT).trim())` -> "Số điện thoại phải gồm 10-11 chữ số và bắt đầu bằng 0").
  - **Đơn giá không âm và Giá bán >= Giá nhập**: `backend/src/modules/shared/createCrudModule.js:72-87` (`giaNhap < 0` -> "Giá nhập phải là số không âm"; `giaBan < giaNhap` -> "Giá bán không được nhỏ hơn giá nhập").
  - **Hạn sử dụng bắt buộc đối với sản phẩm Mẹ & Bé**: `backend/src/modules/shared/createCrudModule.js:64, 89` (Danh sách trường bắt buộc của SanPham có `HanSuDung`; `!body.HanSuDung || isNaN(Date.parse(body.HanSuDung))` -> "Hạn sử dụng không hợp lệ hoặc chưa nhập").
  - **Số lượng nhập/xuất phải là số nguyên dương (> 0)**: `backend/src/modules/business/business.route.js:33` (`!Number.isInteger(quantity) || quantity <= 0` -> "Số lượng phải là số nguyên dương").
  - **Số lượng tồn kho an toàn tối thiểu mặc định 10**: `backend/src/modules/business/business.route.js:1775` (`SoLuongToiThieu: Number(product.SoLuongToiThieu || 10)`).

### 12.3. Giá trị Enum của `ThanhToan` và Danh sách Action của `AuditLogs`
- **Căn cứ mã nguồn**:
  - `ThanhToan`:
    + `PhuongThuc`: "Tiền mặt", "Chuyển khoản" (và mã quét VietQR động NAPAS trên giao diện).
    + `TrangThai`: "Đã thanh toán" (giao dịch thanh toán ghi nhận thành công).
    + `LoaiThanhToan`: "Chi trả NCC", "Thu nợ KH" (đối với thanh toán công nợ theo `business.route.js:878, 962`).
  - `AuditLogs` (`backend/src/modules/audit/audit.service.js` và toàn bộ backend):
    + Danh sách 16 mã hành động (`action`) thực tế trong code: `BACKUP`, `CHANGE_PASSWORD`, `CONFIRM`, `CREATE`, `CREATE_INVOICE`, `DEBT_PAYMENT`, `DELETE`, `EMAIL_INVOICE`, `LOGIN`, `LOGOUT`, `PURCHASE`, `RESTORE`, `ROLE_PERMISSION_CHANGE`, `STOCKTAKE`, `STOCK_ADJUSTMENT`, `UPDATE`.

### 12.4. Bản chất của việc "Hạch toán Nợ/Có tự động"
- **Căn cứ mã nguồn**: `backend/src/modules/reports/reports.route.js:2126-2360` (`GET /api/reports/general-journal`).
- **Bản chất hạch toán**:
  - Hệ thống **KHÔNG** sử dụng bảng CSDL tĩnh `accounting_entries` trong MongoDB. Không ghi nhận sẵn từng dòng định khoản rời rạc khi người dùng thao tác nghiệp vụ.
  - Sổ nhật ký chung (Mẫu S03a-DNN) được **TỔNG HỢP ĐỘNG ON-THE-FLY** tại thời điểm truy vấn báo cáo, bằng cách quét trực tiếp các chứng từ gốc (`HoaDon`, `PhieuNhap`, `PhieuThu`, `PhieuChi`) và tự động sinh các cặp tài khoản Nợ/Có tương ứng:
    + Nghiệp vụ Bán hàng: Nợ TK 111 (hoặc Nợ TK 131 nếu bán nợ) / Có TK 511, Có TK 33311; đồng thời tự động ghi nhận Giá vốn: Nợ TK 632 / Có TK 156.
    + Nghiệp vụ Nhập kho mua hàng: Nợ TK 156 / Có TK 331 (hoặc Có TK 111 nếu thanh toán ngay).
    + Nghiệp vụ Thu tiền mặt: Nợ TK 111 / Có TK 131.
    + Nghiệp vụ Chi tiền mặt thanh toán NCC: Nợ TK 331 / Có TK 111.
    *(Hệ thống không sử dụng tài khoản Tiền gửi ngân hàng 112 do các giao dịch thanh toán chuyển khoản được hạch toán trực tiếp hoặc quy đổi sang dòng tiền quỹ phục vụ cửa hàng bán lẻ)*.

