# SciVal Search

A Python package to retrieve and analyze data from SciVal with automated API calls and intelligent caching.

## Features

- **RelatedPapers**: Retrieve all publications related to a specific SciVal topic
- **RelatedTopics**: Get the top 50 related topics for any given topic
- **Smart Caching**: Automatic caching of API responses for faster subsequent access

## Installation

### 1. **Clone the repository**:
```bash
git clone https://github.com/nils-herrmann/scival_search.git
cd scival_search
```

### 2. **Install dependencies**:
If not executed in a venv, poetry will automatically create and manage a virtual environment for you:
```bash
poetry install
```

### 3. **Configure environment variables**:

#### 3.1 Get your SciVal cookie
1. Log into SciVal in your browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Click on any request to scival.com
6. In Network → Headers → Request Headers → Cookie (copy the entire cookie string)

#### 3.2 Set your SciVal cookie
Copy `.env.example` to `.env` and add your SciVal cookie:
```env
COOKIE="your_scival_cookie_here"
```

## Usage

### Quick Example

```python
from dotenv import dotenv_values
from scival_search import RelatedPapers, RelatedTopics

# Load your SciVal cookie from environment
env_vars = dotenv_values()
COOKIE = env_vars['COOKIE']

# Example topic ID
topic_id = "12345"

# Get related papers for a topic
papers = RelatedPapers(topic_id, cookie=COOKIE)
print(f"Found {len(papers.results)} papers")
print(papers.results.head())

# Get related topics
topics = RelatedTopics(topic_id, cookie=COOKIE)
print(f"Found {len(topics.results)} related topics")
print(topics.results.head())
```

### RelatedPapers - Detailed Usage

```python
from scival_search import RelatedPapers

# Fetch papers with progress display
papers = RelatedPapers(
    topic_id="12345",
    cookie=COOKIE,
    show_progress=True,  # Show progress bar
    refresh=False,       # Refresh cache
    cache=True           # Save to cache
)

# Access the results
df = papers.results  # or papers.data
print(f"Retrieved {len(df)} papers")

# Access metadata
print(f"Year range: {papers.info['start_year']} - {papers.info['end_year']}")
print(f"Total publications: {papers.info['total_publications']}")
```

### RelatedTopics - Detailed Usage

```python
from scival_search import RelatedTopics

# Fetch related topics
topics = RelatedTopics(
    topic_id="12345",
    cookie=COOKIE,
    show_progress=True,
    refresh=False,
    cache=True
)

# Access the results (always 50 topics)
df = topics.results  # or topics.data
print(df.head())

# Access metadata
print(f"Entity: {topics.info['entity']}")
print(f"Year range: {topics.info['year_range']}")
```

### Caching Behavior

```python
# First call - fetches from SciVal and caches
papers = RelatedPapers(topic_id, cookie=COOKIE)

# Second call - loads from cache (much faster!)
papers = RelatedPapers(topic_id, cookie=COOKIE)

# Force refresh - ignores cache and fetches fresh data
papers = RelatedPapers(topic_id, cookie=COOKIE, refresh=True)

# Fetch without caching
papers = RelatedPapers(topic_id, cookie=COOKIE, cache=False)
```

## API Reference

### RelatedPapers

Retrieve all publications related to a SciVal topic.

**Parameters:**
- `topic_id` (str): The SciVal topic ID
- `cookie` (str): Authentication cookie for SciVal
- `show_progress` (bool, optional): Show progress bar. Default: `True`
- `refresh` (bool, optional): Refresh cache and fetch new data. Default: `False`
- `cache` (bool, optional): Save fetched data to cache. Default: `True`

**Attributes:**
- `results`: DataFrame of retrieved papers (alias for `data`)
- `data`: DataFrame of retrieved papers
- `info`: Dictionary with metadata (year range, total publications, etc.)

### RelatedTopics

Retrieve the top 50 related topics for a SciVal topic.

**Parameters:**
- `topic_id` (str): The SciVal topic ID
- `cookie` (str): Authentication cookie for SciVal
- `show_progress` (bool, optional): Show progress info. Default: `True`
- `refresh` (bool, optional): Refresh cache and fetch new data. Default: `False`
- `cache` (bool, optional): Save fetched data to cache. Default: `True`

**Attributes:**
- `results`: DataFrame of 50 related topics (alias for `data`)
- `data`: DataFrame of 50 related topics
- `info`: Dictionary with metadata (entity, year range, etc.)

## Cache Location

Cached data is stored in your system's cache directory:
- **macOS**: `~/Library/Caches/scival_search/`
- **Linux**: `~/.cache/scival_search/`
- **Windows**: `%LOCALAPPDATA%\scival_search\Cache\`

Each API call is cached separately by topic ID and page number.

## License

MIT License - see LICENSE file for details.

