# Bing Search MCP Server

A Model Context Protocol (MCP) server for Microsoft Bing Search API integration, allowing AI assistants to perform web, news, and image searches.

[![smithery badge](https://smithery.ai/badge/@leehanchung/bing-search-mcp)](https://smithery.ai/server/@leehanchung/bing-search-mcp)

![Bing Search MCP Server](assets/mcp_server_bing.png)


## Features

- Web search for general information
- News search for recent events and timely information
- Image search for visual content
- Rate limiting to prevent API abuse
- Comprehensive error handling

## Requirements

- Python 3.10 or higher
- Microsoft Bing Search API key
- MCP-compatible client (e.g., Claude Desktop, Cursor)

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

## Configuration

Set the required environment variables:

```bash
export BING_API_KEY="your-bing-api-key"
export BING_API_URL="https://api.bing.microsoft.com/"  # Optional
```

For Windows:
```cmd
set BING_API_KEY=your-bing-api-key
set BING_API_URL=https://api.bing.microsoft.com/
```

## Usage

### Running the server

```
uvx bing-search-mcp
```

### Configuring with Claude for Desktop

Add the following to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "bing-search": {
      "command": "uvx",
      "args": [
        "/path/to/your/bing-search-mcp"
      ],
      "env": {
        "BING_API_KEY": "your-bing-api-key"
      }
    }
  }
}
```
![Claude Code Bing Search MCP](assets/claude_bing_search.png)

## Available Tools

### 1. bing_web_search
General web search for information, websites, and content.

```python
bing_web_search(query: str, count: int = 10, offset: int = 0, market: str = "en-US")
```

### 2. bing_news_search
Search for news articles and current events.

```python
bing_news_search(query: str, count: int = 10, market: str = "en-US", freshness: str = "Day")
```

### 3. bing_image_search
Search for images.

```python
bing_image_search(query: str, count: int = 10, market: str = "en-US")
```

## Getting a Bing API Key

1. Visit [Microsoft Azure Portal](https://portal.azure.com/)
2. Create or sign in to your Azure account
3. Create a new Bing Search resource
4. Go to the resource and find your API key in the "Keys and Endpoint" section

## License

[MIT License](LICENSE)
