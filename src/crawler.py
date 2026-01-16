"""
Web crawler for Shopify Community forum
"""
import time
import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin
from config.config import (
    REQUEST_DELAY, REQUEST_TIMEOUT, MAX_RETRIES, USER_AGENT, FULL_URL
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
        Crawl detailed content of a single thread
        
        Args:
            thread_url: URL of the thread to crawl
            
        Returns:
            Dictionary with complete thread data or None if failed
        """
        if thread_url in self.crawled_urls:
            logger.debug(f"Thread already crawled: {thread_url}")
            return None
        
        logger.info(f"Crawling thread: {thread_url}")
        
        html = self._make_request(thread_url)
        if not html:
            logger.error(f"Failed to fetch thread: {thread_url}")
            return None
        
        thread_data = self.parser.parse_thread_detail(html, thread_url)
        self.crawled_urls.add(thread_url)
        
        # Check for pagination in thread (multiple pages of posts)
        next_page = self.parser.find_next_page_url(html)
        if next_page and next_page not in self.crawled_urls:
            logger.info(f"Thread has multiple pages, crawling next page: {next_page}")
            time.sleep(REQUEST_DELAY)
            next_html = self._make_request(next_page)
            if next_html:
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
        return all_thread_data

