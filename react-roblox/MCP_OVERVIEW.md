# React in Roblox - MCP Overview

## What is This?

This is a **Model Context Protocol (MCP)** documentation collection for **React development in Roblox using TypeScript**. It provides comprehensive, organized information about building modern UIs with React and roblox-typescript.

## Contents

### Main Documentation

```
react-roblox/
├── README.md                           # Overview and quick start
├── docs/
│   ├── INDEX.md                        # Quick navigation guide
│   │
│   ├── api/                            # Complete API Reference
│   │   ├── core.md                    # Core API (elements, components)
│   │   ├── hooks.md                   # Hooks API (useState, useEffect, etc.)
│   │   ├── context.md                 # Context API (global state)
│   │   └── advanced.md                # Advanced features (refs, lazy, etc.)
│   │
│   ├── guides/                         # Practical Guides
│   │   ├── getting-started.md         # Your first React component
│   │   ├── components.md              # Component patterns & conventions
│   │   ├── project-structure.md       # Organizing your codebase
│   │   ├── file-naming.md             # File naming conventions
│   │   ├── component-organization.md  # Component structure patterns
│   │   └── ui-scaler.md               # Responsive design with usePx
│   │
│   └── examples/                       # Real-World Examples
│       ├── counter.md                 # Simple counter component
│       ├── form.md                    # Form with validation
│       ├── project-slither.md         # Production game UI reference
│       └── project-ui-labs.md         # Component library reference
└── docs/INDEX.md                       # Navigation and search guide
```

## Key Features

✅ **TypeScript First** - All examples use roblox-typescript  
✅ **Community Best Practices** - Patterns from modern Roblox projects  
✅ **Clear Conventions** - PascalCase components, kebab-case files  
✅ **Modern Packages** - ui-scaler, topbar-components, ripple, ultimate-list  
✅ **Practical Examples** - Real code ready to adapt  
✅ **Real-World References** - Slither, UI-Labs, and more  
✅ **Responsive Design** - usePx from @rbxts/ui-scaler  

## Documentation Structure

### For Beginners
1. Start with **[Getting Started Guide](./docs/guides/getting-started.md)**
2. Learn **[Core API](./docs/api/core.md)** concepts
3. Understand **[Component Patterns](./docs/guides/components.md)**
4. Review **[Project Structure](./docs/guides/project-structure.md)**

### For Intermediate Users
1. Master **[Hooks](./docs/api/hooks.md)**
2. Learn **[Context API](./docs/api/context.md)**
3. Study **[Responsive Design](./docs/guides/ui-scaler.md)**
4. Review **[Real-World Examples](./docs/examples/)**

### For Advanced Users
1. Explore **[Advanced Features](./docs/api/advanced.md)**
2. Study **[Project References](./docs/examples/)**
3. Design **[Component Systems](./docs/guides/component-organization.md)**
4. Build scalable architectures

## What's Covered

### React APIs
- ✅ Component creation (JSX and createElement)
- ✅ Functional components with TypeScript
- ✅ Hooks (useState, useEffect, useContext, useReducer, etc.)
- ✅ Context API for global state
- ✅ Refs and forwardRef
- ✅ Component composition patterns
- ✅ Roblox-specific event handling

### Patterns & Best Practices
- ✅ Component composition
- ✅ Higher-order components
- ✅ Render props pattern
- ✅ Custom hooks
- ✅ Container/presentational pattern
- ✅ Context providers
- ✅ Compound components
- ✅ Form handling
- ✅ List rendering with ultimate-list

### Project Organization
- ✅ Folder structure conventions
- ✅ File naming (kebab-case)
- ✅ Component naming (PascalCase)
- ✅ Scaling strategies
- ✅ Component libraries
- ✅ Shared utilities and hooks

### Modern Packages
- ✅ @rbxts/ui-scaler - Responsive design
- ✅ @rbxts/topbar-components - UI patterns
- ✅ @rbxts/ripple - Component libraries
- ✅ @rbxts/ultimate-list - List virtualization
- ✅ Pretty React Hooks - Custom hook patterns

### Real-World Examples
- ✅ Game UIs (Slither)
- ✅ Component libraries (UI-Labs)
- ✅ Simple components (Counter, Forms)

## What's NOT Covered

❌ Luau/Lua syntax - TypeScript only  
❌ Other state libraries - React only  
❌ Non-React Roblox APIs - use official Roblox docs  
❌ UI frameworks beyond React  
❌ Backend/server logic  
❌ Testing frameworks  

## Quick Links

| Need | Go To |
|------|-------|
| First component | [Getting Started](./docs/guides/getting-started.md) |
| API reference | [Core API](./docs/api/core.md), [Hooks](./docs/api/hooks.md) |
| Component patterns | [Component Patterns](./docs/guides/components.md) |
| Project structure | [Project Structure](./docs/guides/project-structure.md) |
| File/component naming | [File Naming](./docs/guides/file-naming.md) |
| Responsive design | [UI Scaler Guide](./docs/guides/ui-scaler.md) |
| Real-world reference | [Slither](./docs/examples/project-slither.md), [UI-Labs](./docs/examples/project-ui-labs.md) |
| Quick reference | [INDEX](./docs/INDEX.md) |

## Naming Conventions

### Components (PascalCase)
```typescript
const MyButton: React.FC<Props> = () => { ... }
const AlertDialog: React.FC<Props> = () => { ... }
```

### Files & Folders (kebab-case)
```
src/components/my-button/my-button.tsx
src/hooks/use-form.ts
src/utils/formatting.ts
```

### UI Sizing (usePx)
```typescript
import { usePx } from "@rbxts/ui-scaler"

const MyComponent: React.FC = () => {
  const px = usePx()
  return <frame Size={new UDim2(0, px(200), 0, px(50))} />
}
```

## Community References

This documentation incorporates patterns from:

1. **@rbxts/topbar-components**
   - Component export patterns
   - Composable UI components

2. **littensy/pretty-react-hooks**
   - Custom hook patterns
   - Reusable hook utilities

3. **@rbxts/ripple**
   - UI component library structure
   - Component composition

4. **PepeElToro41/ui-labs**
   - Design system approach
   - Theme management
   - Component organization

5. **@rbxts/ultimate-list**
   - List rendering patterns
   - Virtualization techniques

6. **@rbxts/ui-scaler**
   - Responsive design
   - usePx hook usage

7. **littensy/slither**
   - Production game UI
   - Complex state management

## Standards & Alignment

### Languages
- **roblox-typescript** - Type-safe development
- **React 17.0+** - Core React patterns
- **TypeScript** - Strong typing throughout

### References
- React JS: https://reactjs.org/docs (concepts apply)
- Roblox API: https://create.roblox.com/docs
- React-Lua: https://react.luau.page/

## Document Statistics

- **Total Pages**: 14+ Markdown files
- **API Documentation**: 4 files covering all major React APIs
- **Guides**: 6 beginner-to-advanced guides
- **Examples**: 4 practical examples and project references
- **Code Examples**: 100+ TypeScript examples
- **Focus**: React patterns only

## How to Use This MCP

This documentation is designed for AI assistants and developers:

1. **Search by topic** - Find relevant documentation by keywords
2. **Navigate with INDEX** - Use INDEX.md for quick lookups
3. **Follow examples** - Copy and adapt TypeScript examples
4. **Reference projects** - Study real-world implementations
5. **Check conventions** - Ensure your code follows standards

## Next Steps

1. **Choose your level**:
   - Beginner: [Getting Started](./docs/guides/getting-started.md)
   - Intermediate: [Hooks](./docs/api/hooks.md)
   - Advanced: [Advanced Features](./docs/api/advanced.md)

2. **Learn the conventions**:
   - [Project Structure](./docs/guides/project-structure.md)
   - [File Naming](./docs/guides/file-naming.md)
   - [UI Scaler](./docs/guides/ui-scaler.md)

3. **Build with examples**:
   - Study [Examples](./docs/examples/)
   - Reference [Real Projects](./docs/examples/project-slither.md)

4. **Use as reference**:
   - Bookmark [INDEX](./docs/INDEX.md)
   - Return to [API docs](./docs/api/) as needed

---

**MCP Version**: 2.0 (TypeScript Edition)  
**Focus**: React patterns with roblox-typescript  
**Updated**: 2026  
**Language**: TypeScript only  
**Scope**: React usage and best practices
