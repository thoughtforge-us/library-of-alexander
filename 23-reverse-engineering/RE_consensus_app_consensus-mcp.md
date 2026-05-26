# Consensus MCP — Reverse Engineering Analysis

**URL**: https://mcp.consensus.app/mcp  
**Category**: MCP Server / Research Tool  
**Language**: API (HTTP/SSE transport)  
**Database**: 200M+ peer-reviewed research papers

## Architecture

Consensus MCP is a hosted MCP server that provides AI assistants access to 200M+ peer-reviewed research papers. It uses HTTP transport with OAuth authentication.

## Key Design Patterns

1. **OAuth-first authentication** — Automatic browser-based OAuth flow for all clients
2. **Tiered access model** — Free (10 papers/search), Pro (20 papers), Deep (10K searches/month)
3. **Two-tool architecture** — `search` for discovery, `fetch` for full paper details
4. **Academic filtering** — Study type (RCT, meta-analysis), SJR quartile, sample size, human-only, medical mode
5. **Deep Research integration** — ChatGPT Deep Research can call search + fetch automatically

## What We Can Learn

- OAuth-based MCP servers are the future — no API key management needed
- Tiered access with free tier is a great adoption strategy
- Academic filters (study type, SJR, sample size) make searches more useful
- Two-tool pattern (search + fetch) is cleaner than one bloated tool
- Medical mode prioritizes clinical journals — domain-specific optimization

## Integration Ideas

- Add Consensus as an MCP server to our fleet for research validation
- Use it to fact-check our reverse engineering files against published research
- Integrate into our discovery pipeline to validate tool claims against papers
- Use Deep Research mode for comprehensive literature reviews
