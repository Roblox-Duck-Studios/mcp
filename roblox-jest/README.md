# Roblox Jest MCP Server

This MCP server provides access to Roblox Jest documentation and testing best practices.

## Available Tools

- `get_documentation` - Fetch specific Roblox Jest documentation content by key
- `search_documentation` - Search documentation for specific topics or keywords
- `list_documentation` - List all available documentation pages with metadata
- `extract_code_examples_from_doc` - Extract code examples from a specific documentation page
- `get_documentation_outline` - Get the outline (headings) of a documentation file
- `search_code_examples` - Search for code examples across all documentation

## Documentation Topics

### Main
- `readme` - Overview and quick links
- `introduction` - Introduction to Roblox Jest
- `installation` - Installation guide
- `configuration` - Configuration options
- `setupTests` - Setup tests module documentation
- `bestPractices` - Testing best practices

### Guides
- `writingTests` - How to write tests
- `testStructure` - Test directory structure
- `coverage` - Code coverage configuration
- `jestAssassin` - Jestrbx CLI tool documentation
- `globalMocks` - Mocking global functions (print, math.random, etc.)

## Usage

Run the MCP server:

```bash
python main.py
```

Or via the MCP CLI:

```bash
mcp run main.py
```
