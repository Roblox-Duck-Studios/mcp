import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# GitHub API configuration
GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/roblox-ts/roblox-ts.com/master/docs"
)
GITHUB_API_BASE = "https://api.github.com/repos/roblox-ts/roblox-ts.com/contents/docs"

# Documentation structure
DOC_PATHS = {
    # Main pages
    "introduction": "introduction.mdx",
    "quickStart": "quick-start.mdx",
    "setupGuide": "setup-guide.mdx",
    "usage": "usage.mdx",
    # API docs
    "robloxApi": "api/roblox-api.mdx",
    # Guides
    "syncingWithRojo": "guides/syncing-with-rojo.mdx",
    "usingExistingLuau": "guides/using-existing-luau.mdx",
    "typeScriptPackages": "guides/typescript-packages.mdx",
    "roactJsx": "guides/roact-jsx.mdx",
}


class DocCache:
    """Simple cache for documentation"""

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, str] = {}
        self.timestamps: Dict[str, datetime] = {}
        self.ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            if datetime.now() - self.timestamps[key] < self.ttl:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None

    def set(self, key: str, value: str):
        self.cache[key] = value
        self.timestamps[key] = datetime.now()


# Global cache instance
doc_cache = DocCache()


async def fetch_doc_content(file_path: str) -> str:
    """Fetch documentation content from GitHub"""
    # Check cache first
    cached = doc_cache.get(file_path)
    if cached:
        return cached

    url = f"{GITHUB_RAW_BASE}/{file_path}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            content = response.text

            # Cache the content
            doc_cache.set(file_path, content)
            return content
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch documentation: {file_path} - {str(e)}")


async def search_docs(query: str) -> List[Dict[str, Any]]:
    """Search across all documentation"""
    results = []
    query_lower = query.lower()

    for key, path in DOC_PATHS.items():
        try:
            content = await fetch_doc_content(path)
            content_lower = content.lower()

            if query_lower in content_lower:
                # Count matches
                matches = content_lower.count(query_lower)

                # Find snippet around first match
                index = content_lower.find(query_lower)
                start = max(0, index - 100)
                end = min(len(content), index + 200)
                snippet = "..." + content[start:end] + "..."

                results.append(
                    {"path": path, "key": key, "snippet": snippet, "relevance": matches}
                )
        except Exception as e:
            print(f"Error searching {path}: {e}")
            continue

    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)
    return results


def extract_code_examples(content: str) -> List[Dict[str, str]]:
    """Extract code blocks from MDX content"""
    # Regex pattern to match code blocks
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)

    examples = []
    for language, code in matches:
        examples.append({"language": language or "plaintext", "code": code.strip()})

    return examples


def extract_headings(content: str) -> List[str]:
    """Extract headings from MDX content"""
    pattern = r"^#{1,6}\s+(.+)$"
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches


async def list_docs() -> List[Dict[str, str]]:
    """List all available documentation"""
    docs = []

    for key, path in DOC_PATHS.items():
        path_parts = path.split("/")
        category = path_parts[0] if len(path_parts) > 1 else "main"

        # Convert camelCase to Title Case
        title = re.sub(r"([A-Z])", r" \1", key).strip()

        docs.append(
            {
                "key": key,
                "path": path,
                "category": category,
                "title": title,
                "description": f"roblox-ts documentation: {title}",
            }
        )

    return docs


# Create MCP server
app = Server("roblox-ts-docs")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_documentation",
            description="Fetch specific roblox-ts documentation content by key",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_key": {
                        "type": "string",
                        "description": "Key of the documentation",
                        "enum": list(DOC_PATHS.keys()),
                    }
                },
                "required": ["doc_key"],
            },
        ),
        Tool(
            name="search_documentation",
            description="Search roblox-ts documentation for specific topics or keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find in documentation",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="list_documentation",
            description="List all available roblox-ts documentation pages with metadata",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="extract_code_examples",
            description="Extract code examples from a specific documentation page",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_key": {
                        "type": "string",
                        "description": "Key of the documentation to extract code from",
                        "enum": list(DOC_PATHS.keys()),
                    }
                },
                "required": ["doc_key"],
            },
        ),
        Tool(
            name="get_doc_outline",
            description="Get the outline (headings) of a documentation file",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_key": {
                        "type": "string",
                        "description": "Key of the documentation",
                        "enum": list(DOC_PATHS.keys()),
                    }
                },
                "required": ["doc_key"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""

    try:
        if name == "get_documentation":
            doc_key = arguments["doc_key"]

            if doc_key not in DOC_PATHS:
                return [
                    TextContent(type="text", text=f"Documentation not found: {doc_key}")
                ]

            path = DOC_PATHS[doc_key]
            content = await fetch_doc_content(path)

            return [
                TextContent(
                    type="text", text=f"# {doc_key}\n\nPath: {path}\n\n{content}"
                )
            ]

        elif name == "search_documentation":
            query = arguments["query"]
            results = await search_docs(query)

            if not results:
                return [
                    TextContent(
                        type="text", text=f'No results found for query: "{query}"'
                    )
                ]

            output = f'# Search Results for "{query}"\n\n'
            output += f"Found {len(results)} result(s):\n\n"

            for i, result in enumerate(results, 1):
                output += f"## Result {i} (Relevance: {result['relevance']})\n"
                output += f"**Path:** {result['path']}\n"
                output += f"**Key:** {result['key']}\n\n"
                output += f"{result['snippet']}\n\n---\n\n"

            return [TextContent(type="text", text=output)]

        elif name == "list_documentation":
            docs = await list_docs()

            output = "# Available roblox-ts Documentation\n\n"

            # Group by category
            categories = {}
            for doc in docs:
                cat = doc["category"]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(doc)

            for category, cat_docs in categories.items():
                output += f"## {category.title()}\n\n"
                for doc in cat_docs:
                    output += f"- **{doc['title']}** (`{doc['key']}`)\n"
                    output += f"  Path: {doc['path']}\n"
                    output += f"  {doc['description']}\n\n"

            return [TextContent(type="text", text=output)]

        elif name == "extract_code_examples":
            doc_key = arguments["doc_key"]

            if doc_key not in DOC_PATHS:
                return [
                    TextContent(type="text", text=f"Documentation not found: {doc_key}")
                ]

            path = DOC_PATHS[doc_key]
            content = await fetch_doc_content(path)
            examples = extract_code_examples(content)

            if not examples:
                return [
                    TextContent(
                        type="text", text=f"No code examples found in {doc_key}"
                    )
                ]

            output = f"# Code Examples from {doc_key}\n\n"
            output += f"Found {len(examples)} example(s):\n\n"

            for i, example in enumerate(examples, 1):
                output += f"### Example {i} ({example['language']})\n\n"
                output += f"```{example['language']}\n{example['code']}\n```\n\n"

            return [TextContent(type="text", text=output)]

        elif name == "get_doc_outline":
            doc_key = arguments["doc_key"]

            if doc_key not in DOC_PATHS:
                return [
                    TextContent(type="text", text=f"Documentation not found: {doc_key}")
                ]

            path = DOC_PATHS[doc_key]
            content = await fetch_doc_content(path)
            headings = extract_headings(content)

            output = f"# Outline of {doc_key}\n\n"
            output += f"Path: {path}\n\n"

            if headings:
                for heading in headings:
                    output += f"- {heading}\n"
            else:
                output += "No headings found.\n"

            return [TextContent(type="text", text=output)]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
