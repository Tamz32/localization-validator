# Localization Validator

Công cụ dòng lệnh Python kiểm tra hai bảng CSV trước khi dùng bản dịch. Dự án được tách từ kinh nghiệm làm quy trình Việt hóa game của mình.

- Kiểm tra ID thiếu, ID thừa, ID trùng và dòng sai cấu trúc CSV.
- Kiểm tra thứ tự biến chèn, mã màu và mã xuống dòng.
- Báo ID bị lỗi và trả mã thoát để có thể đưa vào các bước kiểm tra tự động.

## Chạy thử

Cần Python 3.9 trở lên, dùng thư viện chuẩn.

```bash
python validate.py examples/source.csv examples/vi.csv
python validate.py examples/source.csv examples/vi-invalid.csv
```

Ví dụ đầu trả mã thoát `0`. Ví dụ thứ hai trả `1` vì mã mục tiêu bị đổi. CSV không đọc được hoặc sai định dạng trả `2`.

Hai bảng dùng UTF-8 và có cột `id,text`. Các tệp ví dụ dùng dữ liệu tự tạo.
