"""RelatedPapers class for retrieving related papers from SciVal."""

from io import StringIO
from math import ceil
from typing import Optional

import pandas as pd
from tqdm import tqdm

from scival_search.utils import get_content, parse_search_info, split_lines


class RelatedPapers:
    """
    A class to retrieve and manage related papers from SciVal for a given topic ID.
    
    Attributes:
        topic_id (str): The SciVal topic ID to search for.
        cookie (str): Authentication cookie for SciVal access.
        data (pd.DataFrame): DataFrame containing the retrieved papers.
        info (dict): Metadata about the dataset (year range, total publications, etc.).
        results (pd.DataFrame): DataFrame containing the retrieved papers (alias for data).
    """
    
    def __init__(self, topic_id: str, cookie: str, show_progress: bool = True):
        """
        Initialize the RelatedPapers instance and automatically fetch papers.
        
        Args:
            topic_id: The SciVal topic ID to retrieve papers for.
            cookie: Authentication cookie for SciVal access.
            show_progress: Whether to show a progress bar during fetching.
        """
        self.topic_id = topic_id
        self.cookie = cookie
        self.data: Optional[pd.DataFrame] = None
        self.info: Optional[dict] = None
        
        # Automatically fetch papers on initialization
        self.results = self.fetch_papers(show_progress=show_progress)


    def fetch_papers(self, show_progress: bool = True) -> pd.DataFrame:
        """
        Fetch all related papers for the topic ID from SciVal.
        
        Args:
            show_progress: Whether to show a progress bar during fetching.
            
        Returns:
            DataFrame containing all related papers with their metadata.
            
        Raises:
            AssertionError: If the number of retrieved papers doesn't match expected count.
        """
        # Get first page content
        res_text = get_content(self.topic_id, api="search", cookie=self.cookie, page=1)
        
        # Split the response into intro and table data
        intro_lines, table_text = split_lines(res_text, api="search")
        
        # Parse metadata
        self.info = parse_search_info(intro_lines)
        n = self.info['total_publications']
        retrieved = self.info['publications_retrieved']
        num_pages = ceil(n / retrieved)
        
        if show_progress:
            print(f"Data for topic ID {self.topic_id}: {self.info.get('data_set', 'N/A')}")
            print(f"Year range: {self.info.get('start_year', 'N/A')} - {self.info.get('end_year', 'N/A')}")
            print(f"Total publications: {n}")
            print(f"Retrieved per page: {retrieved}")
            print(f"Total pages: {num_pages}")
        
        # Initialize list to store all table data
        # Exclude last two summary lines from first page
        all_table_lines = table_text.splitlines()[:-2]
        
        # Fetch remaining pages if there are more than 1 page
        if num_pages > 1:
            pages_to_fetch = range(2, num_pages + 1)
            iterator = tqdm(pages_to_fetch, desc="Fetching pages") if show_progress else pages_to_fetch
            
            for page in iterator:
                text = get_content(self.topic_id, api="search", cookie=self.cookie, page=page)
                
                _, page_table_text = split_lines(text, api="search")
                # Exclude header and last two summary lines
                table_lines = page_table_text.splitlines()[1:-2]
                
                all_table_lines.extend(table_lines)
        
        # Create DataFrame from complete dataset
        self.data = pd.read_csv(StringIO("\n".join(all_table_lines)))
        
        # Verify we got all the papers
        assert self.data.shape[0] == n, f"Expected {n} rows, got {self.data.shape[0]}"
        
        return self.data
    
    def __repr__(self) -> str:
        """String representation of the RelatedPapers instance."""
        if self.data is not None:
            return f"RelatedPapers(topic_id={self.topic_id}, papers={len(self.data)})"
        return f"RelatedPapers(topic_id={self.topic_id}, papers=not_fetched)"
