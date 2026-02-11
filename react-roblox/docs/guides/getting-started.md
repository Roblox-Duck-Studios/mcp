# Getting Started

## Introduction

React Roblox brings React's declarative programming model to the Roblox platform. It is split into two key packages:

- **`@rbxts/react@alpha`** - The core React library containing all internal logic
- **`@rbxts/react-roblox@alpha`** - React DOM equivalent for Roblox, providing the rendering system

Every concept in React JS applies to Roblox, but with Roblox's own rendering system and some slight deviations to accommodate the Luau language and Roblox engine.

**Key Philosophy**: React Roblox maintains API alignment with React JS where possible, while introducing Roblox-specific features for better integration with the platform.

## React vs React Roblox

| Aspect | React (JS) | React Roblox |
|--------|------------|--------------|
| **Logic Package** | `react` | `@rbxts/react` |
| **DOM Package** | `react-dom` | `@rbxts/react-roblox` |
| **Language** | JavaScript/TypeScript | TypeScript → Luau |
| **Rendering Target** | Browser DOM | Roblox GUI instances |
| **Component Model** | Classes or Functions | Classes or Functions |

## Why React on Roblox?

1. **Declarative UI** - Describe what your UI should look like at any given state
2. **Component Reusability** - Build modular, reusable components
3. **State Management** - Easy state and lifecycle management with hooks
4. **Developer Experience** - Familiar patterns from React JS
5. **Type Safety** - Full TypeScript support for catching errors early

## JSX in React Roblox

React Roblox supports JSX syntax, which gets compiled to `React.createElement` calls:

```tsx
// JSX
const element = <frame Size={new UDim2(1, 0, 1, 0)} />

// Compiled equivalent
const element = React.createElement("frame", { Size: new UDim2(1, 0, 1, 0) })
```

## Installation

### Basic Installation

```bash
npm install @rbxts/react @rbxts/react-roblox
```

### Full Ecosystem Installation

```bash
# Core
npm install @rbxts/react @rbxts/react-roblox

# Development & Testing
npm install @rbxts/ui-labs

# Animation
npm install @rbxts/ripple

# Utility Hooks
npm install pretty-react-hooks

# Lifecycle Management
npm install @rbxts/react-lifetime-component

# Virtualized Lists
npm install @rbxts/ultimate-list
```
