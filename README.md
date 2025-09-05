# SciVal Search
A notebook and utility functions for finding publications in SciVal of the same topic as a given publication, using
`pybliometrics` and automated `requests` calls with cookie authentication.

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
Open `scival_search.ipynb` and run the cells sequentially
