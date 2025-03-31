import asyncio  # Add asyncio import
import os
import sys
import time

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()


# Initialize FastMCP server
server = FastMCP(
    "bing-search",
    prompt="""
# Bing Search MCP Server

This server provides tools for searching the web using Microsoft Bing's API.
It allows you to search for web pages, news articles, and images.

## Available Tools

### 1. bing_web_search
Use this tool for general web searches. Best for finding information,
websites, articles, and general content.

Example: "What is the capital of France?" or
"recipe for chocolate chip cookies"

### 2. bing_news_search
Use this tool specifically for news-related queries. Best for current
events, recent developments, and timely information.

Example: "latest news on climate change" or
"recent technology announcements"

### 3. bing_image_search
Use this tool for finding images. Best for visual content queries.

Example: "pictures of golden retrievers" or "Eiffel Tower images"

## Guidelines for Use

- Always check if a query would be better served by web, news, or image search
- For current events and recent developments, prefer news search
- For visual content, use image search
- Keep queries concise and specific for best results
- Rate limits apply to all searches (typically 1 request/second)

## Output Format

All search results will be formatted as text with clear sections for each
result item, including:

- Web search: Title, URL, and Description
- News search: Title, URL, Description, Published date, and Provider
- Image search: Title, Source URL, Image URL, and Size

If the API key is missing or invalid, appropriate error messages will be
returned.
""",
)

# Constants
BING_API_URL = os.environ.get(
    "BING_API_URL", "https://api.bing.microsoft.com/"
)
USER_AGENT = "mcp-bing-search/1.0"

# Rate limiting
RATE_LIMIT = {"per_second": 1, "per_month": 15000}

request_count = {"second": 0, "month": 0, "last_reset": time.time()}


def check_rate_limit():
    """Check if we're within rate limits"""
    now = time.time()
    if now - request_count["last_reset"] > 1:
        request_count["second"] = 0
        request_count["last_reset"] = now

    if (
        request_count["second"] >= RATE_LIMIT["per_second"]
        or request_count["month"] >= RATE_LIMIT["per_month"]
    ):
        raise Exception("Rate limit exceeded")

    request_count["second"] += 1
    request_count["month"] += 1


@server.tool()
async def bing_web_search(
    query: str, count: int = 10, offset: int = 0, market: str = "en-US"
) -> str:
    """Performs a web search using the Bing Search API for general information
    and websites.

    Args:
        query: Search query (required)
        count: Number of results (1-50, default 10)
        offset: Pagination offset (default 0)
        market: Market code like en-US, en-GB, etc.
    """
    # Get API key from environment
    api_key = os.environ.get("BING_API_KEY", "")

    if not api_key:
        return (
            "Error: Bing API key is not configured. Please set the "
            "BING_API_KEY environment variable."
        )

    try:
        check_rate_limit()

        headers = {
            "User-Agent": USER_AGENT,
            "Ocp-Apim-Subscription-Key": api_key,
            "Accept": "application/json",
        }

        params = {
            "q": query,
            "count": min(count, 50),  # Bing limits to 50 results max
            "offset": offset,
            "mkt": market,
            "responseFilter": "Webpages",
        }

        search_url = f"{BING_API_URL}v7.0/search"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                search_url, headers=headers, params=params, timeout=10.0
            )

            response.raise_for_status()
            data = response.json()

            if "webPages" not in data:
                return "No results found."

            results = []
            for result in data["webPages"]["value"]:
                results.append(
                    f"Title: {result['name']}\n"
                    f"URL: {result['url']}\n"
                    f"Description: {result['snippet']}"
                )

            return "\n\n".join(results)

    except httpx.HTTPError as e:
        return f"Error communicating with Bing API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@server.tool()
async def bing_news_search(
    query: str, count: int = 10, market: str = "en-US", freshness: str = "Day"
) -> str:
    """Searches for news articles using Bing News Search API for current
    events and timely information.

    Args:
        query: News search query (required)
        count: Number of results (1-50, default 10)
        market: Market code like en-US, en-GB, etc.
        freshness: Time period of news (Day, Week, Month)
    """
    # Get API key from environment
    api_key = os.environ.get("BING_API_KEY", "")

    if not api_key:
        return (
            "Error: Bing API key is not configured. Please set the "
            "BING_API_KEY environment variable."
        )

    try:
        check_rate_limit()

        # News search has a different endpoint
        news_url = f"{BING_API_URL}v7.0/news/search"

        headers = {
            "User-Agent": USER_AGENT,
            "Ocp-Apim-Subscription-Key": api_key,
            "Accept": "application/json",
        }

        params = {
            "q": query,
            "count": min(count, 50),
            "mkt": market,
            "freshness": freshness,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                news_url, headers=headers, params=params, timeout=10.0
            )

            response.raise_for_status()
            data = response.json()

            if "value" not in data:
                return "No news results found."

            results = []
            for result in data["value"]:
                published_date = result.get("datePublished", "Unknown date")
                provider_info = result.get("provider", [{"name": "Unknown"}])
                # Handle potential empty provider list
                provider_name = (
                    provider_info[0]["name"] if provider_info else "Unknown"
                )
                results.append(
                    f"Title: {result['name']}\n"
                    f"URL: {result['url']}\n"
                    f"Description: {result['description']}\n"
                    f"Published: {published_date}\n"
                    f"Provider: {provider_name}"
                )

            return "\n\n".join(results)

    except httpx.HTTPError as e:
        return f"Error communicating with Bing API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@server.tool()
async def bing_image_search(
    query: str, count: int = 10, market: str = "en-US"
) -> str:
    """Searches for images using Bing Image Search API for visual content.

    Args:
        query: Image search query (required)
        count: Number of results (1-50, default 10)
        market: Market code like en-US, en-GB, etc.
    """
    # Get API key from environment
    api_key = os.environ.get("BING_API_KEY", "")

    if not api_key:
        return (
            "Error: Bing API key is not configured. Please set the "
            "BING_API_KEY environment variable."
        )

    try:
        check_rate_limit()

        # Image search has a different endpoint
        image_url = f"{BING_API_URL}v7.0/images/search"

        headers = {
            "User-Agent": USER_AGENT,
            "Ocp-Apim-Subscription-Key": api_key,
            "Accept": "application/json",
        }

        params = {"q": query, "count": min(count, 50), "mkt": market}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                image_url, headers=headers, params=params, timeout=10.0
            )

            response.raise_for_status()
            data = response.json()

            if "value" not in data:
                return "No image results found."

            results = []
            for result in data["value"]:
                results.append(
                    f"Title: {result['name']}\n"
                    f"Source URL: {result['hostPageUrl']}\n"
                    f"Image URL: {result['contentUrl']}\n"
                    f"Size: {result.get('width', 'Unknown')}x"
                    f"{result.get('height', 'Unknown')}"
                )

            return "\n\n".join(results)

    except httpx.HTTPError as e:
        return f"Error communicating with Bing API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
