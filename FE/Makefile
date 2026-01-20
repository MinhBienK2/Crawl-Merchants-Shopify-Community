.PHONY: help install dev build start clean lint type-check

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Start development server"
	@echo "  make build        - Build for production"
	@echo "  make start        - Start production server"
	@echo "  make lint         - Run linter"
	@echo "  make type-check   - Run TypeScript type checking"
	@echo "  make clean        - Clean build artifacts"

install:
	npm install

dev:
	npm run dev

build:
	npm run build

start:
	npm run start

lint:
	npm run lint

type-check:
	npm run type-check

clean:
	rm -rf .next
	rm -rf node_modules
	rm -rf out
