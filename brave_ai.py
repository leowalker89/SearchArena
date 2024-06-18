import json
import requests
from typing import List, Optional
# from langchain_community.document_transformers import MarkdownifyTransformer
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field

class BraveAIWrapper(BaseModel):
    api_key: str = Field(..., description="API key for Brave Search")
    base_search_url: str = Field("https://api.search.brave.com/res/v1/web/search", const=True)
    base_summarize_url: str = Field("https://api.search.brave.com/res/v1/summarizer/search", const=True)
    headers: dict = Field(default_factory=dict, description="HTTP headers for API requests")

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
        }

    def get_brave_results(self, query: str, count: int = 3, safe_search: str = 'off') -> Optional[dict]:
        """
        Get search results from Brave Search.

        Args:
            query (str): The search query.
            count (int): Number of results to return.
            safe_search (str): Safe search filter (off, moderate, strict).

        Returns:
            Optional[dict]: JSON response from Brave Search API or None if an error occurs.
        """
        params = {
            "q": query,
            "count": count,
            "summary": True,
            "safe_search": safe_search,
            "extra_snippets": True,
        }
        try:
            response = requests.get(self.base_search_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def summarize_results(self, summarizer_key: str) -> Optional[dict]:
        """
        Summarize search results using Brave Summarizer.

        Args:
            summarizer_key (str): The key for the summarizer.

        Returns:
            Optional[dict]: JSON response from Brave Summarizer API or None if an error occurs.
        """
        params = {"key": summarizer_key}
        try:
            response = requests.get(self.base_summarize_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_and_summarize(self, query: str, count: int = 3, safe_search: str = 'off') -> Optional[str]:
        """
        Get and summarize search results from Brave Search.

        Args:
            query (str): The search query.
            count (int): Number of results to return.
            safe_search (str): Safe search filter (off, moderate, strict).

        Returns:
            Optional[str]: Summarized result or None if an error occurs.
        """
        results = self.get_brave_results(query, count, safe_search)
        if results and 'summarizer' in results:
            summarizer_key = results['summarizer']['key']
            summary = self.summarize_results(summarizer_key)
            if summary and 'summary' in summary and len(summary['summary']) > 0:
                return summary['summary'][0]['data']
        return None
