# FastMCP — Reverse Engineering Analysis

**Repo**: github.com/PrefectHQ/fastmcp  
**Stars**: 25,326  
**Language**: Python  
**Category**: MCP Server/Client Framework

## Architecture

FastMCP is a Pythonic framework for building MCP (Model Context Protocol) servers and clients. It abstracts the low-level MCP protocol into a clean, Pythonic API.

## Key Design Patterns

1. **Decorator-based tool registration** — `@server.tool()` registers functions as MCP tools
2. **Pydantic validation** — All tool inputs validated via Pydantic models
3. **Async-first** — Built on asyncio, supports both sync and async handlers
4. **Transport abstraction** — Supports stdio, SSE, and HTTP transports
5. **Resource templates** — Dynamic resource generation via URI templates

## What We Can Learn

- Decorator pattern for tool registration is cleaner than JSON config
- Pydantic validation prevents malformed tool calls
- Transport abstraction allows same server to work in multiple contexts
- Resource templates are more flexible than static resources

## Integration Ideas

- Replace our current MCP server setup with FastMCP for Python-based tools
- Use decorator pattern for our fleet health checks
- Leverage Pydantic validation for tool input schemas
