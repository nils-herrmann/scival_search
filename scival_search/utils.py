import re
import requests
import pickle
from pathlib import Path

from platformdirs import user_cache_dir
from typing import Literal, Optional


BASE_PATH = Path(user_cache_dir('scival_search'))

BASE_URL = "https://www.scival.com"

URLS = {
    "search": f"{BASE_URL}/search/export",
    "related_topics": f"{BASE_URL}/trends/relatedtopics/export"
}

BREAK_KEYWORD = {
    "search": '"Title',
    "related_topics": '"Topics"'
}

def get_content(topic_id: str,
                api: Literal["search", "related_topics"],
                cookie: str,
                page=1,
                refresh: bool = False):
    """Get SciVal content for a specific topic and page.
    
    Args:
        topic_id: The SciVal topic ID
        api: API type ('search' or 'related_topics')
        cookie: Authentication cookie for SciVal access
        page: Page number (default: 1)
        refresh: Whether to refresh the cache and fetch new data (default: False)
        
    Returns:
        Content string from cache or freshly fetched from SciVal
    """
    # Check cache first if not refreshing
    if not refresh:
        cached_content = load_content_cache(api, topic_id, page)
        if cached_content is not None:
            return cached_content
    
    # Fetch fresh content from SciVal
    url = URLS.get(api)
    if not url:
        raise ValueError(f"Invalid API type: {api}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Cookie": cookie,
    }

    topic = f"Topic/{topic_id}"
    params = {
        "uri": topic,
        "exportFileType": "csv",
        "currentPage": page
    }

    response = requests.get(url=url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    assert "attachment" in (response.headers.get("Content-Disposition","").lower())

    content = response.content.decode("utf-8-sig")
    
    # Save to cache
    save_content_cache(api, topic_id, page, content)
    
    return content


def split_lines(text, api: Literal["search", "related_topics"]):
    """Split SciVal response into intro lines and table text."""
    # Get keyword to split intro and table
    break_keyword = BREAK_KEYWORD.get(api, '"Title"')
    if not break_keyword:
        raise ValueError(f"Invalid API type: {api}")

    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.startswith(break_keyword):
            start = i
            break

    intro_lines = lines[:start]
    table_text = "\n".join(lines[start:])

    return intro_lines, table_text


def parse_search_info(intro_lines):
    """Parse introductory lines from SciVal CSV export."""
    info = {}
    for line in intro_lines:
        if line.startswith("Data set,"):
            info["data_set"] = line.split(",", 1)[1].strip('"')
        elif line.startswith("Year range,"):
            years = re.findall(r"\d{4}", line)
            info["start_year"] = int(years[0])
            info["end_year"] = int(years[1])
        elif re.match(r"^\d+ publications", line):
            # Matches both:
            # "513 publications" (when < 1000 results)
            # "3952 publications (first 1000 publications exported)" (when >= 1000 results)
            numbers = re.findall(r"\d+", line)
            info["total_publications"] = int(numbers[0])
            # If there's a second number in parentheses, use it; otherwise use total
            if len(numbers) >= 2:
                info["publications_retrieved"] = int(numbers[1])
            else:
                # When all publications fit on one export (< 1000)
                info["publications_retrieved"] = int(numbers[0])
    return info


def parse_related_topics_info(intro_lines):
    """Parse introductory lines from SciVal related topics CSV export."""
    info = {}
    for line in intro_lines:
        if line.startswith("Data set,"):
            info["data_set"] = re.findall(r'Data set,?""(.*)""', line)[0]
        elif line.startswith("Entity,"):
            info["entity"] = re.findall(r'Entity,?"(.*)"', line)[0]
        elif line.startswith("Year range,"):
            info["year_range"] = re.findall(r'Year range,?(.*)', line)[0]
    return info


def get_cache_path(api: str, topic_id: str, page: int = 1) -> Path:
    """Get the cache file path for a specific API endpoint, topic ID, and page.
    
    Args:
        api: API type ('search' or 'related_topics')
        topic_id: The SciVal topic ID
        page: The page number (default: 1)
        
    Returns:
        Path object pointing to the cache file
    """
    cache_dir = BASE_PATH / api
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{topic_id}_page{page}.pkl"


def save_content_cache(api: str, topic_id: str, page: int, content: str) -> None:
    """Save content to cache.
    
    Args:
        api: API type ('search' or 'related_topics')
        topic_id: The SciVal topic ID
        page: The page number
        content: The raw content string to cache
    """
    cache_path = get_cache_path(api, topic_id, page)
    with open(cache_path, 'wb') as f:
        pickle.dump(content, f)


def load_content_cache(api: str, topic_id: str, page: int) -> Optional[str]:
    """Load content from cache if available.
    
    Args:
        api: API type ('search' or 'related_topics')
        topic_id: The SciVal topic ID
        page: The page number
        
    Returns:
        Cached content string if cache exists, None otherwise
    """
    cache_path = get_cache_path(api, topic_id, page)
    if cache_path.exists():
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    return None

