"""RelatedTopics class for retrieving related topics from SciVal."""

from io import StringIO
from typing import Optional

import pandas as pd

from scival_search.utils import get_content, parse_related_topics_info, split_lines


class RelatedTopics:
    """
    A class to retrieve and manage related topics from SciVal for a given topic ID.
    
    Attributes:
        topic_id (str): The SciVal topic ID to search for.
        cookie (str): Authentication cookie for SciVal access.
        data (pd.DataFrame): DataFrame containing the retrieved related topics.
        info (dict): Metadata about the dataset (data set, entity, year range).
        results (pd.DataFrame): DataFrame containing the retrieved topics (alias for data).
    """
    
    def __init__(self, topic_id: str, cookie: str, show_progress: bool = True):
        """
        Initialize the RelatedTopics instance and automatically fetch related topics.
        
        Args:
            topic_id: The SciVal topic ID to retrieve related topics for.
            cookie: Authentication cookie for SciVal access.
            show_progress: Whether to show progress information during fetching.
        """
        self.topic_id = topic_id
        self.cookie = cookie
        self.data: Optional[pd.DataFrame] = None
        self.info: Optional[dict] = None
        
        # Automatically fetch related topics on initialization
        self.results = self.fetch_topics(show_progress=show_progress)

    def fetch_topics(self, show_progress: bool = True) -> pd.DataFrame:
        """
        Fetch all related topics for the topic ID from SciVal.
        
        Args:
            show_progress: Whether to show progress information during fetching.
            
        Returns:
            DataFrame containing all related topics with their metadata.
            
        Raises:
            AssertionError: If the number of retrieved topics doesn't match expected count.
        """
        # Get content from SciVal (related topics are always on one page - 50 topics)
        res_text = get_content(self.topic_id, api="related_topics", cookie=self.cookie, page=1)
        
        # Split the response into intro and table data
        intro_lines, table_text = split_lines(res_text, api="related_topics")
        
        # Parse metadata
        self.info = parse_related_topics_info(intro_lines)
        
        if show_progress:
            print(f"Data for topic ID {self.topic_id}: {self.info.get('data_set', 'N/A')}")
            print(f"Entity: {self.info.get('entity', 'N/A')}")
            print(f"Year range: {self.info.get('year_range', 'N/A')}")
        
        # There are always 50 related topics
        n = 50
        # The table has 3 footer lines to exclude
        all_table_lines = table_text.splitlines()[:-3]
        
        # Create DataFrame from table data
        self.data = pd.read_csv(StringIO("\n".join(all_table_lines)))
        
        # Verify we got all the topics
        assert self.data.shape[0] == n, f"Expected {n} rows, got {self.data.shape[0]}"
        
        return self.data
    
    def __repr__(self) -> str:
        """String representation of the RelatedTopics instance."""
        if self.data is not None:
            return f"RelatedTopics(topic_id={self.topic_id}, topics={len(self.data)})"
        return f"RelatedTopics(topic_id={self.topic_id}, topics=not_fetched)"
