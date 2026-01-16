"""
Configuration settings for Shopify Community Crawler
All settings can be configured via .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Shopify Community settings
BASE_URL = os.getenv("BASE_URL", "https://community.shopify.com")
COMMUNITY_PATH = os.getenv("COMMUNITY_PATH", "/c/jp/13")
FULL_URL = f"{BASE_URL}{COMMUNITY_PATH}"

# Crawler settings
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "1.0"))  # Delay between requests (seconds)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))  # Request timeout (seconds)
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Crawling behavior
MAX_THREADS = int(os.getenv("MAX_THREADS", "0")) or None  # 0 means unlimited
MAX_PAGES = int(os.getenv("MAX_PAGES", "0")) or None  # 0 means unlimited
LIST_ONLY = os.getenv("LIST_ONLY", "false").lower() == "true"  # Only crawl list, not details
EXPORT_LLM = os.getenv("EXPORT_LLM", "false").lower() == "true"  # Export for LLM after crawling

# Output settings
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")  # json or txt
OUTPUT_FILE = os.getenv("OUTPUT_FILE", str(DATA_DIR / "shopify_community_threads.json"))

# Browser settings (for SPA crawling)
USE_BROWSER = os.getenv("USE_BROWSER", "true").lower() == "true"  # Use browser for SPA
BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"  # Run browser in headless mode
BROWSER_WAIT_TIME = int(os.getenv("BROWSER_WAIT_TIME", "5"))  # Wait time for page to load (seconds)
BROWSER_IMPLICIT_WAIT = int(os.getenv("BROWSER_IMPLICIT_WAIT", "10"))  # Implicit wait time (seconds)

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "crawler.log"

