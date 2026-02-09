"""React-Lua documentation MCP server."""

import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Documentation directory
DOCS_DIR = Path(__file__).parent / "docs"

# Documentation structure - maps key to local file path
DOC_PATHS = {
    # API Reference
    "coreApi": "api/core.md",
    "hooks": "api/hooks.md",
    "contextApi": "api/context.md",
    "advancedApi": "api/advanced.md",
    # Guides
    "gettingStarted": "guides/getting-started.md",
    "componentPatterns": "guides/components.md",
    "projectStructure": "guides/project-structure.md",
    # Examples
    "counterExample": "examples/counter.md",
    "formExample": "examples/form.md",
    "slitherProject": "examples/project-slither.md",
    "uiLabsProject": "examples/project-ui-labs.md",
}

mcp = FastMCP("react-roblox")


def get_doc_content(file_path: str) -> str:
    """Load documentation content from local file."""
    full_path = DOCS_DIR / file_path

    if not full_path.exists():
        raise Exception(f"Documentation file not found: {file_path}")

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise Exception(f"Failed to read documentation: {file_path} - {str(e)}")


def extract_headings(content: str) -> list[str]:
    """Extract headings from markdown content."""
    pattern = r"^#{1,6}\s+(.+)$"
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches


def extract_code_examples(content: str) -> list[dict]:
    """Extract code blocks from markdown content."""
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)

    examples = []
    for language, code in matches:
        examples.append({"language": language or "plaintext", "code": code.strip()})

    return examples


@mcp.tool()
def get_documentation(doc_key: str) -> str:
    """Fetch specific React-Lua documentation content by key."""
    if doc_key not in DOC_PATHS:
        return f"Documentation not found: {doc_key}"

    try:
        path = DOC_PATHS[doc_key]
        content = get_doc_content(path)
        return f"# {doc_key}\n\nPath: {path}\n\n{content}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def list_documentation() -> str:
    """List all available React-Lua documentation pages with metadata."""
    output = "# Available React-Lua Documentation\n\n"

    # Group by category
    categories = {
        "api": [],
        "guides": [],
        "examples": [],
    }

    for key, path in DOC_PATHS.items():
        category = path.split("/")[0]
        title = re.sub(r"([A-Z])", r" \1", key).strip()

        categories[category].append({"key": key, "path": path, "title": title})

    # Output by category
    category_names = {"api": "API Reference", "guides": "Guides", "examples": "Examples"}

    for cat_key in ["api", "guides", "examples"]:
        items = categories[cat_key]
        if items:
            output += f"## {category_names[cat_key]}\n\n"
            for item in items:
                output += f"- **{item['title']}** (`{item['key']}`)\n"
                output += f"  Path: {item['path']}\n\n"

    return output


@mcp.tool()
def extract_code_examples_from_doc(doc_key: str) -> str:
    """Extract code examples from a specific documentation page."""
    if doc_key not in DOC_PATHS:
        return f"Documentation not found: {doc_key}"

    try:
        path = DOC_PATHS[doc_key]
        content = get_doc_content(path)
        examples = extract_code_examples(content)

        if not examples:
            return f"No code examples found in {doc_key}"

        output = f"# Code Examples from {doc_key}\n\n"
        output += f"Found {len(examples)} example(s):\n\n"

        for i, example in enumerate(examples, 1):
            output += f"### Example {i} ({example['language']})\n\n"
            output += f"```{example['language']}\n{example['code']}\n```\n\n"

        return output
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_documentation_outline(doc_key: str) -> str:
    """Get the outline (headings) of a documentation file."""
    if doc_key not in DOC_PATHS:
        return f"Documentation not found: {doc_key}"

    try:
        path = DOC_PATHS[doc_key]
        content = get_doc_content(path)
        headings = extract_headings(content)

        output = f"# Outline of {doc_key}\n\n"
        output += f"Path: {path}\n\n"

        if headings:
            for heading in headings:
                output += f"- {heading}\n"
        else:
            output += "No headings found.\n"

        return output
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def search_documentation(query: str) -> str:
    """Search React-Lua documentation for specific topics or keywords."""
    results = []
    query_lower = query.lower()

    for key, path in DOC_PATHS.items():
        try:
            content = get_doc_content(path)
            content_lower = content.lower()

            if query_lower in content_lower:
                # Count matches
                matches = content_lower.count(query_lower)

                # Find snippet around first match
                index = content_lower.find(query_lower)
                start = max(0, index - 100)
                end = min(len(content), index + 200)
                snippet = "..." + content[start:end] + "..."

                results.append({"path": path, "key": key, "snippet": snippet, "matches": matches})
        except Exception:
            continue

    if not results:
        return f'No results found for query: "{query}"'

    # Sort by relevance
    results.sort(key=lambda x: x["matches"], reverse=True)

    output = f'# Search Results for "{query}"\n\n'
    output += f"Found {len(results)} result(s):\n\n"

    for i, result in enumerate(results, 1):
        output += f"## Result {i} (Matches: {result['matches']})\n"
        output += f"**Path:** {result['path']}\n"
        output += f"**Key:** {result['key']}\n\n"
        output += f"{result['snippet']}\n\n---\n\n"

    return output


def main():
    """Main entry point."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
