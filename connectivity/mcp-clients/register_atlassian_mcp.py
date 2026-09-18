"""Config-driven registration of the self-hosted Atlassian MCP server for Claude Code.

Reads connection details from config.json (git-ignored; copy config.example.json to
create it) and the PAT from the environment variable it names, then emits (and runs)
the equivalent `claude mcp add` command. Keeping this in one script means the
connection details live in one reviewable file instead of being retyped into a
terminal each time — see docs/dev-methodologies/context-engineering.md for why that
matters across sessions.

Usage:
    python register_atlassian_mcp.py            # prints the command, asks before running
    python register_atlassian_mcp.py --run       # runs it directly
"""

import json
import os
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        sys.exit(
            f"Missing {CONFIG_PATH}. Copy config.example.json to config.json and fill in your "
            "company's Confluence/Jira URLs first."
        )
    return json.loads(CONFIG_PATH.read_text())


def build_command(cfg: dict) -> list[str]:
    atl = cfg["atlassian"]
    token_var = atl["personal_token_env_var"]
    if not os.environ.get(token_var):
        sys.exit(
            f"Environment variable {token_var} is not set. Export your Confluence/Jira "
            "Personal Access Token into it first (see docs/guides/connect-confluence-gitlab-mcp.md)."
        )

    cmd = [
        "claude", "mcp", "add", "atlassian-selfhosted",
        "--env", f"CONFLUENCE_URL={atl['confluence_url']}",
        "--env", f"JIRA_URL={atl['jira_url']}",
        "--env", f"CONFLUENCE_PERSONAL_TOKEN=${token_var}",
        "--env", f"JIRA_PERSONAL_TOKEN=${token_var}",
    ]
    if atl.get("confluence_spaces_filter"):
        cmd += ["--env", f"CONFLUENCE_SPACES_FILTER={atl['confluence_spaces_filter']}"]
    if atl.get("jira_projects_filter"):
        cmd += ["--env", f"JIRA_PROJECTS_FILTER={atl['jira_projects_filter']}"]
    if atl.get("read_only", True):
        cmd += ["--env", "READ_ONLY_MODE=true"]
    cmd += ["--", "uvx", "mcp-atlassian"]
    return cmd


def main() -> None:
    cfg = load_config()
    cmd = build_command(cfg)
    print("Command to register the MCP server:\n")
    print(" ".join(cmd))

    if "--run" in sys.argv:
        subprocess.run(cmd, check=True)
        print("\nRegistered. Run /mcp inside a Claude Code session to confirm it connected.")
    else:
        print("\nRe-run with --run to execute it, or paste the command above yourself.")


if __name__ == "__main__":
    main()
