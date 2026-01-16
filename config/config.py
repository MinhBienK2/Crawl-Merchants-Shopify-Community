"""
Configuration settings for Shopify Community Crawler
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
BASE_URL = "https://community.shopify.com"
COMMUNITY_PATH = "/c/jp/13"
FULL_URL = f"{BASE_URL}{COMMUNITY_PATH}"

# Crawler settings
REQUEST_DELAY = 1.0  # Delay between requests (seconds)
REQUEST_TIMEOUT = 30  # Request timeout (seconds)
MAX_RETRIES = 3
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Output settings
OUTPUT_FORMAT = "json"  # json or txt
OUTPUT_FILE = DATA_DIR / "shopify_community_threads.json"

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "crawler.log"

