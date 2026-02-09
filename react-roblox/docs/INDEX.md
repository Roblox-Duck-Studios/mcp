# Index

Quick navigation guide for react-roblox MCP documentation.

## Getting Started

Begin here if you're new to React in Roblox:

1. **[Getting Started Guide](./guides/getting-started.md)** - Your first React component
2. **[Project Structure](./guides/project-structure.md)** - How to organize your code
3. **[Component Patterns](./guides/components.md)** - Common patterns and best practices

## API Reference

Complete reference for React APIs:

### Core API
- **[React.createElement, Components, Refs](./api/core.md)** - Creating elements and components
  - React.createElement
  - React.Component
  - React.PureComponent
  - React.memo
  - React.forwardRef
  - React.createRef
  - React.Children utilities
  - Context.Provider / Consumer

### Hooks
- **[State, Effects, Context Hooks](./api/hooks.md)** - Modern functional component patterns
  - useState
  - useEffect
  - useContext
  - useReducer
  - useCallback
  - useMemo
  - useRef
  - useImperativeHandle
  - useLayoutEffect

### Context
- **[Context API](./api/context.md)** - Sharing data across components
  - createContext
  - Provider pattern
  - Consumer pattern
  - useContext hook
  - Real-world examples

### Advanced
- **[Advanced Features](./api/advanced.md)** - Performance and integration
  - React.lazy
  - Error Boundaries
  - useBinding (Roblox-specific)
  - Compound components
  - External data integration

## Examples

Learn by example:

### Basic Examples
- **[Counter](./examples/counter.md)** - Simple state management
- **[Form](./examples/form.md)** - Form handling and validation

### Real-World Projects
- **[Slither](./examples/project-slither.md)** - Game UI architecture
- **[UI-Labs](./examples/project-ui-labs.md)** - Component library patterns

## Quick Reference

### Creating a Component

**Functional Component:**
```lua
local function MyComponent(props)
    return React.createElement("Frame", {
        Size = UDim2.fromScale(1, 1)
    })
end
```

**Class Component:**
```lua
local MyComponent = React.Component:extend("MyComponent")

function MyComponent:render()
    return React.createElement("Frame", {})
end
```

### Using Hooks

```lua
local function MyComponent(props)
    local count, setCount = React.useState(0)
    
    React.useEffect(function()
        -- Side effect code
    end, {})
    
    local theme = React.useContext(ThemeContext)
    
    return React.createElement("TextLabel", {
        Text = tostring(count)
    })
end
```

### Creating Context

```lua
local MyContext = React.createContext(defaultValue)

local function Provider(props)
    return React.createElement(MyContext.Provider, {
        value = { /* data */ }
    }, props.children)
end

local function useMyContext()
    return React.useContext(MyContext)
end
```

## Key Concepts

| Concept | Purpose | Example |
|---------|---------|---------|
| **Element** | Describes UI | `React.createElement(...)` |
| **Component** | Reusable UI unit | Function or class |
| **Props** | Configuration | `{ label = "Click" }` |
| **State** | Mutable data | `React.useState(0)` |
| **Effect** | Side effects | `React.useEffect(...)` |
| **Context** | Global data | `React.createContext(...)` |
| **Hook** | Stateful logic | `useState`, `useEffect`, etc. |
| **Ref** | Direct access | `React.useRef(nil)` |

## Common Tasks

### How do I...

**Create a button?**
```lua
React.createElement("TextButton", {
    Text = "Click me",
    [React.Event.Activated] = function() end
})
```

**Manage state?**
```lua
local value, setValue = React.useState(initialValue)
```

**Handle side effects?**
```lua
React.useEffect(function()
    -- Code runs after render
    return function()
        -- Cleanup code
    end
end, { dependencies })
```

**Pass data to children?**
```lua
React.createElement(MyContext.Provider, {
    value = dataToShare
}, props.children)
```

**Optimize rendering?**
```lua
local memoized = React.useMemo(function()
    return expensiveComputation()
end, { dependencies })
```

## Troubleshooting

### Component not re-rendering
- Check `useState` is being called at top level
- Verify state is being updated with `setState`, not mutated
- Ensure dependencies in `useEffect` are correct

### State not updating
- Use setter function: `setValue(newValue)`
- For objects, create new table: `setState({ ...state, key = value })`
- Remember state updates may be batched

### Context not updating children
- Ensure `Provider` wraps children
- Check context value is being provided
- Use `useContext` at top level of component

### Performance issues
- Use `React.memo` for expensive components
- Memoize callbacks with `useCallback`
- Memoize values with `useMemo`
- Check for unnecessary re-renders

## Resources

**Official Documentation:**
- React-Lua: https://react.luau.page/
- React Concepts (applies to React-Lua): https://reactjs.org/docs
- Roblox API: https://create.roblox.com/docs

**Real Examples:**
- [Slither Repository](https://github.com/littensy/slither)
- [UI-Labs Repository](https://github.com/PepeElToro41/ui-labs)

## Standards

This documentation follows:
- **Facebook's React project structure recommendations**
- **React API and patterns from React 17.0.1**
- **Roblox-Lua best practices**
- **TypeScript/roblox-ts conventions**

---

**Last updated**: 2026  
**Scope**: React usage patterns only (no other dependencies)
