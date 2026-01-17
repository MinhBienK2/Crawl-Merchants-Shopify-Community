"""
Main script for Shopify Community Crawler
All configuration is loaded from .env file
"""
import sys
from pathlib import Path
from src.crawler import ShopifyCommunityCrawler
from src.storage import DataStorage
from src.logger import setup_logger
from config.config import (
    FULL_URL, MAX_THREADS, MAX_PAGES, LIST_ONLY, EXPORT_LLM,
    OUTPUT_FORMAT, OUTPUT_FILE
)

logger = setup_logger(__name__)


def main():
    """Main entry point for the crawler"""
    try:
        logger.info("=" * 80)
        logger.info("Shopify Community Crawler - Starting")
        logger.info("=" * 80)
        logger.info(f"Target URL: {FULL_URL}")
        logger.info(f"Max threads: {MAX_THREADS or 'Unlimited'}")
        logger.info(f"Max pages: {MAX_PAGES or 'Unlimited'}")
        logger.info(f"List only: {LIST_ONLY}")
        logger.info("=" * 80)
        
        # Initialize crawler
        crawler = ShopifyCommunityCrawler(base_url=FULL_URL)
        
        # Initialize storage
        output_file = Path(OUTPUT_FILE)
        storage = DataStorage(output_file=output_file, output_format=OUTPUT_FORMAT)
        
        # Crawl data
        if LIST_ONLY:
            logger.info("Crawling thread list only...")
            threads = crawler.crawl_thread_list(
                start_url=FULL_URL,
                max_pages=MAX_PAGES
            )
        else:
            logger.info("Crawling full thread content...")
            threads = crawler.crawl_all_threads(
                max_threads=MAX_THREADS,
                max_pages=MAX_PAGES
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
        if EXPORT_LLM:
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

