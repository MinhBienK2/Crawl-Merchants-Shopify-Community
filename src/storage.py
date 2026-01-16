"""
Data storage module for saving crawled data
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from config.config import OUTPUT_FILE, OUTPUT_FORMAT, DATA_DIR
from src.logger import setup_logger

logger = setup_logger(__name__)


class DataStorage:
    """Handle storage of crawled data"""
    
    def __init__(self, output_file: Optional[Path] = None, output_format: str = "json"):
        """
        Initialize storage
        
        Args:
            output_file: Path to output file (defaults to config setting)
            output_format: Output format ('json' or 'txt')
        """
        self.output_file = output_file or OUTPUT_FILE
        self.output_format = output_format.lower()
        
        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
    
    def save_threads(self, threads: List[Dict], append: bool = False) -> bool:
        """
        Save threads data to file
        
        Args:
            threads: List of thread dictionaries
            append: Whether to append to existing file or overwrite
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.output_format == "json":
                return self._save_json(threads, append)
            elif self.output_format == "txt":
                return self._save_txt(threads, append)
            else:
                logger.error(f"Unsupported output format: {self.output_format}")
                return False
        except Exception as e:
            logger.error(f"Error saving threads: {e}")
            return False
    
    def _save_json(self, threads: List[Dict], append: bool) -> bool:
        """
        Save threads as JSON
        
        Args:
            threads: List of thread dictionaries
            append: Whether to append to existing file
            
        Returns:
            True if successful
        """
        try:
            data = {
                'metadata': {
                    'crawl_date': datetime.now().isoformat(),
                    'total_threads': len(threads),
                    'source': 'Shopify Community'
                },
                'threads': threads
            }
            
            if append and self.output_file.exists():
                # Load existing data
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # Merge threads
                existing_data['threads'].extend(threads)
                existing_data['metadata']['total_threads'] = len(existing_data['threads'])
                existing_data['metadata']['last_update'] = datetime.now().isoformat()
                data = existing_data
            
            # Save to file
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(threads)} threads to {self.output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return False
    
    def _save_txt(self, threads: List[Dict], append: bool) -> bool:
        """
        Save threads as plain text (for LLM analysis)
        
        Args:
            threads: List of thread dictionaries
            append: Whether to append to existing file
            
        Returns:
            True if successful
        """
        try:
            mode = 'a' if append else 'w'
            
            with open(self.output_file.with_suffix('.txt'), mode, encoding='utf-8') as f:
                for thread in threads:
                    f.write("=" * 80 + "\n")
                    f.write(f"THREAD: {thread.get('title', 'Untitled')}\n")
                    f.write(f"URL: {thread.get('url', 'N/A')}\n")
                    f.write(f"Author: {thread.get('author', 'N/A')}\n")
                    f.write(f"Posts: {thread.get('total_posts', len(thread.get('posts', [])))}\n")
                    f.write("-" * 80 + "\n\n")
                    
                    # Write all posts
                    for post in thread.get('posts', []):
                        f.write(f"Post #{post.get('post_number', '?')} by {post.get('author', 'Unknown')}\n")
                        if post.get('timestamp'):
                            f.write(f"Date: {post['timestamp']}\n")
                        f.write("\n")
                        f.write(post.get('content', 'No content') + "\n")
                        f.write("\n" + "-" * 80 + "\n\n")
                    
                    f.write("\n" + "=" * 80 + "\n\n")
            
            logger.info(f"Saved {len(threads)} threads to {self.output_file.with_suffix('.txt')}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving TXT: {e}")
            return False
    
    def load_threads(self) -> Optional[List[Dict]]:
        """
        Load threads from saved file
        
        Returns:
            List of thread dictionaries or None if failed
        """
        try:
            if not self.output_file.exists():
                logger.warning(f"Output file does not exist: {self.output_file}")
                return None
            
            if self.output_format == "json":
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('threads', [])
            else:
                logger.warning("Loading from TXT format not supported")
                return None
                
        except Exception as e:
            logger.error(f"Error loading threads: {e}")
            return None
    
    def export_for_llm(self, output_path: Optional[Path] = None) -> bool:
        """
        Export data in a format optimized for LLM analysis
        
        Args:
            output_path: Path for LLM-optimized output (defaults to data/llm_input.txt)
            
        Returns:
            True if successful
        """
        try:
            threads = self.load_threads()
            if not threads:
                logger.error("No threads to export")
                return False
            
            output_path = output_path or DATA_DIR / "llm_input.txt"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("SHOPIFY COMMUNITY FORUM DATA\n")
                f.write("=" * 80 + "\n\n")
                
                for thread in threads:
                    # Thread header
                    f.write(f"THREAD TITLE: {thread.get('title', 'Untitled')}\n")
                    f.write(f"THREAD URL: {thread.get('url', 'N/A')}\n")
                    f.write(f"THREAD AUTHOR: {thread.get('author', 'N/A')}\n")
                    f.write(f"TOTAL POSTS: {thread.get('total_posts', len(thread.get('posts', [])))}\n")
                    f.write(f"TAGS: {', '.join(thread.get('tags', []))}\n")
                    f.write("\n")
                    
                    # All posts in conversation format
                    for post in thread.get('posts', []):
                        author = post.get('author', 'Unknown')
                        content = post.get('content', 'No content')
                        f.write(f"[{author}]: {content}\n\n")
                    
                    f.write("\n" + "=" * 80 + "\n\n")
            
            logger.info(f"Exported {len(threads)} threads for LLM analysis to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting for LLM: {e}")
            return False

