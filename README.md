# SciVal Search

A Python package to retrieve and analyze data from SciVal using `pybliometrics` and automated `requests` calls with cookie authentication.

## Features

- **RelatedPapers**: Retrieve all publications related to a specific SciVal topic
- **Topic Retrieval**: Find top related topics for a given topic
- **DataFrame Output**: Get results as pandas DataFrames for easy analysis
- **Progress Tracking**: Built-in progress bars for long-running queries

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

### Using the RelatedPapers Class

```python
import os
from dotenv import load_dotenv
from pybliometrics.scival import PublicationLookup, init
from scival_search import RelatedPapers

# Load environment and initialize pybliometrics
load_dotenv()
init()
COOKIE = os.getenv('COOKIE')

# Get topic ID for a publication
pl = PublicationLookup('85068268027')  # Example: pybliometrics paper
topic_id = pl.topic_id

# Create RelatedPapers instance and fetch data
rp = RelatedPapers(topic_id=topic_id, cookie=COOKIE)
df = rp.fetch_papers()

# Access the data
print(f"Retrieved {len(df)} papers")
print(df.head())

# Get metadata
metadata = rp.get_info()
print(f"Year range: {metadata['start_year']} - {metadata['end_year']}")
```

### Using Notebooks

There are example notebooks showcasing the functionality:
- `scival_search/scival_search.ipynb`: Find publications in SciVal of the same topic as a given publication
- `scival_search/scival_topic_retrieval.ipynb`: Find top related topics for a given topic

To use the notebooks:
```bash
poetry run jupyter lab
```

### Examples

Check the `examples/` directory for more usage examples:
```bash
poetry run python examples/related_papers_example.py
```

## API Reference

### RelatedPapers Class

#### `__init__(topic_id: str, cookie: str)`
Initialize a RelatedPapers instance.

**Parameters:**
- `topic_id`: The SciVal topic ID to retrieve papers for
- `cookie`: Authentication cookie for SciVal access

#### `fetch_papers(show_progress: bool = True) -> pd.DataFrame`
Fetch all related papers for the topic ID from SciVal.

**Parameters:**
- `show_progress`: Whether to show a progress bar during fetching

**Returns:**
- DataFrame containing all related papers with their metadata

#### `get_data() -> pd.DataFrame`
Get the DataFrame of related papers. If not yet fetched, calls `fetch_papers()` first.

#### `get_info() -> dict`
Get metadata about the dataset (year range, total publications, etc.).

## License

MIT License - see LICENSE file for details.

