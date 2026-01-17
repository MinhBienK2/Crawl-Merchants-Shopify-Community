# Quick Start Guide

Hướng dẫn nhanh để bắt đầu với Shopify Community Crawler sử dụng `uv`.

## ⚡ Cài đặt nhanh (3 bước)

### 1. Cài đặt uv

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Hoặc dùng pip:**
```bash
pip install uv
```

### 2. Cài đặt dependencies

```bash
uv sync
```

Lệnh này sẽ:
- Tự động tạo virtual environment trong `.venv/`
- Cài đặt tất cả dependencies từ `pyproject.toml`
- Không cần activate virtual environment thủ công!

### 3. Chạy crawler

```bash
# Test với 5 threads đầu tiên
uv run python main.py --max-threads 5 --max-pages 1
```

## 🎯 Các lệnh thường dùng

```bash
# Chạy crawler
uv run python main.py

# Crawl với options
uv run python main.py --max-threads 50 --export-llm

# Thêm package mới
uv add package-name

# Xem packages đã cài
uv pip list

# Cập nhật packages
uv sync --upgrade
```

## 💡 Lợi ích của uv

✅ **Nhanh hơn pip**: Tốc độ cài đặt nhanh hơn 10-100x  
✅ **Tự động quản lý venv**: Không cần tạo/activate thủ công  
✅ **Reproducible**: Lock file đảm bảo môi trường giống nhau  
✅ **Không cài global**: Tất cả packages trong `.venv/` của project  

## 🔄 So sánh với pip truyền thống

| Thao tác | pip truyền thống | uv |
|----------|------------------|-----|
| Cài đặt | `pip install -r requirements.txt` | `uv sync` |
| Chạy script | `python main.py` (sau khi activate) | `uv run python main.py` |
| Thêm package | `pip install pkg` | `uv add pkg` |
| Tạo venv | `python -m venv venv` | Tự động |

## 📁 Virtual Environment

uv tự động tạo virtual environment trong `.venv/` (đã được ignore trong .gitignore).

Nếu muốn activate thủ công:

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

Sau đó có thể chạy `python main.py` bình thường.

## ❓ Troubleshooting

**Q: Lệnh `uv` không tìm thấy?**  
A: Thêm `$HOME/.cargo/bin` vào PATH hoặc restart terminal.

**Q: Muốn dùng Python version khác?**  
A: `uv python install 3.11` rồi `uv sync --python 3.11`

**Q: Có thể dùng pip thay vì uv không?**  
A: Có, nhưng phải tự tạo venv và activate. `requirements.txt` vẫn được giữ để tương thích.

