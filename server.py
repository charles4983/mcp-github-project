
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import json

mcp = FastMCP("DeveloperTools")

PROJECT_DIR = Path(__file__).parent.resolve()

@mcp.tool()
def get_project_info() -> dict:
    """Return information about the project."""
    return {
        "name": "MCP Developer Tools",
        "language": "Python",
        "status": "active"
    }

@mcp.tool()
def list_project_files() -> list[str]:
    """List files in the current project directory."""
    return sorted(
        p.name for p in PROJECT_DIR.iterdir()
        if p.is_file()
    )

@mcp.tool()
def create_task(title: str) -> dict:
    """Create a new development task."""
    title = title.strip()
    if not title or len(title) > 200:
        return {"error": "Invalid task title"}

    path = PROJECT_DIR / "tasks.json"
    tasks = json.loads(path.read_text()) if path.exists() else []

    task = {"id": len(tasks) + 1, "title": title}
    tasks.append(task)
    path.write_text(json.dumps(tasks, indent=2))

    return task

@mcp.tool()
def list_tasks() -> list[dict]:
    """Retrieve all development tasks."""
    path = PROJECT_DIR / "tasks.json"

    if not path.exists():
        return []

    return json.loads(path.read_text())

if __name__ == "__main__":
    mcp.run(transport="stdio")
