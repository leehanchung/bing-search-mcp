#!/usr/bin/env python3
"""
Bing Search MCP Server
A Model Context Protocol server that provides access to Bing Search API.

Environment variables:
- BING_API_KEY: Your Bing Search API key
- BING_API_URL: (Optional) Base URL for Bing API endpoints
"""

import os
import sys

from bing_search_mcp.server import server


def main():
    """Run the Bing Search MCP server"""

    # Check for required environment variables
    if "BING_API_KEY" not in os.environ:
        print(
            "Error: BING_API_KEY environment variable is required",
            file=sys.stderr,
        )
        print(
            "Get a Bing API key from: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api",
            file=sys.stderr,
        )
        sys.exit(1)

    # Start the MCP server
    print("Starting Bing Search MCP server...", file=sys.stderr)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
