import fs from 'fs';
import zlib from 'zlib';

const code = `erDiagram
    Users {
        ObjectId id PK
        string username "Unique"
        string passwordHash
        string fullName
        string role
        string status
    }
    VaiTro {
        ObjectId id PK
        int MaVaiTro "Unique"
        string TenVaiTro
        string MaKey "Unique"
        boolean LaVaiTroHeThong
    }
    NhanVien {
        ObjectId id PK
        string MaNV "Unique"
        string HoTen
        string ChucVu
        string username FK
        int MaVaiTro FK
    }
    KhachHang {
        ObjectId id PK
        string MaKH "Unique"
        string HoTen
        string SDT "Unique"
        int DiemTichLuy
        string CapThanhVien
    }
    NhaCungCap {
        ObjectId id PK
        string MaNCC "Unique"
        string TenNCC
        string SDT
        string DiaChi
    }
    LoaiHang {
        ObjectId id PK
        string MaLoai "Unique"
        string TenLoai
    }
    SanPham {
        ObjectId id PK
        string MaSP "Unique"
        string TenSP
        string MaLoai FK
        decimal GiaNhap
        decimal GiaBan
        date HanSuDung
        int stock
    }
    TonKho {
        ObjectId id PK
        ObjectId MaSP FK
        int SoLuongTon
    }
    DonDatHang {
        ObjectId id PK
        string MaDDH "Unique"
        string MaNCC FK
        string MaNV FK
        decimal TongTien
        string TrangThai
    }
    CT_DonDatHang {
        ObjectId id PK
        string MaDDH FK
        string MaSP FK
        int SoLuong
        decimal DonGia
        decimal ThanhTien
    }
    PhieuNhap {
        ObjectId id PK
        string MaPN "Unique"
        string MaDDH FK
        string MaNCC FK
        string MaNV FK
        decimal TongTien
        string TrangThai
    }
    CT_PhieuNhap {
        ObjectId id PK
        string MaPN FK
        string MaSP FK
        int SoLuong
        decimal DonGia
        decimal ThanhTien
    }
    DonHang {
        ObjectId id PK
        string MaDH "Unique"
        string MaKH FK
        string MaNV FK
        decimal TongTien
        decimal ThanhTien
        string TrangThai
    }
    CT_DonHang {
        ObjectId id PK
        string MaDH FK
        string MaSP FK
        int SoLuong
        decimal DonGia
        decimal ThanhTien
    }
    HoaDon {
        ObjectId id PK
        string MaHD "Unique"
        string MaDH FK
        string MaKH FK
        decimal TongTien
        decimal SoTienDaTra
        decimal ConNo
        string TrangThai
    }
    CT_HoaDon {
        ObjectId id PK
        string MaHD FK
        string MaSP FK
        int SoLuong
        decimal DonGia
        decimal ThanhTien
    }
    PhieuXuat {
        ObjectId id PK
        string MaPX "Unique"
        string MaDH FK
        string MaNV FK
        decimal TongTien
        string TrangThai
    }
    CT_PhieuXuat {
        ObjectId id PK
        string MaPX FK
        string MaSP FK
        int SoLuong
        decimal ThanhTien
    }
    PhieuThu {
        ObjectId id PK
        string MaPT "Unique"
        string NguoiNopTien
        decimal SoTien
        string ChungTuGoc FK
        string TrangThai
    }
    PhieuChi {
        ObjectId id PK
        string MaPC "Unique"
        string NguoiNhanTien
        decimal SoTien
        string ChungTuGoc FK
        string TrangThai
    }
    ThanhToan {
        ObjectId id PK
        string MaTT "Unique"
        string MaHD FK
        decimal SoTien
        string PhuongThuc
        string TrangThai
    }
    CongNo {
        ObjectId id PK
        string MaCN "Unique"
        string MaPN FK
        string MaNCC FK
        string MaHD FK
        string MaKH FK
        string LoaiCongNo
        decimal SoTien
        decimal SoTienConLai
    }
    KiemKe {
        ObjectId id PK
        string MaKK "Unique"
        date NgayKiemKe
        string NguoiKiemKe
        string TrangThai
    }
    CT_KiemKe {
        ObjectId id PK
        string MaKK FK
        string MaSP FK
        int SoLuongHeThong
        int SoLuongThucTe
        int ChenhLech
    }
    DieuChinhKho {
        ObjectId id PK
        string MaDC "Unique"
        string MaKK FK
        string NguoiThucHien
        string LyDo
    }
    PhieuTraHang {
        ObjectId id PK
        string MaPTH "Unique"
        string MaDH FK
        string MaHD FK
        string MaKH FK
        string TrangThai
    }
    CT_PhieuTraHang {
        ObjectId id PK
        string MaPTH FK
        string MaSP FK
        int SoLuong
        decimal ThanhTien
    }
    KhuyenMai {
        ObjectId id PK
        string MaKM "Unique"
        string TenKM
        string LoaiKM
        decimal GiaTriGiam
    }
    CT_KhuyenMai {
        ObjectId id PK
        string MaKM FK
        string MaSP FK
    }
    Counters {
        string id PK
        int seq
    }
    AuditLogs {
        ObjectId id PK
        date timestamp
        string userId FK
        string action
        string module
        string entity
    }

    Users ||--o{ AuditLogs : "thuc_hien"
    Users ||--o| NhanVien : "lien_ket"
    VaiTro ||--o{ NhanVien : "phan_quyen"

    LoaiHang ||--o{ SanPham : "phan_loai"
    SanPham ||--|| TonKho : "quan_ly_ton"

    NhaCungCap ||--o{ DonDatHang : "cung_cap"
    NhanVien ||--o{ DonDatHang : "lap_don"
    DonDatHang ||--|{ CT_DonDatHang : "gom"
    SanPham ||--o{ CT_DonDatHang : "san_pham"

    DonDatHang ||--o{ PhieuNhap : "ke_thua"
    NhaCungCap ||--o{ PhieuNhap : "giao_hang"
    NhanVien ||--o{ PhieuNhap : "nhap_kho"
    PhieuNhap ||--|{ CT_PhieuNhap : "gom"
    SanPham ||--o{ CT_PhieuNhap : "san_pham"

    KhachHang ||--o{ DonHang : "mua_hang"
    NhanVien ||--o{ DonHang : "ban_hang"
    DonHang ||--|{ CT_DonHang : "gom"
    SanPham ||--o{ CT_DonHang : "san_pham"

    DonHang ||--|| HoaDon : "xuat_hd"
    KhachHang ||--o{ HoaDon : "khach_hang"
    HoaDon ||--|{ CT_HoaDon : "gom"
    SanPham ||--o{ CT_HoaDon : "san_pham"

    DonHang ||--o| PhieuXuat : "xuat_kho"
    NhanVien ||--o{ PhieuXuat : "lap_phieu"
    PhieuXuat ||--|{ CT_PhieuXuat : "gom"
    SanPham ||--o{ CT_PhieuXuat : "san_pham"

    NhanVien ||--o{ KiemKe : "kiem_ke"
    KiemKe ||--|{ CT_KiemKe : "gom"
    SanPham ||--o{ CT_KiemKe : "san_pham"
    KiemKe ||--o| DieuChinhKho : "can_bang"

    DonHang ||--o{ PhieuTraHang : "doi_tra"
    KhachHang ||--o{ PhieuTraHang : "tra_hang"
    NhanVien ||--o{ PhieuTraHang : "tiep_nhan"
    PhieuTraHang ||--|{ CT_PhieuTraHang : "gom"
    SanPham ||--o{ CT_PhieuTraHang : "san_pham"

    HoaDon ||--o{ ThanhToan : "thanh_toan"
    PhieuNhap ||--o| CongNo : "no_ncc"
    NhaCungCap ||--o{ CongNo : "chu_no"
    HoaDon ||--o| CongNo : "no_kh"
    KhachHang ||--o{ CongNo : "khach_no"
    HoaDon ||--o{ PhieuThu : "thu_tien"
    PhieuNhap ||--o{ PhieuChi : "chi_tien"

    KhuyenMai ||--|{ CT_KhuyenMai : "gom"
    SanPham ||--o{ CT_KhuyenMai : "san_pham"
`;

const deflated = zlib.deflateSync(Buffer.from(code, 'utf8'), { level: 9 });
const b64 = deflated.toString('base64').replace(/\+/g, '-').replace(/\//g, '_');

async function run() {
  for (const ext of ['svg', 'png']) {
    const url = 'https://kroki.io/mermaid/' + ext + '/' + b64;
    console.log('Fetching ' + ext + '...');
    const res = await fetch(url);
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(res.status + ' ' + res.statusText + ': ' + errText);
    }
    const buf = Buffer.from(await res.arrayBuffer());
    
    // Lưu vào thư mục gốc project
    fs.writeFileSync('D:/BabyShop/so_do_erd_31_bang.' + ext, buf);
    // Lưu vào thư mục database/
    fs.writeFileSync('D:/BabyShop/database/so_do_erd_31_bang.' + ext, buf);
    console.log('✅ Đã lưu thành công D:/BabyShop/so_do_erd_31_bang.' + ext + ' (' + buf.byteLength + ' bytes)');
  }
}

run().catch(e => {
  console.error('Lỗi tải từ Kroki:', e);
  process.exit(1);
});
