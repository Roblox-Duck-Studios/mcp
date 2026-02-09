# React in Roblox - MCP Documentation

This MCP (Model Context Protocol) documentation provides comprehensive information about using React (React-Lua) for building UIs in Roblox with TypeScript/Luau.

## Overview

React-Lua is an implementation of React for the Luau language, enabling declarative UI development on the Roblox platform. This documentation covers:

- Core React API concepts
- Hooks for state management
- Component patterns and lifecycle
- Real-world project examples
- Best practices aligned with official React recommendations

## Structure

```
react-roblox/
├── docs/
│   ├── api/                    # React API reference
│   │   ├── core.md            # Core API (createElement, etc.)
│   │   ├── hooks.md           # Hooks API
│   │   ├── context.md         # Context API
│   │   └── advanced.md        # Advanced features
│   ├── guides/
│   │   ├── getting-started.md # Beginner guide
│   │   ├── components.md      # Component patterns
│   │   ├── state-management.md # State and effects
│   │   └── project-structure.md # Folder organization
│   └── examples/
│       ├── counter.md         # Simple counter
│       ├── form.md            # Form handling
│       └── reflex-integration.md # State management
├── projects/
│   ├── slither/               # Real-world example
│   └── ui-labs/               # Component library example
└── src/
    └── code-examples/         # Runnable examples
```

## Key Concepts

### Functional Components
```lua
local function MyComponent(props)
    return React.createElement("TextLabel", {
        Text = props.text
    })
end
```

### Hooks
- `useState` - State management
- `useEffect` - Side effects
- `useContext` - Context consumption
- `useCallback` - Function memoization
- `useMemo` - Value memoization
- `useRef` - Direct instance access

### Project Structure (Facebook/Official Recommendations)

Follow the official React folder structure patterns adapted for Roblox:

```
src/
├── components/           # Reusable UI components
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Card.tsx
├── hooks/               # Custom hooks
│   ├── useForm.ts
│   └── useTheme.ts
├── context/             # Context providers
│   ├── ThemeContext.ts
│   └── UserContext.ts
├── pages/               # Page-level components
│   └── HomePage.tsx
├── utils/               # Utility functions
│   └── formatting.ts
└── types/               # Type definitions
    └── models.ts
```

## References

- **Official React Lua Documentation**: https://react.luau.page/api-reference/react/
- **React JS Concepts**: https://reactjs.org/docs (concepts apply to React-Lua)
- **Roblox Engine API**: https://create.roblox.com/docs

## Real-World Examples

### Slither (littensy/slither)
A game built with React patterns demonstrating:
- Complex state management
- Component composition
- Event handling and Roblox-specific integrations

### UI-Labs (PepeElToro41/ui-labs)
A component library and design system showing:
- Reusable component patterns
- Theme management with Context
- Plugin development
- Custom hooks for UI utilities

## Getting Started

1. Start with [Getting Started Guide](./docs/guides/getting-started.md)
2. Learn [Core API Concepts](./docs/api/core.md)
3. Understand [Hooks](./docs/api/hooks.md)
4. Review [Component Patterns](./docs/guides/components.md)
5. Study [Project Structure](./docs/guides/project-structure.md)

---

**Note**: This MCP focuses exclusively on React usage patterns. For Roblox-specific APIs not related to React, consult the official Roblox documentation.
