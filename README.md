# SciVal Search
This repo uses `pybliometrics` and automated `requests` calls with cookie authentication to retrieve tables from SciVal. There are currently two notebooks showcasing the functionality:
- `scival_publication_retrieval.ipynb`: Find publications in SciVal of the same topic as a given publication.
- `scival_topic_retrieval.ipynb`: Find top related topics for a given topic.

## Installation
### 1. **Clone the repository**:
   ```bash
   git clone https://github.com/nils-herrmann/scival_search.git
   cd scival_search
   ```

### 2. **Install dependencies**:
   ```bash
   poetry install
   ```

### 3. **Configure environment variables**:
#### 3.1 get your SciVal cookie (see below)
1. Log into SciVal in your browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Click on any request to scival.com
6. In Network → Headers → Request Headers → Cookie (copy the entire cookie string)

#### 3.2 set your SciVal cookie
Edit `.env` and add your SciVal cookie:
```env
COOKIE="your_scival_cookie_here"
```

## Usage
Open notebooks and run the cells sequentially
