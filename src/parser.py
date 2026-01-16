"""
HTML Parser for extracting thread data from Shopify Community pages
"""
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urljoin
from src.logger import setup_logger

logger = setup_logger(__name__)


class ShopifyCommunityParser:
    """Parser for Shopify Community forum pages"""
    
    def __init__(self, base_url: str):
        """
        Initialize parser
        
        Args:
            base_url: Base URL of Shopify Community
        """
        self.base_url = base_url
    
    def parse_thread_list(self, html: str) -> List[Dict]:
        """
        Parse thread list from community page
        
        Args:
            html: HTML content of the page
            
        Returns:
            List of thread dictionaries with basic info
        """
        soup = BeautifulSoup(html, 'lxml')
        threads = []
        
        try:
            # Find thread containers (adjust selectors based on actual HTML structure)
            thread_elements = soup.find_all('tr', class_='topic-list-item') or \
                            soup.find_all('div', class_='topic-list-item') or \
                            soup.find_all('article', class_='topic-list-item')
            
            if not thread_elements:
                # Try alternative selectors
                thread_elements = soup.select('tbody tr') or \
                                soup.select('.topic-list-item')
            
            logger.info(f"Found {len(thread_elements)} thread elements")
            
            for element in thread_elements:
                thread_data = self._extract_thread_info(element)
                if thread_data:
                    threads.append(thread_data)
            
        except Exception as e:
            logger.error(f"Error parsing thread list: {e}")
        
        return threads
    
    def _extract_thread_info(self, element) -> Optional[Dict]:
        """
        Extract thread information from a single thread element
        
        Args:
            element: BeautifulSoup element containing thread info
            
        Returns:
            Dictionary with thread information or None
        """
        try:
            thread_data = {}
            
            # Extract title and link
            title_link = element.find('a', class_='title') or \
                        element.find('a', href=lambda x: x and '/t/' in x) or \
                        element.select_one('a[href*="/t/"]')
            
            if title_link:
                thread_data['title'] = title_link.get_text(strip=True)
                relative_url = title_link.get('href', '')
                thread_data['url'] = urljoin(self.base_url, relative_url)
                thread_data['thread_id'] = self._extract_thread_id(relative_url)
            else:
                return None
            
            # Extract author
            author_elem = element.find('a', class_='poster') or \
                         element.find('span', class_='poster') or \
                         element.select_one('.poster a')
            if author_elem:
                thread_data['author'] = author_elem.get_text(strip=True)
            
            # Extract post count
            post_count_elem = element.find('span', class_='posts') or \
                            element.select_one('.posts, .post-count')
            if post_count_elem:
                try:
                    thread_data['post_count'] = int(post_count_elem.get_text(strip=True))
                except (ValueError, AttributeError):
                    thread_data['post_count'] = 0
            
            # Extract views
            views_elem = element.find('span', class_='views') or \
                        element.select_one('.views, .view-count')
            if views_elem:
                try:
                    thread_data['views'] = int(views_elem.get_text(strip=True))
                except (ValueError, AttributeError):
                    thread_data['views'] = 0
            
            # Extract last activity
            last_activity = element.find('span', class_='last-activity') or \
                          element.select_one('.last-activity, .relative-date')
            if last_activity:
                thread_data['last_activity'] = last_activity.get_text(strip=True)
            
            # Extract category/tags
            tags = []
            tag_elements = element.find_all('a', class_='badge') or \
                          element.select('.badge, .tag')
            for tag_elem in tag_elements:
                tag_text = tag_elem.get_text(strip=True)
                if tag_text:
                    tags.append(tag_text)
            thread_data['tags'] = tags
            
            return thread_data
            
        except Exception as e:
            logger.error(f"Error extracting thread info: {e}")
            return None
    
    def _extract_thread_id(self, url: str) -> Optional[str]:
        """
        Extract thread ID from URL
        
        Args:
            url: Thread URL
            
        Returns:
            Thread ID or None
        """
        try:
            # URL format: /c/jp/13/t/thread-name/12345
            parts = url.split('/')
            if 't' in parts:
                idx = parts.index('t')
                if idx + 1 < len(parts):
                    return parts[idx + 1]
        except Exception:
            pass
        return None
    
    def parse_thread_detail(self, html: str, thread_url: str) -> Dict:
        """
        Parse detailed thread content including all posts
        
        Args:
            html: HTML content of the thread page
            thread_url: URL of the thread
            
        Returns:
            Dictionary with complete thread data including all posts
        """
        soup = BeautifulSoup(html, 'lxml')
        thread_data = {
            'url': thread_url,
            'posts': []
        }
        
        try:
            # Extract thread title
            title_elem = soup.find('h1', class_='fancy-title') or \
                        soup.find('h1') or \
                        soup.select_one('h1.title, .topic-title h1')
            if title_elem:
                thread_data['title'] = title_elem.get_text(strip=True)
            
            # Extract all posts
            post_elements = soup.find_all('article', class_='post') or \
                          soup.find_all('div', class_='post') or \
                          soup.select('.post, article[data-post-id]')
            
            if not post_elements:
                # Try alternative selectors
                post_elements = soup.select('.topic-post, .post-wrapper')
            
            logger.debug(f"Found {len(post_elements)} posts in thread")
            
            for idx, post_elem in enumerate(post_elements):
                post_data = self._extract_post_info(post_elem, idx)
                if post_data:
                    thread_data['posts'].append(post_data)
            
            # Extract metadata
            thread_data['total_posts'] = len(thread_data['posts'])
            
        except Exception as e:
            logger.error(f"Error parsing thread detail: {e}")
        
        return thread_data
    
    def _extract_post_info(self, element, post_number: int) -> Optional[Dict]:
        """
        Extract information from a single post element
        
        Args:
            element: BeautifulSoup element containing post info
            post_number: Post number in the thread (0-indexed)
            
        Returns:
            Dictionary with post information or None
        """
        try:
            post_data = {
                'post_number': post_number + 1,
                'is_original_post': post_number == 0
            }
            
            # Extract post ID
            post_id = element.get('data-post-id') or \
                     element.get('id', '').replace('post_', '')
            if post_id:
                post_data['post_id'] = post_id
            
            # Extract author
            author_elem = element.find('a', class_='poster') or \
                        element.select_one('.poster a, .username a')
            if author_elem:
                post_data['author'] = author_elem.get_text(strip=True)
                post_data['author_url'] = urljoin(self.base_url, author_elem.get('href', ''))
            
            # Extract post content
            content_elem = element.find('div', class_='post-content') or \
                          element.select_one('.post-content, .cooked, .post-body')
            if content_elem:
                # Get text content
                post_data['content'] = content_elem.get_text(separator='\n', strip=True)
                # Also keep HTML for potential future use
                post_data['content_html'] = str(content_elem)
            
            # Extract timestamp
            time_elem = element.find('time') or \
                       element.select_one('time, .post-date, .relative-date')
            if time_elem:
                post_data['timestamp'] = time_elem.get('datetime') or \
                                       time_elem.get_text(strip=True)
            
            # Extract likes/reactions
            likes_elem = element.find('span', class_='like-count') or \
                        element.select_one('.like-count, .reactions-count')
            if likes_elem:
                try:
                    post_data['likes'] = int(likes_elem.get_text(strip=True))
                except (ValueError, AttributeError):
                    post_data['likes'] = 0
            
            return post_data if 'content' in post_data else None
            
        except Exception as e:
            logger.error(f"Error extracting post info: {e}")
            return None
    
    def find_next_page_url(self, html: str) -> Optional[str]:
        """
        Find URL for the next page of threads
        
        Args:
            html: HTML content of current page
            
        Returns:
            URL of next page or None if no next page
        """
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            # Look for pagination links
            next_link = soup.find('a', class_='next') or \
                       soup.find('a', rel='next') or \
                       soup.select_one('a.next, .pagination a.next')
            
            if next_link and next_link.get('href'):
                return urljoin(self.base_url, next_link.get('href'))
            
        except Exception as e:
            logger.error(f"Error finding next page: {e}")
        
        return None

