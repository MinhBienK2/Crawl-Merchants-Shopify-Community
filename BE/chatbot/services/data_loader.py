"""Service for loading and querying Shopify community data."""
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.conf import settings


class DataLoader:
    """Service to load and query Shopify community threads data."""

    def __init__(self, data_path: Optional[Path] = None):
        """Initialize data loader."""
        self.data_path = data_path or settings.DATA_PATH
        self._data: Optional[Dict[str, Any]] = None

    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        if self._data is None:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        return self._data

    def get_all_threads(self) -> List[Dict[str, Any]]:
        """Get all threads from the data."""
        data = self.load_data()
        return data.get("threads", [])

    def search_threads(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search threads by title or content."""
        threads = self.get_all_threads()
        query_lower = query.lower()

        results = []
        for thread in threads:
            title = thread.get("title", "").lower()
            # Check if query matches title
            if query_lower in title:
                results.append(thread)
            else:
                # Check posts content
                for post in thread.get("posts", []):
                    content = post.get("content", "").lower()
                    if query_lower in content:
                        results.append(thread)
                        break

            if len(results) >= limit:
                break

        return results

    def get_thread_by_id(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get thread by ID."""
        threads = self.get_all_threads()
        for thread in threads:
            if thread.get("thread_id") == str(thread_id):
                return thread
        return None

    def get_context_for_llm(self, query: str, max_threads: int = 3) -> str:
        """Get relevant context from threads for LLM."""
        relevant_threads = self.search_threads(query, limit=max_threads)

        if not relevant_threads:
            # Return summary if no matches
            data = self.load_data()
            return f"Total threads available: {data.get('metadata', {}).get('total_threads', 0)}"

        context_parts = []
        for thread in relevant_threads:
            title = thread.get("title", "")
            thread_id = thread.get("thread_id", "")
            url = thread.get("url", "")
            posts = thread.get("posts", [])[:3]  # Limit to first 3 posts

            context_parts.append(f"Thread: {title}")
            context_parts.append(f"ID: {thread_id}")
            context_parts.append(f"URL: {url}")

            for post in posts:
                author = post.get("author", "")
                content = post.get("content", "")
                # Remove HTML tags for cleaner context
                content_text = re.sub("<[^<]+?>", "", content)
                context_parts.append(f"  - {author}: {content_text[:500]}...")

            context_parts.append("")

        return "\n".join(context_parts)


# Global instance
data_loader = DataLoader()
