.PHONY: help install run test clean setup

help: ## Hiển thị help message
	@echo "Shopify Community Crawler - Makefile Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup: ## Cài đặt uv và dependencies
	@echo "🚀 Setting up project..."
	@if ! command -v uv &> /dev/null; then \
		echo "📦 Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@echo "📥 Installing dependencies..."
	uv sync
	@echo "✅ Setup completed!"

install: ## Cài đặt dependencies (alias cho setup)
	@$(MAKE) setup

run: ## Chạy crawler với options mặc định
	uv run python main.py

run-test: ## Chạy crawler với 5 threads để test
	uv run python main.py --max-threads 5 --max-pages 1

run-export: ## Chạy crawler và export cho LLM
	uv run python main.py --export-llm

clean: ## Xóa cache và build files
	@echo "🧹 Cleaning..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	@echo "✅ Clean completed!"

clean-all: clean ## Xóa tất cả bao gồm venv và data
	@echo "🧹 Cleaning all..."
	rm -rf .venv
	rm -rf data/*
	rm -rf logs/*
	@echo "✅ Clean all completed!"

update: ## Cập nhật tất cả packages
	uv sync --upgrade

add: ## Thêm package mới (usage: make add PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "❌ Error: PACKAGE is required"; \
		echo "Usage: make add PACKAGE=package-name"; \
		exit 1; \
	fi
	uv add $(PACKAGE)

remove: ## Xóa package (usage: make remove PACKAGE=package-name)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "❌ Error: PACKAGE is required"; \
		echo "Usage: make remove PACKAGE=package-name"; \
		exit 1; \
	fi
	uv remove $(PACKAGE)

list: ## Liệt kê tất cả packages đã cài
	uv pip list

