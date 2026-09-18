# Connecting Self-Hosted Confluence, Jira, and GitLab via MCP

Correction from an earlier version of this guide: this section originally assumed Atlassian Cloud (`mcp.atlassian.com`), which only works for cloud-hosted Confluence/Jira. **This company runs self-hosted (Data Center) Confluence and Jira**, which is a different connector path — Atlassian's own remote MCP server does not support Data Center instances as of this writing. Below is the corrected, self-hosted-specific path, plus config-driven client code so the connection details live in one file instead of being hardcoded into commands.

**None of this has been run yet.** This is a guide to follow yourself, since it requires your own company credentials/OAuth app registration — I cannot complete that step for you.

---

## 1. Why self-hosted needs a different approach

Atlassian's official remote MCP server (`mcp.atlassian.com`) is Cloud-only. For Data Center/Server products, the supported path is the **Atlassian Remote MCP Server's self-managed mode is not offered** — instead, the community-maintained, self-host-aware server is the practical option:

- **[`sooperset/mcp-atlassian`](https://github.com/sooperset/mcp-atlassian)** — the most widely used community MCP server that explicitly supports Confluence/Jira **Data Center and Server** via Personal Access Tokens (PATs), in addition to Cloud via API tokens or OAuth. This is what the steps below use.

Check with your Atlassian admin first: Data Center PATs are created per-user under **Profile → Personal Access Tokens**, and need to be enabled at the instance level (`Administration → Security → Personal Access Tokens`). If PATs are disabled instance-wide, you'll need your admin to enable them or use basic auth (supported but discouraged — PATs are revocable and don't expose your password).

## 2. Install and run the MCP server

The server runs locally (stdio transport) and talks to your company's Confluence/Jira over HTTPS using your PAT. It does **not** require internet egress beyond your company's own Atlassian instances.

```bash
# Requires Python 3.10+; uvx runs it without a manual venv
uvx mcp-atlassian \
  --confluence-url https://confluence.yourcompany.com \
  --confluence-personal-token "$CONFLUENCE_PAT" \
  --jira-url https://jira.yourcompany.com \
  --jira-personal-token "$JIRA_PAT"
```

Don't put tokens directly on the command line in a shared shell history — use environment variables (see the config-driven setup below) or a `.env` file that's git-ignored.

## 3. Config-driven setup (recommended over ad-hoc flags)

Rather than remembering CLI flags, register the server once via Claude Code's MCP config and drive it from environment variables. This repo's convention: secrets and instance URLs live in `.env` (git-ignored), the MCP registration itself is checked in.

### 3.1 `.env` (create this file locally — it is git-ignored, see `.gitignore`)

```bash
CONFLUENCE_URL=https://confluence.yourcompany.com
CONFLUENCE_PERSONAL_TOKEN=<your PAT>
JIRA_URL=https://jira.yourcompany.com
JIRA_PERSONAL_TOKEN=<your PAT>
```

### 3.2 Register the server with Claude Code

```bash
claude mcp add atlassian-selfhosted \
  --env CONFLUENCE_URL=$CONFLUENCE_URL \
  --env CONFLUENCE_PERSONAL_TOKEN=$CONFLUENCE_PERSONAL_TOKEN \
  --env JIRA_URL=$JIRA_URL \
  --env JIRA_PERSONAL_TOKEN=$JIRA_PERSONAL_TOKEN \
  -- uvx mcp-atlassian
```

This writes the registration (command + env var *names*, not values) into Claude Code's MCP config. Verify it's live:

```
/mcp
```

You should see `atlassian-selfhosted` listed as connected. If it fails, check: PAT not expired, instance URL reachable from this machine (VPN required for most self-hosted instances), PATs enabled on the instance.

### 3.3 Scoping to specific spaces/projects (recommended)

`mcp-atlassian` supports restricting visibility so the agent only sees what this project needs, not your entire company Confluence/Jira:

```bash
--confluence-spaces-filter "COSTOPT,FINOPS"
--jira-projects-filter "COSTOPT"
```

Add these as additional `--env CONFLUENCE_SPACES_FILTER=...` / `--env JIRA_PROJECTS_FILTER=...` flags in the `claude mcp add` command above. This is worth doing even though PAT-based access already respects your own permissions — it keeps the tool's search results scoped and relevant instead of noisy.

### 3.4 Read-only mode (recommended until you explicitly need writes)

```bash
--env READ_ONLY_MODE=true
```

Given this project's existing trust-boundary discipline (design plan §5: no agent gets standing write access without a human approval gate), default this connector to read-only. Only drop it if a specific workflow needs Claude to create/update Jira issues or Confluence pages directly — and if so, treat that the same way `profile-bootstrap` treats AWS writes: human-approved, not standing.

## 4. What this gets you for this project

Once connected and scoped:
- Search/read Confluence pages (the PPT-derived backlog content) directly — the real mechanism for `PLAN.md` Phase 2's backlog import.
- Search/read Jira issues (if your existing features/stories live there instead of/alongside Confluence).
- Cross-reference against `backlog/epics/` in this repo to reconcile the illustrative starters with the real backlog.

Confirm scope before trusting completeness: ask Claude to list the Confluence spaces or Jira projects it can see, and compare against what you expect, rather than assuming full visibility.

## 5. GitLab — official GitLab MCP server

(Unchanged from the original guidance — GitLab's MCP server supports self-managed instances natively.)

```bash
claude mcp add --transport http GitLab https://<your-company-gitlab-domain>/api/v4/mcp
```

Then inside a Claude Code session:

```
/mcp
```

Select GitLab, approve the OAuth request. GitLab's MCP integration uses OAuth 2.0 — if your company's GitLab admin needs to register Claude Code as an OAuth application, it needs the **`mcp`** scope.

**Security note (from GitLab's own docs):** you're responsible for guarding against prompt injection when using these tools — be deliberate about which repos/issues you let Claude read via this connector, especially content from outside your immediate team.

## Do's and don'ts for this connector

**Do:**
- Scope the connector to this project's specific spaces/projects (§3.3) rather than granting implicit access to everything you can see.
- Default to read-only (§3.4) and add write access only for a specific, human-approved workflow.
- Keep the PAT in `.env`, never in a committed file or command-line history.
- Rotate the PAT per your company's token policy — Data Center PATs typically have a configurable max lifetime.

**Don't:**
- Don't assume `mcp.atlassian.com` (the Cloud remote server) will work — it won't, for a self-hosted instance, and will fail silently or with a confusing auth error.
- Don't grant write access by default "in case it's needed later" — add it when a real workflow needs it, per this repo's existing guardrail philosophy.
- Don't skip the spaces/projects filter — an unscoped connector searching your entire company Confluence is both noisy and a wider blast radius than this project needs.

## Sources

- [`sooperset/mcp-atlassian` — GitHub repo](https://github.com/sooperset/mcp-atlassian) — the community MCP server used above; documents Data Center/Server PAT auth, space/project filters, and read-only mode.
- [Atlassian: Using Personal Access Tokens](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html) — official docs on enabling and creating Data Center PATs.
- [Atlassian Remote MCP Server official repo](https://github.com/atlassian/atlassian-mcp-server) — for reference/comparison; confirms Cloud-only scope.
- [GitLab MCP server official docs](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) — self-managed instance support.
- [Model Context Protocol specification](https://modelcontextprotocol.io/) — underlying protocol reference, useful background for the client-code section below.
