import requests
from dotenv import load_dotenv
from typing import Optional
from brave_ai import BraveAIWrapper
import os

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
YOU_COM_API_KEY = os.getenv("YOU_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PPLX_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_AI_API_KEY")

def query_you_com(query):
    headers = {"X-API-Key": YOU_COM_API_KEY}
    params = {"query": query}
    try:
        response = requests.get(
            "https://api.ydc-index.io/rag",  # Verify the correctness of the API endpoint
            params=params,
            headers=headers,
        )
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        resp = response.json()
        return resp["answer"]
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"


def query_tavily(query):
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "include_images": False,
        "include_raw_content": False,
        "max_results": 1,
        "include_domains": [],
        "exclude_domains": [],
    }
    response = requests.post("https://api.tavily.com/search", json=payload)
    if response.status_code == 200:
        resp = response.json()
        return resp["answer"]
    else:
        return f"Request failed with status code: {response.status_code}"


def query_perplexity(query):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    }
    data = {
        "model": "llama-3-sonar-large-32k-online",
        "stream": False,
        "max_tokens": 1024,
        "frequency_penalty": 1,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": "Be precise and concise in your responses."},
            {"role": "user", "content": query},
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Request failed with status code: {response.status_code}"


def ProcessQuestion(question, model):
    if model == "You.com":
        return query_you_com(question)
    elif model == "Tavily.com":
        return query_tavily(question)
    elif model == "Perplexity.ai":
        return query_perplexity(question)
    elif model == "Brave.com":
        return query_brave(question)
    else:
        return "Model not supported"


def query_brave(query: str) -> Optional[str]:
    """
    Get a summary for the given query using BraveAIWrapper.

    Args:
        query (str): The search query.
        api_key (str): The API key for Brave Search.

    Returns:
        Optional[str]: Summarized result or None if an error occurs.
    """
    brave_ai = BraveAIWrapper(api_key=BRAVE_API_KEY)
    summary = brave_ai.get_and_summarize(query)
    return summary