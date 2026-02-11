"""React Roblox documentation MCP server."""

import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Documentation directory
DOCS_DIR = Path(__file__).parent / "docs"
README_PATH = Path(__file__).parent / "README.md"

# Documentation structure - maps key to local file path
DOC_PATHS = {
    # Main
    "readme": str(README_PATH),
    "gettingStarted": "guides/getting-started.md",
    # Guides
    "components": "guides/components.md",
    "stories": "guides/stories.md",
    "pixelScaling": "guides/pixel-scaling.md",
    # API Reference
    "core": "api/core.md",
    "ripple": "api/ripple.md",
    "prettyHooks": "api/pretty-hooks.md",
    "lifetime": "api/lifetime.md",
    "ultimateList": "api/ultimate-list.md",
    "robloxApis": "api/roblox-apis.md",
}

mcp = FastMCP("react-roblox")


def get_doc_content(file_path: str) -> str:
    """Load documentation content from local file."""
    # Handle absolute paths (like README)
    if file_path.startswith("/"):
        full_path = Path(file_path)
    else:
        full_path = DOCS_DIR / file_path

    if not full_path.exists():
        raise Exception(f"Documentation file not found: {file_path}")

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise Exception(f"Failed to read documentation: {file_path} - {str(e)}")


def extract_code_examples(content: str) -> list[dict]:
    """Extract code blocks from markdown content."""
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)

    examples = []
    for language, code in matches:
        examples.append({"language": language or "plaintext", "code": code.strip()})

    return examples


def extract_headings(content: str) -> list[str]:
    """Extract headings from markdown content."""
    pattern = r"^#{1,6}\s+(.+)$"
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches


@mcp.tool()
def get_documentation(doc_key: str) -> str:
    """Fetch specific React Roblox documentation content by key."""
    if doc_key not in DOC_PATHS:
        return f"Documentation not found: {doc_key}"

    try:
        path = DOC_PATHS[doc_key]
        content = get_doc_content(path)
        return f"# {doc_key}\n\nPath: {path}\n\n{content}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def search_documentation(query: str) -> str:
    """Search React Roblox documentation for specific topics or keywords."""
    results = []
    query_lower = query.lower()

    for key, path in DOC_PATHS.items():
        try:
            content = get_doc_content(path)
            content_lower = content.lower()

            if query_lower in content_lower:
                matches = content_lower.count(query_lower)
                index = content_lower.find(query_lower)
                start = max(0, index - 100)
                end = min(len(content), index + 200)
                snippet = "..." + content[start:end] + "..."

                results.append(
                    {"path": path, "key": key, "snippet": snippet, "matches": matches}
                )
        except Exception:
            continue

    if not results:
        return f'No results found for query: "{query}"'

    results.sort(key=lambda x: x["matches"], reverse=True)

    output = f'# Search Results for "{query}"\n\n'
    output += f"Found {len(results)} result(s):\n\n"

    for i, result in enumerate(results, 1):
        output += f"## Result {i} (Matches: {result['matches']})\n"
        output += f"**Path:** {result['path']}\n"
        output += f"**Key:** {result['key']}\n\n"
        output += f"{result['snippet']}\n\n---\n\n"

    return output


@mcp.tool()
def list_documentation() -> str:
    """List all available React Roblox documentation pages with metadata."""
    output = "# Available React Roblox Documentation\n\n"

    # Group by category
    categories = {}
    for key, path in DOC_PATHS.items():
        path_parts = path.replace(str(README_PATH), "main").split("/")
        category = path_parts[0] if len(path_parts) > 1 else "main"
        title = re.sub(r"([A-Z])", r" \1", key).strip()

        if category not in categories:
            categories[category] = []

        categories[category].append(
            {
                "key": key,
                "path": path,
                "title": title,
                "description": f"React Roblox documentation: {title}",
            }
        )

    for category, docs in sorted(categories.items()):
        output += f"## {category.title()}\n\n"
        for doc in docs:
            output += f"- **{doc['title']}** (`{doc['key']}`)\n"
            output += f"  Path: {doc['path']}\n"
            output += f"  {doc['description']}\n\n"

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
def search_code_examples(query: str) -> str:
    """Search for code examples across all documentation."""
    results = []
    query_lower = query.lower()

    for key, path in DOC_PATHS.items():
        try:
            content = get_doc_content(path)
            examples = extract_code_examples(content)

            for i, example in enumerate(examples, 1):
                if query_lower in example["code"].lower():
                    results.append(
                        {
                            "doc_key": key,
                            "example_num": i,
                            "language": example["language"],
                            "code": example["code"][:300] + "..."
                            if len(example["code"]) > 300
                            else example["code"],
                        }
                    )
        except Exception:
            continue

    if not results:
        return f'No code examples found for query: "{query}"'

    output = f'# Code Examples Matching "{query}"\n\n'
    output += f"Found {len(results)} example(s):\n\n"

    for i, result in enumerate(results, 1):
        output += f"## Example {i} from {result['doc_key']}\n"
        output += f"**Language:** {result['language']}\n\n"
        output += f"```{result['language']}\n{result['code']}\n```\n\n---\n\n"

    return output


def main():
    """Main entry point."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
