# React in Roblox - MCP Documentation

This MCP (Model Context Protocol) documentation provides comprehensive information about using React with **roblox-typescript** for building UIs in Roblox.

## Overview

React-Lua is an implementation of React for Roblox, enabling declarative, component-based UI development. This documentation covers React patterns with **TypeScript best practices**:

- Core React API concepts with TypeScript
- Hooks for state and side effect management
- Component composition and patterns
- Real-world Roblox project examples
- Modern community conventions and standards
- Responsive design with ui-scaler

## Structure

```
react-roblox/
├── docs/
│   ├── api/                      # React API reference
│   │   ├── core.md               # Core API (createElement, etc.)
│   │   ├── hooks.md              # Hooks API (useState, useEffect, etc.)
│   │   ├── context.md            # Context API for global state
│   │   └── advanced.md           # Advanced features (refs, etc.)
│   ├── guides/
│   │   ├── getting-started.md    # Your first React component
│   │   ├── components.md         # Component patterns & best practices
│   │   ├── project-structure.md  # Project organization & conventions
│   │   ├── file-naming.md        # File naming conventions
│   │   ├── component-organization.md # Organizing components
│   │   └── ui-scaler.md          # Responsive design with usePx
│   └── examples/
│       ├── counter.md            # Simple counter component
│       ├── form.md               # Form with validation
│       ├── project-slither.md    # Production game UI reference
│       └── project-ui-labs.md    # Component library reference
└── INDEX.md                       # Quick navigation guide
```

## Key Concepts

### Functional Components (TypeScript)

```typescript
import React from "@rbxts/react"

interface HelloWorldProps {
  name: string
}

const HelloWorld: React.FC<HelloWorldProps> = ({ name }) => {
  return <textlabel Text={`Hello, ${name}`} Size={new UDim2(0, 200, 0, 50)} />
}

export default HelloWorld
```

### Hooks
- `useState` - State management
- `useEffect` - Side effects and lifecycle
- `useContext` - Context consumption
- `useCallback` - Memoize functions
- `useMemo` - Memoize values
- `useRef` - Direct instance access

### Project Structure (Community Best Practices)

Follow modern folder structure patterns adapted for Roblox:

```
src/
├── components/                   # Reusable UI components
│   ├── common/
│   │   ├── my-button/
│   │   │   ├── my-button.tsx
│   │   │   └── index.ts
│   │   └── my-card/
│   │       ├── my-card.tsx
│   │       └── index.ts
│   ├── layouts/
│   │   ├── app-layout/
│   │   │   ├── app-layout.tsx
│   │   │   └── index.ts
│   └── pages/
│       ├── home-page/
│       │   ├── home-page.tsx
│       │   └── index.ts
├── hooks/                        # Custom hooks
│   ├── use-form.ts
│   ├── use-theme.ts
│   └── index.ts
├── context/                      # Context providers
│   ├── theme-context.ts
│   ├── user-context.ts
│   └── index.ts
├── utils/                        # Utility functions
│   ├── formatting.ts
│   └── validation.ts
├── types/                        # Type definitions
│   ├── component-props.ts
│   └── models.ts
└── app.tsx                       # Root component
```

**Key Conventions:**
- 📝 **Component names**: PascalCase (`MyButton`, `AlertDialog`)
- 📁 **Files & folders**: kebab-case (`my-button`, `use-form`)
- 📏 **UI sizing**: Use `usePx` from `@rbxts/ui-scaler`

## Modern Community References

This documentation incorporates patterns from:

- **@rbxts/topbar-components** - Component export patterns
- **@rbxts/ripple** - UI component library structure
- **@rbxts/ultimate-list** - List rendering and virtualization
- **@rbxts/ui-scaler** - Responsive design with `usePx`
- **littensy/pretty-react-hooks** - Custom hook patterns
- **littensy/slither** - Production game UI
- **PepeElToro41/ui-labs** - Design systems and theming

## Getting Started

**Beginner Path:**
1. [Getting Started Guide](./docs/guides/getting-started.md) - Your first component
2. [Core API](./docs/api/core.md) - API fundamentals
3. [Component Patterns](./docs/guides/components.md) - Building with components
4. [Project Structure](./docs/guides/project-structure.md) - Organizing your code

**Intermediate Path:**
1. [Hooks Deep Dive](./docs/api/hooks.md) - Master hooks
2. [Context API](./docs/api/context.md) - Global state management
3. [UI Scaler Guide](./docs/guides/ui-scaler.md) - Responsive design
4. [Examples](./docs/examples/) - Real-world patterns

**Advanced Path:**
1. [Advanced Features](./docs/api/advanced.md) - Refs, lazy, etc.
2. [Project References](./docs/examples/) - Study production code
3. [Component Organization](./docs/guides/component-organization.md) - Scale your project

---

**Focus**: React patterns with roblox-typescript  
**Language**: TypeScript only (no Luau)  
**Based on**: React 17.0+, community best practices  
**Scope**: React usage and patterns
