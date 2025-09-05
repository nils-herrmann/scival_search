import re
import requests

BASE_URL = "https://www.scival.com/search/export"

def get_content(topic_id, cookie, page=1):
    """Get SciVal content for a specific topic and page."""

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

    response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    assert "attachment" in (response.headers.get("Content-Disposition","").lower())

    return response.content.decode("utf-8-sig")


def split_lines(text):
    """Split SciVal response into intro lines and table text."""
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.startswith('"Title"'):
            start = i
            break

    intro_lines = lines[:start]
    table_text = "\n".join(lines[start:])

    return intro_lines, table_text


def parse_scival_info(intro_lines):
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
