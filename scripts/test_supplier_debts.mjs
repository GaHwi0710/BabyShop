import assert from "assert";
import { MongoClient } from "../backend/node_modules/mongodb/lib/index.js";
import dotenv from "../backend/node_modules/dotenv/lib/main.js";
import { buildDebtsHtml } from "../frontend/src/lib/reportPrint.js";

dotenv.config({ path: "./backend/.env" });

console.log("==================================================");
console.log("TESTING CÔNG NỢ NHÀ CUNG CẤP & BẢN IN");
console.log("==================================================");

// Mock suppliers list
const mockSuppliers = [
  { id: "supp-1", MaNCC: "NCC001", TenNCC: "Công ty TNHH Pigeon Việt Nam", SDT: "028 3823 1234" },
  { id: "supp-2", MaNCC: "NCC002", TenNCC: "Nhà phân phối Xe Đạp", SDT: "090 123 4567" },
  { id: "supp-3", MaNCC: "NCC003", TenNCC: "Nhà phân phối Bỉm Sạch", SDT: "091 999 8888" },
  { id: "supp-4", MaNCC: "NCC004", TenNCC: "Công ty Sữa Meiji", SDT: "024 3999 7777" },
];

// Test Case 1: Có nhà cung cấp còn nợ (Chưa thanh toán)
const debtUnpaid = {
  id: "cn-1",
  MaCN: "CN-NCC-001",
  MaNCC: "supp-1",
  MaNCCCode: "NCC001",
  TenNCC: "Công ty TNHH Pigeon Việt Nam",
  LoaiCongNo: "Nhà cung cấp",
  MaPhieuNhap: "PN001",
  NgayPhatSinh: "2026-09-01",
  SoTien: 10000000,
  SoTienDaTra: 0,
  SoTienConLai: 10000000,
  TrangThai: "Còn nợ",
};

// Test Case 2: Nhà cung cấp đã thanh toán một phần
const debtPartial = {
  id: "cn-2",
  MaCN: "CN-NCC-002",
  MaNCC: "supp-2",
  MaNCCCode: "NCC002",
  TenNCC: "Nhà phân phối Xe Đạp",
  LoaiCongNo: "Nhà cung cấp",
  MaPhieuNhap: "PN002",
  NgayPhatSinh: "2026-09-05",
  SoTien: 5000000,
  SoTienDaTra: 2000000,
  SoTienConLai: 3000000,
  TrangThai: "Còn nợ",
};

// Test Case 3: Nhà cung cấp đã thanh toán hết
const debtPaid = {
  id: "cn-3",
  MaCN: "CN-NCC-003",
  MaNCC: "supp-3",
  MaNCCCode: "NCC003",
  TenNCC: "Nhà phân phối Bỉm Sạch",
  LoaiCongNo: "Nhà cung cấp",
  MaPhieuNhap: "PN003",
  NgayPhatSinh: "2026-09-10",
  SoTien: 4000000,
  SoTienDaTra: 4000000,
  SoTienConLai: 0,
  TrangThai: "Đã thanh toán",
};

// Mixed list including CUSTOMER debts that must NOT be printed!
const customerDebt1 = {
  id: "cn-cust-1",
  MaCN: "CN-KH-001",
  MaKH: "cust-1",
  MaKHCode: "KH001",
  TenKH: "Khách hàng Nguyễn Văn A",
  LoaiCongNo: "Khách hàng",
  SoTien: 1500000,
  SoTienDaTra: 0,
  SoTienConLai: 1500000,
  TrangThai: "Còn nợ",
};

const customerDebt2 = {
  id: "cn-cust-2",
  MaCN: "CN-KH-002",
  MaKH: "cust-2",
  MaKHCode: "KH002",
  TenKH: "Khách hàng Trần Thị B",
  LoaiCongNo: "Khách hàng",
  SoTien: 2500000,
  SoTienDaTra: 500000,
  SoTienConLai: 2000000,
  TrangThai: "Còn nợ",
};

// Run Build HTML Test
const testList = [debtUnpaid, debtPartial, debtPaid, customerDebt1, customerDebt2];

const html = buildDebtsHtml({
  debts: testList,
  supplierDebts: [debtUnpaid, debtPartial, debtPaid],
  suppliers: mockSuppliers,
  dateFrom: "2026-09-01",
  dateTo: "2026-09-30",
});

console.log("\n[1] KIỂM TRA MẪU IN CÔNG NỢ:");

// Check 1: Must NOT have "Công nợ phải thu"
const hasCustomerReceivable = html.toLowerCase().includes("công nợ phải thu");
console.log("- Chứa 'công nợ phải thu'?", hasCustomerReceivable ? "CÓ (LỖI!)" : "KHÔNG (ĐẠT)");
assert.strictEqual(hasCustomerReceivable, false, "Mẫu in không được chứa 'công nợ phải thu'!");

// Check 2: Must NOT have "khách hàng" in tables or headers
const hasCustomerWord = html.includes("Khách hàng Nguyễn Văn A") || html.includes("Trần Thị B");
console.log("- Lọt tên khách hàng vào mẫu in?", hasCustomerWord ? "CÓ (LỖI!)" : "KHÔNG (ĐẠT)");
assert.strictEqual(hasCustomerWord, false, "Mẫu in không được chứa khách hàng!");

// Check 3: Must NOT have "Chênh lệch công nợ"
const hasDifference = html.toLowerCase().includes("chênh lệch công nợ");
console.log("- Chứa 'chênh lệch công nợ'?", hasDifference ? "CÓ (LỖI!)" : "KHÔNG (ĐẠT)");
assert.strictEqual(hasDifference, false, "Mẫu in không được chứa 'chênh lệch công nợ'!");

// Check 4: Must have required supplier info
assert.ok(html.includes("BÁO CÁO CÔNG NỢ PHẢI TRẢ NHÀ CUNG CẤP"), "Thiếu tiêu đề báo cáo công nợ phải trả NCC");
assert.ok(html.includes("Công ty TNHH Pigeon Việt Nam"), "Thiếu tên NCC 1");
assert.ok(html.includes("NCC001"), "Thiếu mã NCC 1");
assert.ok(html.includes("028 3823 1234"), "Thiếu SĐT NCC 1");
assert.ok(html.includes("Nhà phân phối Xe Đạp"), "Thiếu tên NCC 2");
assert.ok(html.includes("Nhà phân phối Bỉm Sạch"), "Thiếu tên NCC 3");
assert.ok(html.includes("Dư nợ đầu kỳ"), "Thiếu cột Dư nợ đầu kỳ");
assert.ok(html.includes("Phát sinh tăng"), "Thiếu cột Phát sinh tăng");
assert.ok(html.includes("Phát sinh giảm"), "Thiếu cột Phát sinh giảm");
assert.ok(html.includes("Công nợ cuối kỳ"), "Thiếu cột Công nợ cuối kỳ");
assert.ok(html.includes("Tổng nợ phải trả NCC"), "Thiếu tổng nợ phải trả NCC");

console.log("- Tiêu đề: BÁO CÁO CÔNG NỢ PHẢI TRẢ NHÀ CUNG CẤP (ĐẠT)");
console.log("- Đầy đủ các cột: Tên NCC, Mã NCC, SĐT, Dư nợ đầu kỳ, Phát sinh tăng, Phát sinh giảm, Công nợ cuối kỳ (ĐẠT)");
console.log("- Kiểm tra loại bỏ hoàn toàn Khách hàng: ĐẠT");

// Check 5: Số tiền tổng cộng
// Tổng phát sinh tăng: 10m + 5m + 4m = 19m
// Tổng phát sinh giảm: 0 + 2m + 4m = 6m
// Tổng cuối kỳ còn phải trả: 10m + 3m + 0 = 13m
assert.ok(html.includes("19.000.000"), "Tổng phát sinh tăng phải là 19.000.000 đ");
assert.ok(html.includes("6.000.000"), "Tổng phát sinh giảm phải là 6.000.000 đ");
assert.ok(html.includes("13.000.000"), "Tổng công nợ cuối kỳ phải là 13.000.000 đ");
console.log("- Số liệu tổng hợp tăng/giảm/còn lại: 19.000.000 / 6.000.000 / 13.000.000 đ (KHỚP CHÍNH XÁC)");

console.log("\n[2] KIỂM TRA DỮ LIỆU THỰC TẾ TỪ MONGODB:");
(async () => {
  const client = new MongoClient(process.env.MONGODB_URI);
  await client.connect();
  const db = client.db(process.env.MONGODB_DB);

  const [allDebts, suppliers] = await Promise.all([
    db.collection("CongNo").find({}).toArray(),
    db.collection("NhaCungCap").find({}).toArray(),
  ]);

  // Bộ lọc đúng như trên màn hình DebtsPage
  const supplierDebts = allDebts.filter((d) => {
    if (
      d.LoaiCongNo === "Khách hàng" ||
      d.type === "customers" ||
      Boolean(d.MaKH) ||
      Boolean(d.MaKHCode) ||
      Boolean(d.MaHD) ||
      Boolean(d.MaDH)
    ) {
      return false;
    }
    return (
      d.LoaiCongNo === "Nhà cung cấp" ||
      d.type === "suppliers" ||
      Boolean(d.MaNCC) ||
      Boolean(d.MaNCCCode) ||
      Boolean(d.MaPN) ||
      Boolean(d.MaPhieuNhap) ||
      Boolean(d.MaDDH)
    );
  });

  console.log(`- Tổng số bản ghi CongNo trong DB: ${allDebts.length}`);
  console.log(`- Số bản ghi lọc được cho Nhà cung cấp: ${supplierDebts.length}`);
  console.log(`- Số bản ghi loại trừ (Khách hàng): ${allDebts.length - supplierDebts.length}`);

  // Test các trường hợp:
  const unpaidList = supplierDebts.filter(d => (Number(d.SoTienConLai ?? (d.SoTien - (d.SoTienDaTra || 0)))) === Number(d.SoTien));
  const partialList = supplierDebts.filter(d => Number(d.SoTienDaTra || 0) > 0 && Number(d.SoTienConLai ?? (d.SoTien - (d.SoTienDaTra || 0))) > 0);
  const fullyPaidList = supplierDebts.filter(d => Number(d.SoTienConLai ?? (d.SoTien - (d.SoTienDaTra || 0))) <= 0);
  const uniqueSuppliers = new Set(supplierDebts.map(d => d.TenNCC || d.MaNCC?.toString())).size;

  console.log(`- Trường hợp còn nợ nguyên vẹn: ${unpaidList.length} khoản`);
  console.log(`- Trường hợp đã thanh toán một phần: ${partialList.length} khoản`);
  console.log(`- Trường hợp đã thanh toán hết: ${fullyPaidList.length} khoản`);
  console.log(`- Số nhà cung cấp cùng tồn tại: ${uniqueSuppliers} NCC`);

  assert.ok(supplierDebts.length > 0, "Phải có dữ liệu công nợ nhà cung cấp");
  assert.ok(uniqueSuppliers > 1, "Phải có nhiều nhà cung cấp cùng tồn tại");

  // In thử với dữ liệu DB
  const dbPrintHtml = buildDebtsHtml({
    debts: supplierDebts,
    supplierDebts,
    suppliers,
  });

  assert.strictEqual(dbPrintHtml.toLowerCase().includes("công nợ phải thu"), false);
  assert.strictEqual(dbPrintHtml.toLowerCase().includes("chênh lệch công nợ"), false);
  assert.ok(dbPrintHtml.includes("BÁO CÁO CÔNG NỢ PHẢI TRẢ NHÀ CUNG CẤP"));
  console.log("- In báo cáo với dữ liệu MongoDB thực tế: HOÀN TOÀN HỢP LỆ VÀ SẠCH SẼ!");

  await client.close();
  console.log("\n==================================================");
  console.log("TẤT CẢ CÁC BÀI TEST ĐÃ HOÀN TẤT THÀNH CÔNG 100%!");
  console.log("==================================================");
})();
