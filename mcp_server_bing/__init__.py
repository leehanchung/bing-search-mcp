from . import server
import asyncio

def main():
    """Initialize and run the MCP server."""

    # Check for required environment variables
    if "BING_API_KEY" not in os.environ:
        print(
            "Error: BING_API_KEY environment variable is required",
            file=sys.stderr,
        )
        print(
            "Get a Bing API key from: "
            "https://www.microsoft.com/en-us/bing/apis/bing-web-search-api",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Starting Bing Search MCP server...", file=sys.stderr)
    # Run server synchronously even within async main
    asyncio.run(server.run(transport="stdio"))


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())


__all__ = ["main", "server"]
