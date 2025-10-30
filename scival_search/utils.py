import re
import requests
from typing import Literal

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
                page=1):
    """Get SciVal content for a specific topic and page."""
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

    return response.content.decode("utf-8-sig")


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
        elif re.match(r"\d+ publications \(", line):
            numbers = re.findall(r"\d+", line)
            info["total_publications"] = int(numbers[0])
            info["publications_retrieved"] = int(numbers[1])
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
