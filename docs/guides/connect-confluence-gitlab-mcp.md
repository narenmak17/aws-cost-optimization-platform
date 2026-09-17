# Connecting Confluence and GitLab via MCP

You mentioned you just got a company license today and want to connect Claude Code to your company's Confluence (for the existing PPT/backlog pages) and GitLab (for company repos). This is a real, supported path — both Atlassian and GitLab ship official MCP servers. Below is what's verified as of this session (2026-09-17); MCP connector setup details change, so re-check the linked docs if something doesn't match what you see.

**None of this has been run yet.** This is a guide to follow yourself, since it requires your own company OAuth login — I cannot complete that browser-based approval step for you.

---

## 1. Confluence (and Jira, Bitbucket, Compass) — Atlassian's official remote MCP server

Atlassian's remote MCP server is officially GA and lists Claude as a launch partner. It respects your existing Confluence permissions — the agent only sees what you can already see.

### Setup

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp
```

Then, inside a Claude Code session, run:

```
/mcp
```

This triggers a browser-based OAuth 2.1 consent screen. Log in with your company Atlassian account and approve. After that, the connection is live for this machine.

### Important: use `/v2/mcp`, not `/v1/sse`

Older guides reference `https://mcp.atlassian.com/v1/sse`. The `/sse` transport is being deprecated (legacy SSE endpoint loses support after 30 June 2026 per Atlassian's own docs) — use the `/v2/mcp` HTTP endpoint shown above for any new setup.

### Permissions

Confluence access requires the `read_confluence` (and `search_confluence`, `write_confluence` if you need to edit) permission groups to be enabled on your account/instance. If your company's Atlassian admin hasn't enabled these for your license yet, the connector will authenticate but return no Confluence data — that's a permissions issue, not a broken connection.

### What this gets you for this project

Once connected, you'll be able to ask Claude Code to read your existing PPT-derived backlog pages, feature/story definitions, or any other Confluence content directly — this is the actual mechanism for the backlog-import step described in `PLAN.md` Phase 2 ("import your actual existing features/stories from wherever they live"). Confirm with Claude at that point by asking it to list or search the relevant Confluence space before assuming it can see everything.

---

## 2. GitLab — official GitLab MCP server

GitLab ships its own MCP server, supporting both GitLab.com and self-managed/company instances.

### Setup

```bash
claude mcp add --transport http GitLab https://<your-company-gitlab-domain>/api/v4/mcp
```

Replace `<your-company-gitlab-domain>` with your company's actual GitLab hostname (e.g. `gitlab.yourcompany.com`). If your company uses GitLab.com directly (not self-managed), use `gitlab.com` instead.

Then, inside a Claude Code session:

```
/mcp
```

Select your GitLab server from the list, then approve the OAuth authorization request in your browser.

### Authentication

GitLab's MCP server uses OAuth 2.0, not a static personal access token, for the Claude Code integration path. If your company's GitLab admin needs to register Claude Code as an OAuth application first, they'll need to grant it the **`mcp`** scope specifically.

### Security note (from GitLab's own docs, worth taking seriously)

GitLab's documentation explicitly states you're responsible for guarding against prompt injection when using these tools, and to exercise caution using MCP tools only on GitLab objects you trust. In practice: be deliberate about which repos/issues you have Claude read via this connector, especially ones with content from outside your immediate team.

---

## Once both are connected

A reasonable next step for this project specifically: ask Claude Code to search your company Confluence for the existing PPT-derived cost-optimization backlog pages, and cross-reference against `backlog/epics/` in this repo — that's the real version of the "reconcile against the illustrative starter epics" step flagged as pending in `STATE.md`.

## Sources

- [Atlassian's MCP Server official repo](https://github.com/atlassian/atlassian-mcp-server)
- [Atlassian MCP Server GA announcement](https://www.mindstudio.ai/blog/atlassian-mcp-server-ga-claude-reads-writes-jira-confluence-compass-oauth)
- [GitLab MCP server official docs](https://docs.gitlab.com/user/model_context_protocol/mcp_server/)
- [GitLab MCP setup walkthrough](https://mcp.harishgarg.com/use/gitlab/mcp-server/with/claude-code)
