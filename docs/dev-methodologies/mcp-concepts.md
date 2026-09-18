# MCP (Model Context Protocol) — Concepts for Mastery, Not Just Setup

This file is different from the others in this folder: it's not "when to use this practice on this project," it's "understand this concept properly," because MCP is infrastructure you'll keep using well beyond this project. The `connect-confluence-gitlab-mcp.md` guide gives you the commands; this gives you the mental model underneath them.

## What MCP actually is

MCP is an open protocol (originated by Anthropic, now with broad industry adoption) that standardizes how an AI application (the **host**, e.g., Claude Code) connects to external tools and data sources (**servers**, e.g., `mcp-atlassian`). Before MCP, every AI tool needed a bespoke integration per data source (N hosts × M sources = N×M integrations). MCP makes it N+M: any MCP-compliant host can talk to any MCP-compliant server.

Three roles, don't conflate them:
- **Host** — the AI application itself (Claude Code, in this repo's case).
- **Client** — the connector logic inside the host that speaks MCP to a specific server (one client per server connection).
- **Server** — the thing exposing tools/data (e.g., `mcp-atlassian` exposing Confluence search, Jira issue read).

## The primitives a server can expose

- **Tools** — functions the AI can call (e.g., "search Confluence," "create Jira issue"). This is what most MCP servers are used for.
- **Resources** — data the host can read into context (e.g., a specific Confluence page's content), addressed by URI, analogous to a file the AI can open.
- **Prompts** — reusable, server-defined prompt templates the host can surface to the user.

`mcp-atlassian` primarily exposes tools (search/read/create operations); understanding that it's tools, not raw resource access, explains why scoping (`CONFLUENCE_SPACES_FILTER`) matters — you're limiting what the tool call is allowed to search, not what files exist.

## Transports — why this project uses two different ones

- **stdio** — the server runs as a local subprocess, communicating over stdin/stdout. Used for `mcp-atlassian` here because it runs locally and needs your local PAT/environment. Simpler, no network exposure of the server itself.
- **HTTP / SSE (Server-Sent Events)** — the server runs remotely, host connects over HTTP. Used for GitLab's official server and for Atlassian's *Cloud* remote server (not applicable to this project's self-hosted instance, but worth knowing the distinction — see `/v2/mcp` vs. deprecated `/v1/sse` note in the connector guide's history). SSE-based transport is being phased out industry-wide in favor of streamable HTTP as of 2026.

## Authentication models you'll encounter

- **Static token** (PAT, API key) — what `mcp-atlassian` uses for Data Center. Simple, revocable, but you manage rotation yourself.
- **OAuth 2.0/2.1** — what Atlassian Cloud's remote server and GitLab's server use. More setup (admin must register an OAuth app in some cases) but no long-lived static secret to leak.

## Why config-driven client setup matters (the mastery point, not just the practice point)

The `register_atlassian_mcp.py` script in `connectivity/mcp-clients/` isn't just "nicer than typing a long command" — it's an application of the same principle as [Spec-Driven Development](./spec-driven-development.md) and [Context Engineering](./context-engineering.md): connection configuration is *intent that should survive a session boundary*. A command typed once into a terminal is invisible to the next session, the next developer, or a future you. A config file the connection logic reads is discoverable, diffable, and reviewable.

## Do's

- Do understand which primitive (tool/resource/prompt) you're actually using before debugging a connector — "it's not returning data" means something different for a tool-call failure vs. a resource-read failure.
- Do learn the transport your server uses — stdio failures look different from HTTP/OAuth failures, and the guide's troubleshooting only helps if you know which category you're in.
- Do read the actual MCP spec at least once (linked below) rather than only ever interacting with it through `claude mcp add` — the CLI hides real protocol concepts worth having a mental model of.

## Don'ts

- Don't treat "the connector isn't working" as one failure mode — separate transport failure, auth failure, and permission/scope failure (all three look similar from the outside but debug differently).
- Don't assume every MCP server exposes the same primitives — check the server's own docs for what it actually implements before assuming resource-style access when it only offers tools.

## References (for mastery, in rough learning order)

1. [Model Context Protocol — official specification](https://modelcontextprotocol.io/) — start here; read the architecture overview before anything else.
2. [Anthropic: Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — the original announcement and motivation.
3. [MCP: Tools, Resources, and Prompts explained](https://modelcontextprotocol.io/docs/concepts/tools) — the primitives section of the spec docs.
4. [`sooperset/mcp-atlassian` source](https://github.com/sooperset/mcp-atlassian) — read this project's actual server implementation once you're comfortable with the spec, to see the primitives applied concretely.
5. [Anthropic: Claude Code MCP documentation](https://docs.claude.com/en/docs/claude-code/mcp) — how the host (Claude Code) side of the connection is configured and managed.
