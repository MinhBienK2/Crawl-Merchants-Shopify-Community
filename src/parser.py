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
            
            # Extract post count
            replies_count_elem = element.find('span', class_='posts') or \
                            element.select_one('.posts, .post-count')
            if replies_count_elem:
                try:
                    thread_data['replies'] = int(replies_count_elem.get_text(strip=True))
                except (ValueError, AttributeError):
                    thread_data['replies'] = 0
            
            # Extract views
            views_elem = element.find('span', class_='views')
            if views_elem:
                try:
                    thread_data['views'] = int(views_elem.get_text(strip=True))
                except (ValueError, AttributeError):
                    thread_data['views'] = 0
            
            # Extract last activity
            last_activity = element.find('a', class_='post-activity') or \
                        element.select_one('.activity, .post-activity')
            if last_activity:
                thread_data['last_activity'] = last_activity.get_text(strip=True)
            
            # badge-category
            badge_category = element.find('span', class_='badge-category') or \
                        element.select_one('.badge-category, .badge-category__name')
            if badge_category:
                thread_data['category'] = badge_category.get_text(strip=True)

            # Extract category/tags
            tags = []
            tag_elements = element.find_all('a', class_='discourse-tag') or \
                        element.select_one('.discourse-tag')
            if tag_elements:
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
                if idx + 2 < len(parts):
                    return f"{parts[idx + 1]}/{parts[idx + 2]}"
        except Exception:
            pass
        return None

    def parse_thread_detail(self, html: str, thread_url: str) -> Dict:
        soup = BeautifulSoup(html, 'lxml')
        topic_posts = []
        
        try:
            # find post container
            post_elements = soup.find_all('div', class_='topic-post') or \
                soup.select('.topic-post')
            if not post_elements:
                logger.warning("no post elements found")
                return {'posts': []}

            for idx, post_element in enumerate(post_elements, 1):
                post_data = self._extract_post_info(post_element, idx, thread_url)
                if post_data:
                    topic_posts.append(post_data)
            
        except Exception as e:
            logger.error(f"Error parsing thread detail: {e}")
        
        return {'posts': topic_posts}

    
    
    def _extract_post_info(self, element, idx: int, thread_url: str) -> Optional[Dict]:
        try:
            post_info = {}
            print("element post detail", element)
            post_info['post_id'] = idx
            post_info['url'] = f"{thread_url}/{idx}"

            # extract author
            author_elem = element.find('span', class_='username') or \
                        element.select_one('.username')
            if author_elem:
                post_info['author'] = author_elem.get_text(strip=True)

            # extract user title
            user_title_elem = element.find('span', class_='user-title') or \
                        element.select_one('.user-title')
            if user_title_elem:
                post_info['user_title'] = user_title_elem.get_text(strip=True)
            
            # extract content
            content_elem = element.find('div', class_='post-body') or \
                        element.select_one('.post-body, .post-content')
            if content_elem:
                post_info['content'] = content_elem.get_text(strip=True)

            # extract post date
            post_date_elem = element.find('a', class_='post-date') or \
                        element.select_one('.post-date')
            if post_date_elem:
                post_info['post_date'] = post_date_elem.get_text(strip=True)

            # extract content
            content_elem = element.find('div', class_='cooked') or \
                        element.select_one('.cooked')
            if content_elem:
                post_info['content'] = content_elem.get_text(strip=True)

            # solved by post_id
            accepted_answer_ele = element.find('aside', class_='accepted-answer accepted-answer--has-excerpt')
            if accepted_answer_ele:
                post_info['solved_by_post_id'] = accepted_answer_ele.get('data-post')

            return post_info
            
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

