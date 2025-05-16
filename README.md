BÀI DỰ THI LẬP TRÌNH VIÊN BACKEND RTLS ORBRO ỨNG VIÊN NGUYỄN NGỌC LINH

Trong repository này là toàn bộ kết quả làm Bài thi Lập trình viên Backend RTLS đã được tổng hợp lại

✅ CẤU TRÚC PROJECT 
\
project_name/ \
├── main.py                # File thực thi chính \
├── parser.py              # Xử lý nhận và phân tích cú pháp (Parsing) Tag \
├── api.py                 # REST API dựa trên FastAPI \
├── db.py                  # Logic lưu trữ SQLite (nếu làm Bài tập tùy chọn) \
├── tag_simulator.py       # Simulator do ứng viên tự viết \
├── requirements.txt       # Danh sách các gói phụ thuộc (Dependencies) \
└── README.md              # Tài liệu này

✅ THIẾT LẬP MÔI TRƯỜNG
\
Hoạt động trên Ubuntu 20.04 / Python 3.9 trở lên
\
python3 -m venv venv \
source venv/bin/activate \
pip install -r requirements.txt

✅ Phương pháp thực hiện
1. Chạy Tag Simulator
   #### Chạy mô phỏng in chuẩn
   python tag_simulator.py --mode stdout
   #### Ghi vào file custom.log
   python tag_simulator.py --mode file --file simulator.log
   #### Gửi HTTP tới server tiếp nhận
   python tag_simulator.py --mode socket --api-url http://localhost:8001/log
   #### Chạy mô phỏng với tags tùy chỉnh
   --tags <tag_id> <tag_id> ...

2. Chạy Server tiếp nhận \
   python main.py

3. Chạy API Server (FastAPI) \
uvicorn api:app --reload --host 0.0.0.0 --port 8000

✅ Ví dụ API
\
Đăng ký
curl -X POST http://localhost:8000/tags -H "Content-Type: application/json" -d '{"id": "fa451f0755d8", "description": "Helmet Tag for worker A"}' \
Tra cứu toàn bộ \
curl http://localhost:8000/tags \
Tra cứu chi tiết \
curl http://localhost:8000/tag/fa451f0755d8

✅ Thiết lập SQLite (nếu làm Bài tập tùy chọn)
\
Cơ sở dữ liệu SQLite được lưu vào file tag_data.db

✅ Phuơng thức giả lập (simulation) Tag
- Định nghĩa danh sách Tag mặc định hoặc người dùng nhập
- Hàm generator với vòng lặp vô hạn, sinh chuỗi theo yêu cầu với CNT tăng dần
- Triển khai tự do theo standard output, file output và Socket