"""
Web crawler for Shopify Community forum
"""
import time
import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from config.config import (
    REQUEST_DELAY, REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT, FULL_URL,
    BROWSER_HEADLESS, BROWSER_WAIT_TIME, BROWSER_IMPLICIT_WAIT
)
from src.parser import ShopifyCommunityParser
from src.logger import setup_logger

logger = setup_logger(__name__)


class ShopifyCommunityCrawler:
    """Crawler for Shopify Community forum threads"""
    
    def __init__(self, base_url: str = FULL_URL):
        """
        Initialize crawler
        
        Args:
            base_url: Base URL of the community section to crawl
        """
        self.base_url = base_url
        self.parser = ShopifyCommunityParser("https://community.shopify.com")
        self.session = self._create_session()
        self.crawled_urls = set()
        self.driver = self._create_browser()
    
    def _create_session(self) -> requests.Session:
        """
        Create and configure requests session
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        return session
    
    def _create_browser(self) -> Optional[webdriver.Chrome]:
        """
        Create and configure Selenium browser for SPA crawling
        
        Returns:
            Configured Chrome WebDriver or None if failed
        """
        try:
            chrome_options = Options()
            
            if BROWSER_HEADLESS:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'--user-agent={USER_AGENT}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Use webdriver-manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(BROWSER_IMPLICIT_WAIT)
            
            logger.info("Browser initialized successfully for SPA crawling")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            logger.warning("Falling back to requests-only mode")
            return None
    
    def _close_browser(self):
        """Close browser if it exists"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")
            finally:
                self.driver = None
    
    def _make_request_spa(self, url: str) -> Optional[str]:
        """
        Make request to SPA page using Selenium browser
        
        Args:
            url: URL to request
            
        Returns:
            HTML content after JavaScript execution or None if failed
        """
        if not self.driver:
            logger.error("Browser not initialized, cannot crawl SPA")
            return None
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Loading SPA page: {url} (attempt {attempt + 1}/{MAX_RETRIES})")
                self.driver.get(url)
                
                # Wait for page to load and content to appear
                # Wait for common elements that indicate page is loaded
                try:
                    WebDriverWait(self.driver, BROWSER_WAIT_TIME).until(
                        lambda d: d.execute_script('return document.readyState') == 'complete'
                    )
                    # Additional wait for dynamic content
                    time.sleep(2)  # Give extra time for JavaScript to render
                    
                    # Try to wait for post elements or main content
                    try:
                        WebDriverWait(self.driver, BROWSER_WAIT_TIME).until(
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                    except TimeoutException:
                        logger.warning(f"Timeout waiting for content on {url}, but continuing...")
                    
                except TimeoutException as e:
                    logger.warning(f"Page load timeout for {url}: {e}, but continuing...")

                print("\n--- Bắt đầu scroll ---")
                # Selector cho posts với virtualization
                post_selector = 'article[data-post-id]'
                collected_post_ids = set()
                scroll_pause_time = 2.0
                max_scrolls = 30
                no_new_posts_count = 0
                max_no_new_posts = 3  # Dừng sau 3 lần scroll không có post mới
                
                for scroll_attempt in range(max_scrolls):
                    # Thu thập posts hiện có trong DOM
                    posts = self.driver.find_elements(By.CSS_SELECTOR, post_selector)
                    new_posts_found = 0
                    
                    for post in posts:
                        try:
                            post_id = post.get_attribute('data-post-id')
                            if post_id and post_id not in collected_post_ids:
                                collected_post_ids.add(post_id)
                                new_posts_found += 1
                        except Exception as e:
                            logger.debug(f"Error getting post_id: {e}")
                    
                    if new_posts_found > 0:
                        print(f"Scroll {scroll_attempt + 1}: Tìm thấy {new_posts_found} posts mới (Tổng: {len(collected_post_ids)} posts)")
                        no_new_posts_count = 0
                    else:
                        no_new_posts_count += 1
                        if no_new_posts_count >= max_no_new_posts:
                            print(f"Không còn posts mới sau {max_no_new_posts} lần scroll. Dừng scroll.")
                            break
                    
                    # Scroll xuống một đoạn
                    scroll_amount = 800  # Pixels
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(scroll_pause_time)
                    
                    # Kiểm tra xem đã scroll đến cuối chưa
                    scroll_position = self.driver.execute_script("return window.pageYOffset;")
                    page_height = self.driver.execute_script("return document.body.scrollHeight;")
                    window_height = self.driver.execute_script("return window.innerHeight;")
                    
                    if scroll_position + window_height >= page_height - 100:
                        # Có thể đã đến cuối, đợi thêm một chút để load content mới
                        time.sleep(scroll_pause_time)
                        # Kiểm tra lại xem có content mới không
                        new_page_height = self.driver.execute_script("return document.body.scrollHeight;")
                        if new_page_height == page_height:
                            # Không có content mới, có thể đã đến cuối thực sự
                            if no_new_posts_count >= max_no_new_posts - 1:
                                break
                
                print(f"\n--- Hoàn thành scroll --- Tổng thu thập: {len(collected_post_ids)} posts")

                
                # Get the page source after JavaScript execution
                html = self.driver.page_source
                
                if html and len(html) > 100:  # Basic validation
                    return html
                else:
                    logger.warning(f"Received empty or invalid HTML from {url}")
                    return None
                    
            except WebDriverException as e:
                logger.warning(f"Browser error (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(REQUEST_DELAY * (attempt + 1))
                else:
                    logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                    return None
            except Exception as e:
                logger.error(f"Unexpected error fetching {url}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(REQUEST_DELAY * (attempt + 1))
                else:
                    return None
        
        return None
    
    def _make_request(self, url: str) -> Optional[str]:
        """
        Make HTTP request with retry logic
        
        Args:
            url: URL to request
            
        Returns:
            HTML content or None if request failed
        """
        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Requesting: {url} (attempt {attempt + 1}/{MAX_RETRIES})")
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                # Check if we got HTML
                if 'text/html' in response.headers.get('Content-Type', ''):
                    return response.text
                else:
                    logger.warning(f"Unexpected content type: {response.headers.get('Content-Type')}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(REQUEST_DELAY * (attempt + 1))
                else:
                    logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                    return None
        
        return None
    
    def crawl_thread_list(self, start_url: Optional[str] = None, max_pages: Optional[int] = None) -> List[Dict]:
        """
        Crawl thread list from community pages
        
        Args:
            start_url: URL to start crawling from (defaults to base_url)
            max_pages: Maximum number of pages to crawl (None for all)
            
        Returns:
            List of thread dictionaries
        """
        all_threads = []
        current_url = start_url or self.base_url
        page_count = 0
        
        logger.info(f"Starting to crawl thread list from: {current_url}")
        
        while current_url:
            if max_pages and page_count >= max_pages:
                logger.info(f"Reached maximum page limit: {max_pages}")
                break
            
            page_count += 1
            logger.info(f"Crawling page {page_count}: {current_url}")
            
            html = self._make_request(current_url)
            if not html:
                logger.error(f"Failed to fetch page: {current_url}")
                break
            
            # Parse threads from current page
            threads = self.parser.parse_thread_list(html)
            all_threads.extend(threads)
            logger.info(f"Found {len(threads)} threads on page {page_count}")
            
            # Find next page
            next_url = self.parser.find_next_page_url(html)
            if next_url and next_url != current_url:
                current_url = next_url
                time.sleep(REQUEST_DELAY)  # Be respectful with delays
            else:
                logger.info("No more pages to crawl")
                break
        
        logger.info(f"Total threads found: {len(all_threads)}")
        return all_threads
    
    def crawl_thread_detail(self, thread_url: str) -> Optional[Dict]:
        """
        Crawl detailed content of a single thread (supports SPA and preloaded data)
        
        Args:
            thread_url: URL of the thread to crawl
            
        Returns:
            Dictionary with complete thread data or None if failed
        """
        if thread_url in self.crawled_urls:
            logger.debug(f"Thread already crawled: {thread_url}")
            return None
        
        logger.info(f"Crawling thread: {thread_url}")
        
        # Try regular HTTP request first (faster, no Selenium needed)
        html = self._make_request(thread_url)
        
        if not html:
            logger.error(f"Failed to fetch thread: {thread_url}")
            return None
        
        # Try to parse from preloaded data first (faster, no JavaScript needed)
        thread_data = self.parser.parse_thread_detail_from_preloaded(html, thread_url)
        
        if not thread_data:
            # Fallback to SPA parsing if preloaded data not found
            logger.info(f"Preloaded data not found, trying SPA parsing for: {thread_url}")
            html = self._make_request_spa(thread_url)
            
            if not html:
                logger.error(f"Failed to fetch thread with SPA: {thread_url}")
                return None
            
            # Try preloaded data again from SPA response
            thread_data = self.parser.parse_thread_detail_from_preloaded(html, thread_url)
            
            # If still no preloaded data, fallback to HTML parsing
            if not thread_data:
                logger.info(f"Falling back to HTML parsing for: {thread_url}")
                thread_data = self.parser.parse_thread_detail(html, thread_url)
        
        if not thread_data:
            logger.error(f"Failed to parse thread data: {thread_url}")
            return None
        
        self.crawled_urls.add(thread_url)
        
        # Check for pagination in thread (multiple pages of posts)
        next_page = self.parser.find_next_page_url(html)
        if next_page and next_page not in self.crawled_urls:
            logger.info(f"Thread has multiple pages, crawling next page: {next_page}")
            time.sleep(REQUEST_DELAY)
            
            next_html = self._make_request(next_page)
            if not next_html:
                next_html = self._make_request_spa(next_page)
            
            if next_html:
                next_page_data = self.parser.parse_thread_detail_from_preloaded(next_html, next_page)
                if not next_page_data:
                    next_page_data = self.parser.parse_thread_detail(next_html, next_page)
                
                if next_page_data and 'posts' in next_page_data:
                    thread_data['posts'].extend(next_page_data['posts'])
                    self.crawled_urls.add(next_page)
        
        return thread_data
    
    def crawl_all_threads(self, max_threads: Optional[int] = None, max_pages: Optional[int] = None) -> List[Dict]:
        """
        Crawl all threads with their full content
        
        Args:
            max_threads: Maximum number of threads to crawl (None for all)
            max_pages: Maximum number of list pages to crawl (None for all)
            
        Returns:
            List of complete thread data dictionaries
        """
        # First, get list of all threads
        thread_list = self.crawl_thread_list(max_pages=max_pages)
        
        if max_threads:
            thread_list = thread_list[:max_threads]
        
        logger.info(f"Starting to crawl {len(thread_list)} threads in detail")
        
        all_thread_data = []
        
        for idx, thread_info in enumerate(thread_list, 1):
            if 'url' not in thread_info:
                logger.warning(f"Thread {idx} missing URL, skipping")
                continue
            
            thread_detail = self.crawl_thread_detail(thread_info['url'])
            if thread_detail:
                # Merge basic info with detailed data
                thread_detail.update({
                    k: v for k, v in thread_info.items() 
                    if k not in thread_detail
                })
                all_thread_data.append(thread_detail)
            
            # Progress logging
            if idx % 10 == 0:
                logger.info(f"Progress: {idx}/{len(thread_list)} threads crawled")
            
            # Respectful delay between requests
            time.sleep(REQUEST_DELAY)
        
        logger.info(f"Completed crawling {len(all_thread_data)} threads")
        
        # Close browser when done
        if self.driver:
            self._close_browser()
        
        return all_thread_data
    
    def __del__(self):
        """Cleanup: close browser when crawler is destroyed"""
        self._close_browser()

