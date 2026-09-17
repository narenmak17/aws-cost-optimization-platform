"""Local review UI for the AWS Cost Optimization Platform repo.

Reads backlog/, .claude/skills/, .claude/agents/ from disk. No AWS calls,
no credentials required — this is a repo browser, not a live cost dashboard.
"""
import pathlib
import frontmatter
import markdown
from flask import Flask, render_template, abort

ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "backlog"
SKILLS_DIR = ROOT / ".claude" / "skills"
AGENTS_DIR = ROOT / ".claude" / "agents"

# Top-level docs surfaced for one-click "copy for Confluence" — add new
# markdown files here to make them show up on the /docs page.
DOC_FILES = [
    ("README", ROOT / "README.md"),
    ("STATE", ROOT / "STATE.md"),
    ("PLAN", ROOT / "PLAN.md"),
    ("PROGRESS", ROOT / "PROGRESS.md"),
    ("Design Plan", ROOT / "docs" / "design-plan.md"),
    ("Connect Confluence & GitLab via MCP", ROOT / "docs" / "guides" / "connect-confluence-gitlab-mcp.md"),
    ("Cross-Account Role Design", ROOT / "connectivity" / "cross-account-role.md"),
    ("CUDOS Deployment Plan", ROOT / "dashboard" / "cudos-deployment-plan.md"),
]

app = Flask(__name__)


def load_md_dir(path: pathlib.Path) -> list[dict]:
    items = []
    if not path.exists():
        return items
    for f in sorted(path.glob("*.md")):
        post = frontmatter.load(f)
        items.append({
            "meta": post.metadata,
            "body_html": markdown.markdown(post.content),
            "filename": f.stem,
        })
    return items


def load_skill_dirs(path: pathlib.Path) -> list[dict]:
    """Custom skills live directly under skills/; vendored ones under skills/vendored/."""
    items = []
    if not path.exists():
        return items
    for d in sorted(path.iterdir()):
        if not d.is_dir() or d.name == "vendored":
            continue
        skill_md = d / "SKILL.md"
        if skill_md.exists():
            post = frontmatter.load(skill_md)
            items.append({"meta": post.metadata, "kind": "custom", "name": d.name})
    vendored = path / "vendored"
    if vendored.exists():
        for d in sorted(vendored.iterdir()):
            skill_md = d / "SKILL.md"
            if d.is_dir() and skill_md.exists():
                post = frontmatter.load(skill_md)
                items.append({"meta": post.metadata, "kind": "vendored", "name": d.name})
    return items


def load_agents(path: pathlib.Path) -> list[dict]:
    items = []
    if not path.exists():
        return items
    for f in sorted(path.glob("*.md")):
        post = frontmatter.load(f)
        items.append({
            "meta": post.metadata,
            "body_html": markdown.markdown(post.content),
            "name": f.stem,
        })
    return items


def build_backlog_tree():
    epics = load_md_dir(BACKLOG / "epics")
    features = load_md_dir(BACKLOG / "features")
    stories = load_md_dir(BACKLOG / "stories")

    for epic in epics:
        epic_id = epic["meta"].get("id")
        epic["features"] = []
        for feat in features:
            if feat["meta"].get("epic") == epic_id:
                feat_id = feat["meta"].get("id")
                feat["stories"] = [s for s in stories if s["meta"].get("feature") == feat_id]
                epic["features"].append(feat)
    return epics


@app.route("/")
def index():
    epics = build_backlog_tree()
    skills = load_skill_dirs(SKILLS_DIR)
    agents = load_agents(AGENTS_DIR)
    story_count = sum(len(f.get("stories", [])) for e in epics for f in e["features"])
    feature_count = sum(len(e["features"]) for e in epics)
    return render_template(
        "index.html",
        epics=epics,
        skills=skills,
        agents=agents,
        stats={
            "epics": len(epics),
            "features": feature_count,
            "stories": story_count,
            "skills": len(skills),
            "agents": len(agents),
        },
    )


@app.route("/epic/<epic_id>")
def epic_detail(epic_id):
    epics = build_backlog_tree()
    epic = next((e for e in epics if e["meta"].get("id") == epic_id), None)
    if not epic:
        abort(404)
    return render_template("epic.html", epic=epic)


@app.route("/skills")
def skills_page():
    skills = load_skill_dirs(SKILLS_DIR)
    return render_template("skills.html", skills=skills)


@app.route("/agents")
def agents_page():
    agents = load_agents(AGENTS_DIR)
    return render_template("agents.html", agents=agents)


@app.route("/docs")
def docs_index():
    docs = [{"slug": name.lower().replace(" ", "-").replace("&", "and"), "title": name}
            for name, path in DOC_FILES if path.exists()]
    return render_template("docs_index.html", docs=docs)


@app.route("/docs/<slug>")
def docs_detail(slug):
    for name, path in DOC_FILES:
        this_slug = name.lower().replace(" ", "-").replace("&", "and")
        if this_slug == slug and path.exists():
            html = markdown.markdown(path.read_text(encoding="utf-8"), extensions=["tables", "fenced_code"])
            return render_template("doc_detail.html", title=name, body_html=html, slug=slug)
    abort(404)


if __name__ == "__main__":
    # debug=True's reloader forks a child process, which doesn't survive
    # being spawned through Command Deck's nested minimized-window chain
    # (VBS -> cmd -> start /min -> cmd) reliably. Keep this False.
    app.run(debug=False, port=5060)
