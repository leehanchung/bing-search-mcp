# Claude Code Memory File

## Commands
- Build: python -m main
- Test: pytest
- Lint: ruff check .
- Typecheck: mypy .

## Project Information
- Building a Bing integration using the Model Context Protocol (MCP)
- This project implements an MCP server that will provide tools, resources, and capabilities to clients
- The MCP architecture allows exposing tools that clients (like Claude) can discover and execute

## Key Concepts
- MCP Server: Implements server-side protocol operations for exposing tools, managing resources, and providing prompt templates
- Transport Layer: Handles communication between clients and servers (using STDIO, SSE, etc.)
- Server Capabilities: Configuration for resources, tools, prompts, and logging support
- Tool Registration: Allows defining and implementing tools that clients can use
- Resource Registration: Manages URI-based resources that clients can access
- Prompt Registration: Handles prompt templates and request processing

## MCP Protocol Primitives
| Primitive | Control               | Description                                         | Example Use                  |
|-----------|-----------------------|-----------------------------------------------------|------------------------------|
| Prompts   | User-controlled       | Interactive templates invoked by user choice        | Slash commands, menu options |
| Resources | Application-controlled| Contextual data managed by the client application   | File contents, API responses |
| Tools     | Model-controlled      | Functions exposed to the LLM to take actions        | API calls, data updates      |

## Server Capabilities
| Capability  | Feature Flag                 | Description                        |
|-------------|------------------------------|------------------------------------|
| `prompts`   | `listChanged`                | Prompt template management         |
| `resources` | `subscribe`<br/>`listChanged`| Resource exposure and updates      |
| `tools`     | `listChanged`                | Tool discovery and execution       |
| `logging`   | -                            | Server logging configuration       |
| `completion`| -                            | Argument completion suggestions    |

## Client Session Flow
- Initialize the connection
- List available prompts, resources, and tools
- Get prompts with arguments
- Read resources by URI
- Call tools with arguments

## Development Notes
- The project uses Python to implement an MCP server that will integrate with Bing search
- Will need to implement proper tool registrations, resource handling, and potentially prompt templates
- Error handling should follow MCP's comprehensive error management approach
- The server will likely use STDIO transport for communication

## Documentation Links
- [Model Context Protocol documentation](https://modelcontextprotocol.io)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)