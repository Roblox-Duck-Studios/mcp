# React in Roblox - Quick Reference Card

## File Organization

```
react-roblox/
├── README.md                    ← Start here
├── MCP_OVERVIEW.md             ← What this MCP covers
└── docs/
    ├── INDEX.md                ← Navigation guide
    ├── api/                    ← Complete API reference
    │   ├── core.md            (createElement, Component, etc.)
    │   ├── hooks.md           (useState, useEffect, etc.)
    │   ├── context.md         (createContext, Provider, etc.)
    │   └── advanced.md        (lazy, memo, etc.)
    ├── guides/                 ← How-to guides
    │   ├── getting-started.md
    │   ├── components.md
    │   └── project-structure.md
    └── examples/               ← Working examples
        ├── counter.md
        ├── form.md
        ├── project-slither.md
        └── project-ui-labs.md
```

## API at a Glance

### Components
```lua
-- Functional (recommended)
local function MyComponent(props) ... end

-- Class
local MyComponent = React.Component:extend("MyComponent")
function MyComponent:render() ... end

-- With ref forwarding
React.forwardRef(function(props, ref) ... end)

-- Memoized
React.memo(function(props) ... end)
```

### Hooks
```lua
-- State
local value, setValue = React.useState(initial)

-- Side effects
React.useEffect(function() ... end, { dependencies })

-- Context
local value = React.useContext(MyContext)

-- Reducer
local state, dispatch = React.useReducer(reducer, initial)

-- Memoization
local memoized = React.useMemo(function() ... end, { deps })
local callback = React.useCallback(function() ... end, { deps })

-- References
local ref = React.useRef(initial)
```

### Context
```lua
local MyContext = React.createContext(defaultValue)

React.createElement(MyContext.Provider, { value = ... }, children)
React.createElement(MyContext.Consumer, nil, function(value) ... end)
```

### Roblox Integration
```lua
-- Events
[React.Event.Activated] = function(rbx) ... end
[React.Event.MouseEnter] = function(rbx) ... end

-- Property changes
[React.Change.AbsoluteSize] = function(rbx) ... end

-- Tag system
[React.Tag] = "myTag"

-- No value
Text = condition and "Value" or React.None
```

## Common Patterns

### Form Input
```lua
local function useFormInput(initial)
    local value, setValue = React.useState(initial or "")
    return {
        value = value,
        onChange = setValue,
        reset = function() setValue(initial or "") end
    }
end
```

### Custom Hook
```lua
local function useMyHook(param)
    local state, setState = React.useState(param)
    
    React.useEffect(function()
        -- Setup
        return function() -- Cleanup
        end
    end, { param })
    
    return { state, setState }
end
```

### Context Provider
```lua
local MyContext = React.createContext(defaultValue)

local function MyProvider(props)
    local value = { /* data */ }
    return React.createElement(MyContext.Provider, {
        value = value
    }, props.children)
end
```

## Decision Tree

```
Need to build a component?
├─ Simple UI without state?
│  └─ → Use Functional Component
├─ Need state or effects?
│  └─ → Use Hooks (useState, useEffect)
├─ Expensive computation?
│  └─ → Use useMemo or useCallback
├─ Share data across components?
│  └─ → Use Context
├─ Complex state logic?
│  └─ → Use useReducer or Hooks
└─ Need performance optimization?
   └─ → Use React.memo or useMemo
```

## Props Pattern
```lua
local function Button(props: {
    label: string,
    onClick: (rbx: TextButton) -> nil,
    disabled: boolean?
})
    return React.createElement("TextButton", {
        Text = props.label,
        [React.Event.Activated] = props.onClick,
        Disabled = props.disabled
    })
end
```

## Event Handling
```lua
-- Button click
[React.Event.Activated] = function(rbx) print("Clicked") end

-- Input change
[React.Event.FocusLost] = function(rbx) print(rbx.Text) end

-- Mouse events
[React.Event.MouseEnter] = function(rbx) ... end
[React.Event.MouseLeave] = function(rbx) ... end

-- With state update
[React.Event.Activated] = function()
    setState(function(prev)
        return prev + 1
    end)
end
```

## State Updates
```lua
-- Direct value
setValue(newValue)

-- Function (uses previous state)
setValue(function(prev)
    return prev + 1
end)

-- Multiple values
setState(table.assign({}, state, { key = newValue }))

-- Don't: setState(state) - mutates directly
-- Do: setState({ ...state, key = newValue }) - new table
```

## Dependency Rules
```lua
-- Run once on mount
React.useEffect(function() ... end, {})

-- Run on every render
React.useEffect(function() ... end)

-- Run when value changes
React.useEffect(function() ... end, { value })

-- Tip: Include all values used inside
React.useEffect(function()
    print(value) -- value must be in dependencies
end, { value })
```

## Performance Tips
```lua
-- Memoize expensive component
local Expensive = React.memo(MyComponent)

-- Cache callbacks
local onClick = React.useCallback(function()
    -- handler
end, { /* deps */ })

-- Cache computed values
local filtered = React.useMemo(function()
    return table.filter(items, fn)
end, { items })
```

## Project Structure Template
```
src/
├── components/       # Reusable UI
│   ├── Button.tsx
│   └── Form/
│       └── Input.tsx
├── hooks/           # Custom hooks
│   └── useForm.ts
├── context/         # Providers
│   └── ThemeContext.tsx
├── pages/           # Page components
│   └── Home.tsx
├── utils/           # Helpers
│   └── formatting.ts
├── types/           # Types
│   └── models.ts
└── client/          # Entry point
    └── init.client.tsx
```

## Debugging
```lua
-- Log renders
local function MyComponent()
    print("Rendering MyComponent")
    return ...
end

-- Check state updates
local state, setState = React.useState(0)
React.useEffect(function()
    print("State changed:", state)
end, { state })

-- Inspect props
print("Props:", props)
```

## Common Mistakes
```lua
❌ Calling hooks inside conditions
✅ Always call hooks at top level

❌ Mutating state directly
✅ Use setState function

❌ Missing dependencies
✅ Include all values in dependency array

❌ Not cleaning up effects
✅ Return cleanup function from useEffect

❌ Using string keys in lists
✅ Use unique, stable keys (IDs, not indexes)

❌ Context without Provider
✅ Wrap components in context Provider
```

## Quick Help

| Task | Solution |
|------|----------|
| Create component | Function returning React.createElement |
| Add state | useState hook |
| Run side effects | useEffect hook |
| Share data | Context (createContext + Provider) |
| Handle input | useRef or controlled with state |
| Optimize rendering | React.memo, useMemo, useCallback |
| Access DOM | useRef with ref prop |
| Listen to events | [React.Event.EventName] |

## Links
- **Full Docs**: See README.md
- **Navigation**: See docs/INDEX.md
- **Examples**: See docs/examples/
- **API Ref**: See docs/api/
- **Guides**: See docs/guides/

---
**Use this card while coding for quick lookups**
