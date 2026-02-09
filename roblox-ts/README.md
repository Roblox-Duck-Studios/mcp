# Roblox-ts - MCP Documentation

This MCP (Model Context Protocol) documentation provides comprehensive information about using **roblox-ts**, a TypeScript toolchain for Roblox development.

## Overview

roblox-ts is a way to use the tooling and ecosystem surrounding TypeScript for Roblox development, including intellisense, IDE extensions, linters, code formatters, and more. It allows you to write TypeScript code that is then compiled into Luau code for use inside of Roblox.

## Structure

```
roblox-ts/
├── README.md                    # Overview and structure
├── MCP_OVERVIEW.md             # What this MCP covers
├── QUICK_REFERENCE.md          # Quick lookup guide
└── docs/
    ├── INDEX.md                # Navigation guide
    ├── introduction.md         # What is roblox-ts?
    ├── quick-start.md          # Getting started
    ├── setup-guide.md          # Installation & setup
    ├── usage.md                # How to use roblox-ts
    ├── api/
    │   └── roblox-api.md       # Roblox API reference
    ├── guides/
    │   ├── syncing-with-rojo.md
    │   ├── using-existing-luau.md
    │   ├── typescript-packages.md
    │   ├── roact-jsx.md
    │   ├── typescript-transformers.md
    │   ├── luau-packages.md
    │   ├── lua-tuple.md
    │   ├── indexing-children.md
    │   ├── datatype-math.md
    │   └── callbacks-vs-methods.md
    └── faq/
        ├── powershell.md
        ├── publish-not-found.md
        └── publish-as-public.md
```

## Key Concepts

### What is roblox-ts?

- **TypeScript for Roblox** - Write TypeScript code, it compiles to Luau
- **Full IDE Support** - Intellisense, autocomplete, type checking
- **Modern Tooling** - ESLint, Prettier, and other TypeScript tools
- **Large Projects** - Manage complex games with static typing
- **Open Source** - Customize with TypeScript transformer plugins

### Core Features

- Write TypeScript code that runs in Roblox
- Automatic project structure setup
- Auto-generated type definitions for Roblox API
- Rojo integration for syncing code
- Support for both `.ts` and `.lua` files with `.d.ts` types
- Growing ecosystem of NPM packages

## Quick Links

- **[Introduction](./docs/introduction.md)** - What is roblox-ts and why use it?
- **[Quick Start](./docs/quick-start.md)** - Get your first project running
- **[Setup Guide](./docs/setup-guide.md)** - Installation and configuration
- **[Usage Guide](./docs/usage.md)** - How to use roblox-ts
- **[API Reference](./docs/api/roblox-api.md)** - Roblox API documentation
- **[Navigation Index](./docs/INDEX.md)** - Complete documentation index

## Getting Started

1. **New to roblox-ts?**
   - Start with [Introduction](./docs/introduction.md)
   - Follow [Quick Start](./docs/quick-start.md)
   - Read [Setup Guide](./docs/setup-guide.md)

2. **Ready to develop?**
   - Read [Usage Guide](./docs/usage.md)
   - Check [Syncing with Rojo](./docs/guides/syncing-with-rojo.md)
   - Review [Project Structure](./docs/guides/)

3. **Need specific help?**
   - Search [INDEX.md](./docs/INDEX.md) for topic
   - Check [FAQ](./docs/faq/) for common issues
   - Look at guides for advanced topics

## References

- **Official roblox-ts**: https://roblox-ts.com
- **GitHub**: https://github.com/roblox-ts/roblox-ts
- **Discord**: https://discord.roblox-ts.com
- **NPM Packages**: https://www.npmjs.com/org/rbxts

---

**MCP created**: 2026  
**Based on**: Official roblox-ts documentation  
**Scope**: Complete roblox-ts toolchain and API reference
