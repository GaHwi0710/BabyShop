import sys
import docx
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl

sys.stdout.reconfigure(encoding='utf-8')

# 31 Collections Data
COLLECTIONS_DATA = [
    # Nhóm 1: Quản lý người dùng & phân quyền
    {
        "group": "Nhóm 1 - Quản lý người dùng & phân quyền",
        "num": "3.2.1",
        "name": "Users",
        "desc": "Lưu trữ tài khoản đăng nhập, thông tin định danh và trạng thái truy cập của người dùng trên toàn hệ thống.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh của MongoDB"],
            ["username", "String", "Unique, Bắt buộc", "Tên đăng nhập duy nhất vào hệ thống"],
            ["passwordHash", "String", "Bắt buộc", "Băm mật khẩu an toàn bằng thuật toán scrypt + Salt 16 bytes"],
            ["fullName", "String", "Bắt buộc", "Họ và tên đầy đủ của người sử dụng"],
            ["role", "String", "Bắt buộc", "Tên vai trò phân quyền (QuanLy, NhanVienBanHang, ThuKho...)"],
            ["status", "String", "Bắt buộc", "Trạng thái tài khoản: 'Hoạt động', 'Đã khóa'"],
            ["email", "String", "Tùy chọn", "Địa chỉ thư điện tử người dùng"],
            ["phone", "String", "Tùy chọn", "Số điện thoại liên lạc"],
            ["CCCD", "String", "12 chữ số", "Số Căn cước công dân của nhân sự"],
            ["createdAt", "Date", "Tự động", "Thời điểm khởi tạo tài khoản"],
            ["updatedAt", "Date", "Tự động", "Thời điểm cập nhật hồ sơ gần nhất"]
        ]
    },
    {
        "group": None,
        "num": "3.2.2",
        "name": "VaiTro",
        "desc": "Quản lý 5 vai trò hệ thống chuẩn (mã 1-5) và ma trận phân quyền chi tiết (xem, tao, sua, xoa) trên 24 phân hệ.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaVaiTro", "Number", "Unique, (1-5)", "Mã định danh vai trò số nguyên (1: Quản lý, 2: Bán hàng, 3: Kho, 4: Kế toán, 5: Mua hàng)"],
            ["TenVaiTro", "String", "Bắt buộc", "Tên hiển thị của vai trò"],
            ["MaKey", "String", "Unique, Bắt buộc", "Khóa mã hóa vai trò (QuanLy, NhanVienBanHang, NhanVienKho, KeToan, NhanVienMuaHang)"],
            ["LaVaiTroHeThong", "Boolean", "Bắt buộc", "Đánh dấu vai trò tích hợp sẵn của hệ thống"],
            ["MoTa", "String", "Tùy chọn", "Mô tả trách nhiệm nghiệp vụ"],
            ["QuyenHan", "Object", "Bắt buộc", "Ma trận phân quyền chi tiết (xem, tao, sua, xoa) trên 24 phân hệ"],
            ["createdAt", "Date", "Tự động", "Thời điểm khởi tạo vai trò"]
        ]
    },
    # Nhóm 2: Danh mục đối tác & hàng hóa
    {
        "group": "Nhóm 2 - Danh mục đối tác & hàng hóa",
        "num": "3.2.3",
        "name": "NhanVien",
        "desc": "Quản lý hồ sơ lý lịch nhân sự, phòng ban, chức vụ và liên kết với tài khoản người dùng đăng nhập.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaNV", "String", "Unique, Tự sinh (NVxxx)", "Mã định danh nhân viên"],
            ["HoTen", "String", "Bắt buộc", "Họ và tên đầy đủ nhân sự"],
            ["ChucVu", "String", "Tùy chọn", "Chức danh chuyên môn (Thu ngân, Thủ kho, Kế toán viên...)"],
            ["PhongBan", "String", "Tùy chọn", "Bộ phận công tác (Bán hàng, Kho vận, Kế toán...)"],
            ["SDT", "String", "10-11 số", "Số điện thoại liên hệ"],
            ["Email", "String", "Email hợp lệ", "Thư điện tử công vụ"],
            ["DiaChi", "String", "Tùy chọn", "Nơi cư trú liên hệ"],
            ["CCCD", "String", "12 chữ số", "Số Căn cước công dân"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đang làm việc', 'Đã nghỉ việc'"],
            ["username", "String", "Tham chiếu Users", "Tên tài khoản liên kết đăng nhập"],
            ["VaiTro", "String", "Tùy chọn", "Tên vai trò phân công"],
            ["MaVaiTro", "Number", "Tham chiếu VaiTro", "Mã vai trò số nguyên (1-5)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.4",
        "name": "KhachHang",
        "desc": "Quản lý hồ sơ khách hàng, số điện thoại, điểm thưởng tích lũy (10.000đ = 1 điểm) và hạng thành viên.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaKH", "String", "Unique, Tự sinh (KHxxx)", "Mã quản lý khách hàng"],
            ["HoTen", "String", "Bắt buộc", "Tên khách hàng / người mua hàng"],
            ["SDT", "String", "Unique, 10-11 số", "Số điện thoại định danh khách hàng"],
            ["Email", "String", "Tùy chọn", "Email nhận hóa đơn điện tử"],
            ["DiaChi", "String", "Tùy chọn", "Địa chỉ giao hàng"],
            ["MaSoThue", "String", "Tùy chọn", "Mã số thuế cá nhân / doanh nghiệp"],
            ["DiemTichLuy", "Number", "Mặc định: 0", "Điểm thưởng tích lũy (10.000 VNĐ thanh toán = 1 điểm)"],
            ["CapThanhVien", "String", "Tự động tính", "Hạng thành viên: Đồng (<100đ), Bạc (100-499đ), Vàng (500-999đ), Kim Cương (>=1000đ)"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đang hoạt động', 'Ngưng hoạt động'"],
            ["createdAt", "Date", "Tự động", "Ngày đăng ký hồ sơ khách hàng"]
        ]
    },
    {
        "group": None,
        "num": "3.2.5",
        "name": "NhaCungCap",
        "desc": "Quản lý danh sách nhà cung cấp, nhà phân phối chính thức sản phẩm mẹ và bé.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaNCC", "String", "Unique, Tự sinh (NCCxxx)", "Mã nhà cung cấp hàng hóa"],
            ["TenNCC", "String", "Bắt buộc", "Tên công ty phân phối / nhà sản xuất"],
            ["NguoiLienHe", "String", "Tùy chọn", "Người đại diện kinh doanh"],
            ["SDT", "String", "10-11 số", "Số điện thoại liên lạc đặt hàng"],
            ["Email", "String", "Tùy chọn", "Email đặt hàng và nhận báo giá"],
            ["DiaChi", "String", "Tùy chọn", "Địa chỉ trụ sở / kho hàng của NCC"],
            ["MaSoThue", "String", "Tùy chọn", "Mã số thuế doanh nghiệp"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đang hoạt động', 'Ngưng hoạt động'"],
            ["createdAt", "Date", "Tự động", "Ngày thiết lập hồ sơ đối tác"]
        ]
    },
    {
        "group": None,
        "num": "3.2.6",
        "name": "LoaiHang",
        "desc": "Danh mục phân loại ngành hàng chuyên biệt cho mẹ và bé (Sữa bột, Bỉm tã, Quần áo sơ sinh, Đồ chơi...).",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaLoai", "String", "Unique, Tự sinh (LHxxx)", "Mã phân loại ngành hàng"],
            ["TenLoai", "String", "Bắt buộc", "Tên phân nhóm sản phẩm"],
            ["MoTa", "String", "Tùy chọn", "Mô tả đặc điểm ngành hàng"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đang hoạt động', 'Ngưng hoạt động'"],
            ["createdAt", "Date", "Tự động", "Ngày tạo nhóm hàng"]
        ]
    },
    {
        "group": None,
        "num": "3.2.7",
        "name": "SanPham",
        "desc": "Danh mục sản phẩm kinh doanh, giá nhập/bán, hạn sử dụng bắt buộc, định mức tồn kho tối thiểu và ảnh Base64.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaSP", "String", "Unique, Tự sinh (SPxxx)", "Mã định danh sản phẩm"],
            ["TenSP", "String", "Bắt buộc", "Tên thương mại sản phẩm"],
            ["MaLoai", "String / ObjectId", "Tham chiếu LoaiHang", "Mã nhóm ngành hàng liên kết"],
            ["DonViTinh", "String", "Bắt buộc", "Đơn vị tính: Hộp, Gói, Cái, Bộ, Lon, Thùng..."],
            ["GiaNhap", "Number", "> 0, Bắt buộc", "Giá vốn mua vào từ NCC"],
            ["GiaBan", "Number", "> 0, Bắt buộc", "Giá bán lẻ niêm yết tại quầy"],
            ["HanSuDung", "String", "YYYY-MM-DD, Bắt buộc", "Hạn sử dụng của lô hàng (hệ thống quét cận date <60 ngày)"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái kinh doanh: 'Đang bán', 'Ngừng bán'"],
            ["stock", "Number", "Mặc định: 0", "Số lượng tồn kho khả dụng hiện tại"],
            ["SoLuongToiThieu", "Number", "Mặc định: 10", "Định mức tồn tối thiểu để phát cảnh báo tồn thấp"],
            ["HinhAnh", "String", "Base64 Data URL", "Chuỗi ảnh nén Canvas trực tiếp từ trình duyệt"],
            ["createdAt", "Date", "Tự động", "Thời điểm khởi tạo sản phẩm"]
        ]
    },
    # Nhóm 3: Mua hàng & Nhập kho
    {
        "group": "Nhóm 3 - Nghiệp vụ Mua hàng",
        "num": "3.2.8",
        "name": "DonDatHang",
        "desc": "Đơn đặt hàng mua (PO) gửi nhà cung cấp theo dõi tiến độ giao hàng và điều khoản thanh toán.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaDDH", "String", "Unique, Tự sinh (DDHxxx)", "Mã đơn đặt hàng mua"],
            ["MaNCC", "String / ObjectId", "Tham chiếu NhaCungCap", "Nhà cung cấp được chỉ định"],
            ["MaNV", "String / ObjectId", "Tham chiếu NhanVien", "Nhân viên mua hàng tạo đơn"],
            ["NgayDat", "String", "YYYY-MM-DD", "Ngày gửi đơn đặt mua"],
            ["TongTien", "Number", ">= 0", "Tổng giá trị đơn đặt hàng"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Chờ duyệt', 'Đang giao', 'Hoàn thành', 'Đã hủy'"],
            ["NguoiLap", "String", "Bắt buộc", "Họ tên nhân viên lập đơn"],
            ["GhiChu", "String", "Tùy chọn", "Điều khoản thỏa thuận giao nhận"],
            ["details", "Array", "Mảng nhúng", "Danh sách mặt hàng đặt mua (đồng bộ sang CT_DonDatHang)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.9",
        "name": "CT_DonDatHang",
        "desc": "Bảng chi tiết các mặt hàng trong đơn đặt mua phục vụ truy vấn phân tích mua hàng.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaDDH", "String / ObjectId", "Tham chiếu DonDatHang", "Mã đơn đặt hàng mua cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Sản phẩm đặt mua"],
            ["SoLuong", "Number", "Nguyên dương", "Số lượng đặt mua"],
            ["DonGia", "Number", ">= 0", "Đơn giá mua thỏa thuận"],
            ["ThanhTien", "Number", ">= 0", "Thành tiền dòng = Số lượng * Đơn giá"],
            ["createdAt", "Date", "Tự động", "Thời điểm tạo bản ghi"]
        ]
    },
    # Nhóm 4: Bán hàng & Hóa đơn
    {
        "group": "Nhóm 4 - Nghiệp vụ Bán hàng & Hóa đơn",
        "num": "3.2.10",
        "name": "DonHang",
        "desc": "Đơn hàng bán lẻ phát sinh tại quầy thu ngân POS, ghi nhận chiết khấu voucher và doanh thu.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaDH", "String", "Unique, Tự sinh (DHxxx)", "Mã đơn bán hàng tại quầy POS"],
            ["MaKH", "String / ObjectId", "Tham chiếu KhachHang", "Khách hàng mua (hoặc khách lẻ)"],
            ["MaNV", "String / ObjectId", "Tham chiếu NhanVien", "Nhân viên thu ngân lập đơn"],
            ["NgayDat", "String", "YYYY-MM-DD", "Thời điểm giao dịch bán hàng"],
            ["TongTien", "Number", ">= 0", "Tổng tiền hàng trước chiết khấu"],
            ["TienGiam", "Number", ">= 0", "Số tiền giảm trừ khuyến mãi / voucher"],
            ["ThanhTien", "Number", ">= 0", "Số tiền thực thu = TongTien - TienGiam"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái đơn: 'Hoàn thành', 'Đã hủy'"],
            ["details", "Array", "Mảng nhúng", "Chi tiết mặt hàng bán lẻ (đồng bộ sang CT_DonHang)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.11",
        "name": "CT_DonHang",
        "desc": "Chi tiết từng dòng sản phẩm bán lẻ trên đơn hàng POS.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaDH", "String / ObjectId", "Tham chiếu DonHang", "Mã đơn bán hàng cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Hàng hóa xuất bán"],
            ["SoLuong", "Number", "Nguyên dương", "Số lượng bán"],
            ["DonGia", "Number", ">= 0", "Đơn giá bán lẻ niêm yết"],
            ["ThanhTien", "Number", ">= 0", "Thành tiền dòng = Số lượng * Đơn giá"],
            ["createdAt", "Date", "Tự động", "Ngày tạo chi tiết đơn"]
        ]
    },
    {
        "group": None,
        "num": "3.2.12",
        "name": "HoaDon",
        "desc": "Hóa đơn bán lẻ kiêm chứng từ giao nhận và theo dõi nợ khách hàng (chặn xóa vật lý).",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaHD", "String", "Unique, Tự sinh (HDxxx)", "Mã hóa đơn bán hàng"],
            ["MaDH", "String / ObjectId", "Tham chiếu DonHang", "Đơn bán hàng liên kết"],
            ["MaKH", "String / ObjectId", "Tham chiếu KhachHang", "Khách hàng mua hàng"],
            ["TenKH", "String", "Tùy chọn", "Họ tên khách hàng lưu trên chứng từ"],
            ["MaKHCode", "String", "Tùy chọn", "Mã khách hàng hiển thị (KHxxx)"],
            ["NgayLap", "String", "YYYY-MM-DD", "Ngày lập hóa đơn"],
            ["TongTien", "Number", ">= 0", "Tổng giá trị thanh toán hóa đơn"],
            ["SoTienDaTra", "Number", "Mặc định: 0", "Số tiền khách đã thanh toán"],
            ["ConNo", "Number", "Mặc định: 0", "Số tiền khách còn nợ lại"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đã thanh toán', 'Chưa thanh toán', 'Thanh toán 1 phần', 'Đã hủy'"],
            ["details", "Array", "Mảng nhúng", "Chi tiết dòng hóa đơn (đồng bộ sang CT_HoaDon)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.13",
        "name": "CT_HoaDon",
        "desc": "Chi tiết dòng sản phẩm trên hóa đơn bán hàng phục vụ đối soát doanh thu.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaHD", "String / ObjectId", "Tham chiếu HoaDon", "Mã hóa đơn bán cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Mặt hàng xuất bán"],
            ["SoLuong", "Number", "Nguyên dương", "Số lượng xuất bán"],
            ["DonGia", "Number", ">= 0", "Đơn giá thanh toán"],
            ["ThanhTien", "Number", ">= 0", "Thành tiền dòng mặt hàng"],
            ["createdAt", "Date", "Tự động", "Ngày tạo dòng hóa đơn"]
        ]
    },
    # Nhóm 5: Kho vận, Kiểm kê & Đổi trả
    {
        "group": "Nhóm 5 - Kho vận, Kiểm kê & Đổi trả",
        "num": "3.2.14",
        "name": "PhieuNhap",
        "desc": "Phiếu nhập kho hàng hóa (Mẫu 01-VT), tự động tăng tồn kho và ghi nợ nhà cung cấp.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaPN", "String", "Unique, Tự sinh (PNxxx)", "Mã phiếu nhập kho (Mẫu 01-VT)"],
            ["MaDDH", "String / ObjectId", "Tham chiếu DonDatHang", "Đơn đặt hàng mua liên kết (nếu có)"],
            ["MaNCC", "String / ObjectId", "Tham chiếu NhaCungCap", "Nhà cung cấp giao hàng"],
            ["MaNV", "String / ObjectId", "Tham chiếu NhanVien", "Thủ kho tiếp nhận hàng"],
            ["NgayNhap", "String", "YYYY-MM-DD", "Ngày thực tế hàng về nhập kho"],
            ["TongTien", "Number", ">= 0", "Tổng giá trị vốn hàng nhập kho"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đã lưu', 'Hoàn thành', 'Đã hủy'"],
            ["NguoiLap", "String", "Bắt buộc", "Thủ kho lập phiếu nhập"],
            ["details", "Array", "Mảng nhúng", "Danh sách mặt hàng thực nhập (đồng bộ sang CT_PhieuNhap)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.15",
        "name": "CT_PhieuNhap",
        "desc": "Chi tiết từng mặt hàng nhập kho phục vụ thẻ kho và tính giá vốn bình quân.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaPN", "String / ObjectId", "Tham chiếu PhieuNhap", "Mã phiếu nhập kho cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Sản phẩm thực tế nhập kho"],
            ["SoLuong", "Number", "Nguyên dương", "Số lượng nhập kho"],
            ["DonGia", "Number", ">= 0", "Đơn giá vốn nhập kho"],
            ["ThanhTien", "Number", ">= 0", "Thành tiền = Số lượng * Đơn giá"],
            ["createdAt", "Date", "Tự động", "Ngày tạo dòng nhập kho"]
        ]
    },
    {
        "group": None,
        "num": "3.2.16",
        "name": "PhieuXuat",
        "desc": "Phiếu xuất kho hàng hóa (Mẫu 02-VT), ghi nhận xuất kho bán lẻ hoặc xuất trả hàng.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaPX", "String", "Unique, Tự sinh (PXxxx)", "Mã phiếu xuất kho (Mẫu 02-VT)"],
            ["MaDH", "String / ObjectId", "Tham chiếu DonHang", "Đơn bán lẻ phát sinh xuất hàng"],
            ["MaNV", "String / ObjectId", "Tham chiếu NhanVien", "Thủ kho thực hiện xuất kho"],
            ["NgayXuat", "String", "YYYY-MM-DD", "Ngày thực tế xuất kho"],
            ["TongTien", "Number", ">= 0", "Tổng giá trị xuất kho"],
            ["LyDo", "String", "Tùy chọn", "Lý do xuất kho (Xuất bán lẻ, xuất trả hàng...)"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Hoàn thành', 'Đã hủy'"],
            ["details", "Array", "Mảng nhúng", "Chi tiết hàng xuất kho (đồng bộ sang CT_PhieuXuat)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.17",
        "name": "CT_PhieuXuat",
        "desc": "Chi tiết dòng hàng xuất kho phục vụ sổ theo dõi xuất vật tư.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaPX", "String / ObjectId", "Tham chiếu PhieuXuat", "Mã phiếu xuất kho cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Hàng hóa xuất kho"],
            ["SoLuong", "Number", "Nguyên dương", "Số lượng xuất kho"],
            ["DonGia", "Number", ">= 0", "Đơn giá xuất kho"],
            ["ThanhTien", "Number", ">= 0", "Thành tiền dòng xuất"],
            ["createdAt", "Date", "Tự động", "Ngày tạo dòng xuất"]
        ]
    },
    {
        "group": None,
        "num": "3.2.18",
        "name": "TonKho",
        "desc": "Quản lý số lượng tồn kho khả dụng thời gian thực cho từng mặt hàng (quan hệ 1-1 với SanPham).",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaSP", "ObjectId", "Unique, Tham chiếu SanPham", "Mã định danh sản phẩm được theo dõi"],
            ["SoLuongTon", "Number", ">= 0", "Số lượng tồn kho khả dụng thời gian thực"],
            ["SoLuong", "Number", ">= 0", "Trường đồng bộ số lượng tồn kho"],
            ["NgayCapNhat", "String", "YYYY-MM-DD", "Ngày cập nhật biến động gần nhất"],
            ["updatedAt", "Date", "Tự động", "Thời điểm phát sinh biến động tồn"]
        ]
    },
    {
        "group": None,
        "num": "3.2.19",
        "name": "KiemKe",
        "desc": "Phiếu kiểm kê kho hàng định kỳ, phát hiện sai lệch thừa/thiếu giữa sổ sách và thực tế.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaKK", "String", "Unique, Tự sinh (KKxxx)", "Mã đợt kiểm kê hàng hóa"],
            ["NgayKiemKe", "String", "YYYY-MM-DD", "Ngày thực hiện đếm kiểm kê thực tế"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đang kiểm kê', 'Đã điều chỉnh', 'Chờ điều chỉnh', 'Khớp hoàn toàn'"],
            ["GhiChu", "String", "Tùy chọn", "Mục đích kiểm kê định kỳ / đột xuất"],
            ["NguoiKiemKe", "String", "Bắt buộc", "Họ tên thủ kho thực hiện đếm"],
            ["NguoiDieuChinh", "String", "Tùy chọn", "Người bấm xác nhận cân bằng kho"],
            ["NgayDieuChinh", "String", "Tùy chọn", "Ngày thực hiện cân bằng kho"],
            ["details", "Array", "Mảng nhúng", "Chi tiết mặt hàng kiểm kê (đồng bộ sang CT_KiemKe)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.20",
        "name": "CT_KiemKe",
        "desc": "Chi tiết chênh lệch tồn sổ sách so với tồn thực tế cho từng mặt hàng kiểm kê.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaKK", "String / ObjectId", "Tham chiếu KiemKe", "Mã phiếu kiểm kê cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Sản phẩm được kiểm đếm"],
            ["SoLuongHeThong", "Number", ">= 0", "Số lượng tồn theo sổ sách kế toán"],
            ["SoLuongThucTe", "Number", ">= 0", "Số lượng thực đếm tại quầy kệ / kho"],
            ["ChenhLech", "Number", "Số thực", "Chênh lệch = ThucTe - HeThong (dương: thừa, âm: thiếu)"],
            ["LyDo", "String", "Tùy chọn", "Giải trình nguyên nhân thừa / thiếu"],
            ["createdAt", "Date", "Tự động", "Ngày ghi nhận chi tiết"]
        ]
    },
    {
        "group": None,
        "num": "3.2.21",
        "name": "DieuChinhKho",
        "desc": "Chứng từ điều chỉnh cân bằng kho sau kiểm kê hoặc điều chỉnh kho lẻ (Thủ kho tự bấm được).",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaDC", "String", "Unique, Tự sinh (DCxxx)", "Mã phiếu điều chỉnh cân bằng kho"],
            ["MaKK", "String / ObjectId", "Tham chiếu KiemKe", "Phiếu kiểm kê làm căn cứ điều chỉnh"],
            ["NgayDieuChinh", "String", "YYYY-MM-DD", "Ngày thực hiện cân bằng hệ thống"],
            ["NguoiThucHien", "String", "Bắt buộc", "Thủ kho / Quản lý bấm điều chỉnh kho"],
            ["LyDo", "String", "Bắt buộc", "Căn cứ pháp lý và nguyên nhân điều chỉnh"],
            ["details", "Array", "Mảng nhúng", "Danh sách mặt hàng được cập nhật lại số tồn"],
            ["createdAt", "Date", "Tự động", "Thời điểm ghi nhận chứng từ điều chỉnh"]
        ]
    },
    {
        "group": None,
        "num": "3.2.22",
        "name": "PhieuTraHang",
        "desc": "Phiếu tiếp nhận hàng khách trả lại, tự động nhập tăng lại số lượng tồn kho và hoàn tiền.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaPTH", "String", "Unique, Tự sinh (PTHxxx)", "Mã phiếu tiếp nhận hàng đổi trả"],
            ["MaDH", "String / ObjectId", "Tham chiếu DonHang", "Đơn mua hàng gốc của khách"],
            ["MaHD", "String / ObjectId", "Tham chiếu HoaDon", "Hóa đơn bán lẻ liên kết"],
            ["MaKH", "String / ObjectId", "Tham chiếu KhachHang", "Khách hàng yêu cầu đổi trả"],
            ["MaNV", "String / ObjectId", "Tham chiếu NhanVien", "Nhân viên tiếp nhận xử lý"],
            ["NguoiLap", "String", "Bắt buộc", "Họ tên nhân viên tiếp nhận"],
            ["NgayTra", "String", "YYYY-MM-DD", "Ngày tiếp nhận sản phẩm trả lại"],
            ["LyDo", "String", "Bắt buộc", "Lý do trả hàng (Hết hạn, lỗi bao bì...)"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đã xử lý', 'Đã hoàn tiền', 'Đã hủy'"],
            ["SoLuong", "Number", "Tổng số lượng", "Tổng số lượng hàng nhập lại kho"],
            ["details", "Array", "Mảng nhúng", "Chi tiết các mặt hàng trả lại (đồng bộ sang CT_PhieuTraHang)"]
        ]
    },
    {
        "group": None,
        "num": "3.2.23",
        "name": "CT_PhieuTraHang",
        "desc": "Chi tiết dòng hàng khách trả lại nhập về kho hàng.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaPTH", "String / ObjectId", "Tham chiếu PhieuTraHang", "Mã phiếu trả hàng cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Sản phẩm được hoàn trả"],
            ["SoLuong", "Number", "Nguyên dương", "Số lượng hàng nhập lại kho"],
            ["DonGia", "Number", ">= 0", "Đơn giá hoàn tiền cho khách"],
            ["ThanhTien", "Number", ">= 0", "Tổng tiền hoàn trả dòng mặt hàng"],
            ["createdAt", "Date", "Tự động", "Ngày tạo dòng trả hàng"]
        ]
    },
    # Nhóm 6: Thu chi tiền tệ & Công nợ
    {
        "group": "Nhóm 6 - Thu chi tiền tệ & Công nợ",
        "num": "3.2.24",
        "name": "PhieuThu",
        "desc": "Phiếu thu tiền mặt theo Mẫu số 01-TT ban hành theo chế độ kế toán doanh nghiệp.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaPT", "String", "Unique, Tự sinh (PTxxx)", "Số hiệu phiếu thu tiền mặt (Mẫu 01-TT)"],
            ["NgayLap", "String", "YYYY-MM-DD", "Ngày lập chứng từ thu quỹ"],
            ["NguoiNopTien", "String", "Bắt buộc", "Họ tên người nộp tiền (khách hàng, nhân viên)"],
            ["DiaChi", "String", "Tùy chọn", "Địa chỉ người nộp tiền"],
            ["LyDo", "String", "Bắt buộc", "Nội dung thu tiền mặt nhập quỹ"],
            ["SoTien", "Number", "> 0, Bắt buộc", "Số tiền thực thu nhập quỹ"],
            ["ChungTuGoc", "String", "Tham chiếu chuỗi", "Mã chứng từ gốc đính kèm (HD001, CN002...)"],
            ["KemTheo", "String", "Tùy chọn", "Số lượng chứng từ đính kèm"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đã lập', 'Đã xác nhận', 'Đã hủy'"],
            ["NguoiLap", "String", "Bắt buộc", "Kế toán / Thủ quỹ lập phiếu"]
        ]
    },
    {
        "group": None,
        "num": "3.2.25",
        "name": "PhieuChi",
        "desc": "Phiếu chi tiền mặt theo Mẫu số 02-TT ban hành theo chế độ kế toán doanh nghiệp.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaPC", "String", "Unique, Tự sinh (PCxxx)", "Số hiệu phiếu chi tiền mặt (Mẫu 02-TT)"],
            ["NgayLap", "String", "YYYY-MM-DD", "Ngày lập chứng từ chi quỹ"],
            ["NguoiNhanTien", "String", "Bắt buộc", "Họ tên người nhận tiền / Nhà cung cấp"],
            ["DiaChi", "String", "Tùy chọn", "Địa chỉ người nhận tiền"],
            ["LyDo", "String", "Bắt buộc", "Nội dung chi tiền mặt xuất quỹ (Trả nợ NCC, Vận chuyển...)"],
            ["SoTien", "Number", "> 0, Bắt buộc", "Số tiền thực chi xuất quỹ"],
            ["ChungTuGoc", "String", "Tham chiếu chuỗi", "Mã chứng từ gốc đính kèm (PN001, Hóa đơn...)"],
            ["KemTheo", "String", "Tùy chọn", "Số lượng chứng từ đính kèm"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đã lập', 'Đã xác nhận', 'Đã hủy'"],
            ["NguoiLap", "String", "Bắt buộc", "Kế toán / Thủ quỹ duyệt xuất quỹ"]
        ]
    },
    {
        "group": None,
        "num": "3.2.26",
        "name": "ThanhToan",
        "desc": "Nhật ký các đợt thanh toán của hóa đơn bán lẻ (tiền mặt, chuyển khoản, VietQR).",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaTT", "String", "Unique, Tự sinh (TTxxx)", "Mã định danh giao dịch thanh toán"],
            ["MaHD", "String / ObjectId", "Tham chiếu HoaDon", "Hóa đơn được thanh toán"],
            ["SoTien", "Number", "> 0, Bắt buộc", "Số tiền thanh toán của giao dịch"],
            ["PhuongThuc", "String", "Bắt buộc", "Hình thức: 'Tiền mặt', 'Chuyển khoản', 'VietQR'"],
            ["NgayThanhToan", "String", "YYYY-MM-DD", "Thời điểm giao dịch thanh toán"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái giao dịch: 'Thành công', 'Đã hủy'"],
            ["createdAt", "Date", "Tự động", "Thời điểm hệ thống ghi nhận giao dịch"]
        ]
    },
    {
        "group": None,
        "num": "3.2.27",
        "name": "CongNo",
        "desc": "Sổ theo dõi công nợ chi tiết hai chiều (phải trả nhà cung cấp theo phiếu nhập và phải thu khách hàng theo hóa đơn).",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaCN", "String", "Unique, Tự sinh (CNxxx)", "Mã bản ghi sổ công nợ"],
            ["MaPN", "String / ObjectId", "Tham chiếu PhieuNhap", "Phiếu nhập kho phát sinh nợ (nếu nợ NCC)"],
            ["MaNCC", "String / ObjectId", "Tham chiếu NhaCungCap", "Nhà cung cấp chủ nợ"],
            ["TenNCC", "String", "Tùy chọn", "Tên nhà cung cấp"],
            ["MaHD", "String / ObjectId", "Tham chiếu HoaDon", "Hóa đơn phát sinh nợ (nếu nợ khách hàng)"],
            ["MaKH", "String / ObjectId", "Tham chiếu KhachHang", "Khách hàng nợ tiền hàng"],
            ["LoaiCongNo", "String", "Bắt buộc", "Phân loại: 'Nhà cung cấp' (phải trả) hoặc 'Khách hàng' (phải thu)"],
            ["SoTien", "Number", ">= 0", "Tổng số tiền nợ gốc phát sinh"],
            ["SoTienDaTra", "Number", "Mặc định: 0", "Số tiền đã trả tích lũy"],
            ["SoTienConLai", "Number", ">= 0", "Số dư nợ hiện tại = SoTien - SoTienDaTra"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Còn nợ', 'Đã thanh toán', 'Quá hạn'"]
        ]
    },
    # Nhóm 7: Khuyến mãi & Hệ thống
    {
        "group": "Nhóm 7 - Khuyến mãi & Hệ thống",
        "num": "3.2.28",
        "name": "KhuyenMai",
        "desc": "Chương trình khuyến mãi, voucher giảm giá và chính sách ưu đãi thành viên.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["MaKM", "String", "Unique (BAC50K...)", "Mã định danh chương trình / voucher"],
            ["TenKM", "String", "Bắt buộc", "Tên hiển thị chương trình ưu đãi"],
            ["LoaiKM", "String", "Bắt buộc", "Hình thức giảm: 'Số tiền' hoặc 'Phần trăm'"],
            ["GiaTriGiam", "Number", ">= 0", "Số tiền giảm trực tiếp (50.000đ, 100.000đ...)"],
            ["PhanTramGiam", "Number", "0 - 100", "Tỷ lệ giảm giá (%)"],
            ["DonHangToiThieu", "Number", "Mặc định: 0", "Giá trị đơn tối thiểu để áp dụng"],
            ["NgayBatDau", "String", "YYYY-MM-DD", "Ngày bắt đầu áp dụng ưu đãi"],
            ["NgayKetThuc", "String", "YYYY-MM-DD", "Ngày kết thúc chương trình"],
            ["TrangThai", "String", "Bắt buộc", "Trạng thái: 'Đang áp dụng', 'Đã kết thúc', 'Chưa kích hoạt'"]
        ]
    },
    {
        "group": None,
        "num": "3.2.29",
        "name": "CT_KhuyenMai",
        "desc": "Danh sách mặt hàng áp dụng chương trình khuyến mãi tương ứng.",
        "fields": [
            ["_id", "ObjectId / String", "PK", "Khóa chính chi tiết dòng"],
            ["MaKM", "String / ObjectId", "Tham chiếu KhuyenMai", "Mã chương trình khuyến mãi cha"],
            ["MaSP", "String / ObjectId", "Tham chiếu SanPham", "Sản phẩm được áp dụng chiết khấu"],
            ["createdAt", "Date", "Tự động", "Ngày thêm sản phẩm vào danh mục ưu đãi"]
        ]
    },
    {
        "group": None,
        "num": "3.2.30",
        "name": "Counters",
        "desc": "Bộ đếm tự tăng quản lý cơ chế sinh mã chứng từ nghiệp vụ duy nhất (atomic $inc).",
        "fields": [
            ["_id", "String", "PK (HD, SP, KH...)", "Tiền tố ký hiệu của từng phân hệ nghiệp vụ"],
            ["seq", "Number", "Số nguyên tự tăng", "Giá trị số thứ tự tăng dần đảm bảo mã không trùng lặp"]
        ]
    },
    {
        "group": None,
        "num": "3.2.31",
        "name": "AuditLogs",
        "desc": "Nhật ký kiểm toán hệ thống (append-only, chặn xóa tuyệt đối) ghi nhận mọi thao tác nhạy cảm.",
        "fields": [
            ["_id", "ObjectId", "PK", "Khóa chính tự sinh"],
            ["timestamp", "Date", "Tự động, Index", "Thời điểm chính xác phát sinh thao tác"],
            ["userId", "String", "Tham chiếu Users", "Mã tài khoản người dùng thực hiện"],
            ["username", "String", "Tên tài khoản", "Tên đăng nhập của người thao tác"],
            ["role", "String", "Vai trò", "Vai trò của người dùng tại thời điểm thao tác"],
            ["action", "String", "Bắt buộc", "Hành động: LOGIN, CREATE, UPDATE, DELETE, BACKUP, RESTORE"],
            ["module", "String", "Bắt buộc", "Phân hệ bị tác động (products, invoices, accounts...)"],
            ["entity", "String", "Bắt buộc", "Tên bảng CSDL bị thay đổi"],
            ["entityId", "String", "Tùy chọn", "Khóa chính của bản ghi bị thay đổi"],
            ["description", "String", "Bắt buộc", "Mô tả chi tiết nội dung thao tác nghiệp vụ"],
            ["metadata", "Object", "Tùy chọn", "Dữ liệu payload trước và sau thay đổi"],
            ["ip", "String", "Tùy chọn", "Địa chỉ IP máy trạm phát sinh yêu cầu"]
        ]
    }
]

print(f"Loaded {len(COLLECTIONS_DATA)} collections definitions.")
