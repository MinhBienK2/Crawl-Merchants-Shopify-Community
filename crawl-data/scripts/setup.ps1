# Setup script for Windows PowerShell

Write-Host "🚀 Setting up Shopify Community Crawler..." -ForegroundColor Cyan

# Check if uv is installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing uv..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing | Invoke-Expression
}

Write-Host "✅ uv is installed" -ForegroundColor Green

# Sync dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
uv sync

Write-Host "✅ Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the crawler:" -ForegroundColor Cyan
Write-Host "  uv run python main.py"
Write-Host ""
Write-Host "Or activate virtual environment:" -ForegroundColor Cyan
Write-Host "  .venv\Scripts\Activate.ps1"
Write-Host "  python main.py"

