import json
import sys

import httpx
from mcp.server.fastmcp import FastMCP

import dump

mcp = FastMCP("Roblox Docs")

dump_class = None
try:
    version = httpx.get("https://setup.rbxcdn.com/versionQTStudio")
    version.raise_for_status()
    raw_dump = httpx.get(f"https://setup.rbxcdn.com/{version.text}-API-Dump.json")
    raw_dump.raise_for_status()
    dump_class = dump.dump_from_dict(json.loads(raw_dump.text))
    print(
        f"Successfully loaded Roblox API dump (version: {version.text})",
        file=sys.stderr,
    )
except Exception as e:
    print(f"Error loading Roblox API dump: {e}", file=sys.stderr)
    sys.exit(1)


@mcp.tool()
async def get_class(className: str) -> str:
    """
    Fetches the API details for a specific Roblox ClassName.
    Returns properties, functions, and events in a condensed format.
    """
    if dump_class is None:
        return "Error: API dump not loaded. Server initialization failed."

    # Find the target class in our pre-loaded dump_class
    target = next((c for c in dump_class.classes if c.name == className), None)
    if not target:
        return f"Error: Class '{className}' not found in the Roblox API dump."

    # Build a concise Markdown response
    lines = [f"# Class: {target.name}"]
    lines.append(f"**Inherits from:** {target.superclass}")
    if target.tags:
        lines.append(f"**Tags:** {', '.join([t.value for t in target.tags])}")

    lines.append("\n## Members")

    # Sort members by type to make it readable for the AI
    properties = [
        m for m in target.members if m.member_type == dump.MemberType.PROPERTY
    ]
    functions = [m for m in target.members if m.member_type == dump.MemberType.FUNCTION]
    events = [m for m in target.members if m.member_type == dump.MemberType.EVENT]

    if properties:
        lines.append("\n### Properties")
        for p in properties:
            v_type = p.value_type.name if p.value_type else "unknown"
            lines.append(f"- `{p.name}` ({v_type})")

    if functions:
        lines.append("\n### Functions")
        for f in functions:
            params = ", ".join([p.name for p in f.parameters]) if f.parameters else ""
            lines.append(f"- `{f.name}({params})`")

    if events:
        lines.append("\n### Events")
        for e in events:
            lines.append(f"- `.{e.name}`")

    return "\n".join(lines)


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
