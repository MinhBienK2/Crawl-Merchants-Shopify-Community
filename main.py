"""
Main script for Shopify Community Crawler
"""
import argparse
import sys
from pathlib import Path
from src.crawler import ShopifyCommunityCrawler
from src.storage import DataStorage
from src.logger import setup_logger
from config.config import FULL_URL

logger = setup_logger(__name__)


def main():
    """Main entry point for the crawler"""
    parser = argparse.ArgumentParser(
        description='Crawl Shopify Community forum threads',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Crawl all threads (default)
  python main.py
  
  # Crawl maximum 50 threads
  python main.py --max-threads 50
  
  # Crawl only first 3 pages of thread list
  python main.py --max-pages 3
  
  # Specify custom output file
  python main.py --output data/custom_output.json
  
  # Export for LLM after crawling
  python main.py --export-llm
        """
    )
    
    parser.add_argument(
        '--url',
        type=str,
        default=FULL_URL,
        help=f'URL to start crawling from (default: {FULL_URL})'
    )
    
    parser.add_argument(
        '--max-threads',
        type=int,
        default=None,
        help='Maximum number of threads to crawl (default: all)'
    )
    
    parser.add_argument(
        '--max-pages',
        type=int,
        default=None,
        help='Maximum number of list pages to crawl (default: all)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file path (default: data/shopify_community_threads.json)'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'txt'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--export-llm',
        action='store_true',
        help='Export data in LLM-optimized format after crawling'
    )
    
    parser.add_argument(
        '--list-only',
        action='store_true',
        help='Only crawl thread list, not full thread content'
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("=" * 80)
        logger.info("Shopify Community Crawler - Starting")
        logger.info("=" * 80)
        
        # Initialize crawler
        crawler = ShopifyCommunityCrawler(base_url=args.url)
        
        # Initialize storage
        output_file = Path(args.output) if args.output else None
        storage = DataStorage(output_file=output_file, output_format=args.format)
        
        # Crawl data
        if args.list_only:
            logger.info("Crawling thread list only...")
            threads = crawler.crawl_thread_list(
                start_url=args.url,
                max_pages=args.max_pages
            )
        else:
            logger.info("Crawling full thread content...")
            threads = crawler.crawl_all_threads(
                max_threads=args.max_threads,
                max_pages=args.max_pages
            )
        
        if not threads:
            logger.warning("No threads were crawled. Exiting.")
            return 1
        
        # Save data
        logger.info(f"Saving {len(threads)} threads...")
        success = storage.save_threads(threads)
        
        if not success:
            logger.error("Failed to save threads")
            return 1
        
        # Export for LLM if requested
        if args.export_llm:
            logger.info("Exporting data for LLM analysis...")
            storage.export_for_llm()
        
        logger.info("=" * 80)
        logger.info("Crawling completed successfully!")
        logger.info(f"Total threads: {len(threads)}")
        logger.info(f"Output file: {storage.output_file}")
        logger.info("=" * 80)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nCrawling interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

