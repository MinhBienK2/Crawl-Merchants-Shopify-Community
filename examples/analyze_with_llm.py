"""
Example script: Analyze crawled data with LLM
This is a template showing how to use the crawled data with LLM APIs
"""
import json
from pathlib import Path
from typing import List, Dict

# Example: Using OpenAI API
# Uncomment and install openai: pip install openai
# from openai import OpenAI


def load_crawled_data(data_file: Path) -> Dict:
    """
    Load crawled data from JSON file
    
    Args:
        data_file: Path to JSON file
        
    Returns:
        Dictionary containing threads data
    """
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def prepare_thread_for_llm(thread: Dict) -> str:
    """
    Format a thread into a prompt for LLM analysis
    
    Args:
        thread: Thread dictionary
        
    Returns:
        Formatted string for LLM
    """
    prompt = f"""
THREAD ANALYSIS REQUEST
======================

Thread Title: {thread.get('title', 'N/A')}
Thread URL: {thread.get('url', 'N/A')}
Author: {thread.get('author', 'N/A')}
Total Posts: {thread.get('total_posts', 0)}
Tags: {', '.join(thread.get('tags', []))}

CONVERSATION:
"""
    
    for post in thread.get('posts', []):
        author = post.get('author', 'Unknown')
        content = post.get('content', '')
        prompt += f"\n[{author}]:\n{content}\n"
    
    prompt += "\n\nPlease analyze this thread and provide insights."
    
    return prompt


def analyze_thread_with_llm(thread: Dict, api_key: str = None) -> str:
    """
    Analyze a single thread using LLM API
    
    Args:
        thread: Thread dictionary
        api_key: API key for LLM service
        
    Returns:
        Analysis result from LLM
    """
    prompt = prepare_thread_for_llm(thread)
    
    # Example using OpenAI (uncomment and configure)
    # client = OpenAI(api_key=api_key)
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are an expert analyst for e-commerce community discussions."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message.content
    
    # Placeholder return
    return f"Analysis for thread: {thread.get('title', 'N/A')}"


def batch_analyze_threads(threads: List[Dict], api_key: str = None) -> List[Dict]:
    """
    Analyze multiple threads in batch
    
    Args:
        threads: List of thread dictionaries
        api_key: API key for LLM service
        
    Returns:
        List of analysis results
    """
    results = []
    
    for idx, thread in enumerate(threads, 1):
        print(f"Analyzing thread {idx}/{len(threads)}: {thread.get('title', 'N/A')[:50]}...")
        
        analysis = analyze_thread_with_llm(thread, api_key)
        
        results.append({
            'thread_id': thread.get('thread_id'),
            'thread_title': thread.get('title'),
            'thread_url': thread.get('url'),
            'analysis': analysis
        })
    
    return results


def main():
    """Example main function"""
    # Load data
    data_file = Path("data/shopify_community_threads.json")
    
    if not data_file.exists():
        print(f"Data file not found: {data_file}")
        print("Please run the crawler first: python main.py")
        return
    
    print("Loading crawled data...")
    data = load_crawled_data(data_file)
    threads = data.get('threads', [])
    
    print(f"Loaded {len(threads)} threads")
    
    # Example: Analyze first 5 threads
    sample_threads = threads[:5]
    
    print("\nAnalyzing threads with LLM...")
    # Uncomment when you have API key configured
    # api_key = "your-api-key-here"
    # results = batch_analyze_threads(sample_threads, api_key)
    
    # Save results
    # output_file = Path("data/llm_analysis.json")
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\nExample script completed!")
    print("Please configure your LLM API key and uncomment the analysis code.")


if __name__ == "__main__":
    main()

