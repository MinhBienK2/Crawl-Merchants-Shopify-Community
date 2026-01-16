# Shopify Community Crawler

Ứng dụng crawl và download tất cả các hội thoại (threads) từ Shopify Community forum để phân tích bằng LLM.

> ⚡ **Quick Start**: Xem [QUICKSTART.md](QUICKSTART.md) để bắt đầu nhanh với `uv`

## 📋 Mục đích

Công cụ này giúp bạn:
- Crawl tất cả các threads từ một section của Shopify Community
- Lưu dữ liệu dưới dạng JSON hoặc text
- Export dữ liệu ở định dạng tối ưu cho LLM analysis
- Tổ chức code theo tiêu chuẩn clean code

## 🏗️ Cấu trúc Project

```
merchants-community-crawl/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── config.py          # Cấu hình crawler
├── src/                    # Source code chính
│   ├── __init__.py
│   ├── crawler.py         # Module crawl dữ liệu
│   ├── parser.py          # Module parse HTML
│   ├── storage.py         # Module lưu dữ liệu
│   └── logger.py          # Logging system
├── data/                   # Thư mục chứa dữ liệu output
├── logs/                   # Thư mục chứa log files
├── main.py                 # Entry point chính
├── pyproject.toml          # Project configuration (uv)
├── requirements.txt        # Python dependencies (backup)
├── Makefile                # Make commands (Linux/Mac)
├── scripts/                # Setup scripts
│   ├── setup.sh           # Setup script (Linux/Mac)
│   └── setup.ps1          # Setup script (Windows)
├── .gitignore
├── README.md
└── QUICKSTART.md          # Quick start guide
```

## 🚀 Cài đặt

### 1. Clone hoặc tải project

```bash
cd merchants-community-crawl
```

### 2. Cài đặt uv (nếu chưa có)

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Hoặc dùng pip (không khuyến nghị, nhưng có thể dùng)
pip install uv
```

### 3. Cài đặt dependencies với uv

```bash
# uv sẽ tự động tạo virtual environment và cài đặt packages
uv sync

# Hoặc nếu muốn chỉ cài dependencies (không có dev dependencies)
uv pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
# Cách 1: Sử dụng uv (khuyến nghị - tự động dùng virtual environment)
uv run python main.py

# Cách 2: Sử dụng Makefile (Linux/Mac)
make run

# Cách 3: Activate virtual environment thủ công
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Sau đó chạy bình thường
python main.py
```

### 5. Sử dụng Makefile (Linux/Mac) hoặc Scripts (Windows)

**Linux/Mac:**
```bash
make help          # Xem tất cả commands
make setup         # Cài đặt dependencies
make run           # Chạy crawler
make run-test      # Test với 5 threads
make clean         # Xóa cache files
```

**Windows:**
```powershell
# Chạy setup script
.\scripts\setup.ps1

# Hoặc dùng uv trực tiếp
uv sync
uv run python main.py
```

## 💻 Sử dụng

### Crawl tất cả threads (mặc định)

```bash
# Với uv (khuyến nghị - tự động dùng virtual environment)
uv run python main.py

# Hoặc sau khi activate virtual environment
python main.py
```

### Crawl với giới hạn số lượng threads

```bash
# Chỉ crawl 50 threads đầu tiên
uv run python main.py --max-threads 50
```

### Crawl với giới hạn số trang

```bash
# Chỉ crawl 3 trang đầu tiên
uv run python main.py --max-pages 3
```

### Chỉ crawl danh sách threads (không crawl nội dung chi tiết)

```bash
uv run python main.py --list-only
```

### Chỉ định file output tùy chỉnh

```bash
uv run python main.py --output data/my_custom_output.json
```

### Export dữ liệu cho LLM

```bash
uv run python main.py --export-llm
```

### Crawl từ URL khác

```bash
uv run python main.py --url "https://community.shopify.com/c/jp/13"
```

### Kết hợp các options

```bash
uv run python main.py --max-threads 100 --max-pages 5 --export-llm --format json
```

## 🔧 Quản lý Dependencies với uv

### Thêm package mới

```bash
uv add package-name
```

### Thêm dev dependency

```bash
uv add --dev package-name
```

### Xóa package

```bash
uv remove package-name
```

### Cập nhật tất cả packages

```bash
uv sync --upgrade
```

### Xem danh sách packages

```bash
uv pip list
```

## 📊 Output Format

### JSON Format (mặc định)

Dữ liệu được lưu dưới dạng JSON với cấu trúc:

```json
{
  "metadata": {
    "crawl_date": "2024-01-15T10:30:00",
    "total_threads": 150,
    "source": "Shopify Community"
  },
  "threads": [
    {
      "title": "Thread title",
      "url": "https://community.shopify.com/...",
      "author": "username",
      "thread_id": "thread-id",
      "post_count": 5,
      "views": 100,
      "tags": ["tag1", "tag2"],
      "posts": [
        {
          "post_number": 1,
          "post_id": "12345",
          "author": "username",
          "content": "Post content...",
          "timestamp": "2024-01-15T10:00:00",
          "likes": 5,
          "is_original_post": true
        }
      ],
      "total_posts": 5
    }
  ]
}
```

### Text Format

Dữ liệu được format dưới dạng text dễ đọc, phù hợp cho LLM analysis.

## ⚙️ Cấu hình

Chỉnh sửa file `config/config.py` để thay đổi các settings:

- `REQUEST_DELAY`: Thời gian delay giữa các requests (mặc định: 1.0 giây)
- `REQUEST_TIMEOUT`: Timeout cho mỗi request (mặc định: 30 giây)
- `MAX_RETRIES`: Số lần retry khi request thất bại (mặc định: 3)
- `OUTPUT_FORMAT`: Định dạng output (json hoặc txt)
- `LOG_LEVEL`: Mức độ logging (DEBUG, INFO, WARNING, ERROR)

## 📝 Logging

Logs được lưu trong thư mục `logs/` với file `crawler.log`. Logs cũng được hiển thị trên console.

## 🔍 Sử dụng dữ liệu với LLM

Sau khi crawl xong, bạn có thể:

1. **Sử dụng file JSON trực tiếp**: Import vào Python và xử lý
2. **Sử dụng file LLM export**: Chạy với `--export-llm` để tạo file `data/llm_input.txt` được format tối ưu cho LLM

Ví dụ sử dụng với Python:

```python
import json

with open('data/shopify_community_threads.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for thread in data['threads']:
    print(f"Thread: {thread['title']}")
    for post in thread['posts']:
        print(f"  - {post['author']}: {post['content'][:100]}...")
```

## 🛠️ Development

### Cấu trúc Code

- **Separation of Concerns**: Mỗi module có trách nhiệm riêng biệt
- **Error Handling**: Tất cả các operations đều có error handling
- **Logging**: Comprehensive logging system
- **Configuration**: Centralized configuration management
- **Type Hints**: Code sử dụng type hints để dễ maintain

### Thêm tính năng mới

1. Thêm logic crawl vào `src/crawler.py`
2. Thêm logic parse vào `src/parser.py`
3. Thêm logic storage vào `src/storage.py`
4. Update `main.py` nếu cần thêm CLI options

## ⚠️ Lưu ý

- Crawler có delay giữa các requests để tránh overload server
- Một số trang có thể yêu cầu authentication hoặc có rate limiting
- HTML structure của Shopify Community có thể thay đổi, cần update parser nếu cần
- Luôn tuân thủ robots.txt và terms of service của Shopify

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

