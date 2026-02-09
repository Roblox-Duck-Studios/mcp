# Core React API

Core API for creating and managing React elements in Roblox.

## React.createElement

Creates a new React element.

```lua
React.createElement(type, props, ...children)
```

### Parameters
- `type` (string | function | class): The component type
  - String: Roblox instance (e.g., "Frame", "TextLabel")
  - Function: Functional component
  - Class: React.Component subclass
- `props` (table | nil): Properties and event handlers
- `...children` (variable): Child elements

### Returns
A React element representing the component

### Examples

**Basic element:**
```lua
local frame = React.createElement("Frame", {
    Size = UDim2.fromScale(1, 1),
    BackgroundColor3 = Color3.new(1, 1, 1)
})
```

**With children:**
```lua
local container = React.createElement("Frame", {
    Size = UDim2.fromScale(1, 1)
}, 
    React.createElement("TextLabel", { Text = "Child 1" }),
    React.createElement("TextLabel", { Text = "Child 2" })
)
```

**With functional component:**
```lua
local function MyButton(props)
    return React.createElement("TextButton", {
        Text = props.label,
        Size = UDim2.fromOffset(100, 50)
    })
end

local button = React.createElement(MyButton, { label = "Click me" })
```

## React.Component

Base class for class components. Use `:extend()` to create subclasses.

```lua
local MyComponent = React.Component:extend("MyComponent")

function MyComponent:init()
    self:setState({ count = 0 })
end

function MyComponent:render()
    return React.createElement("TextLabel", {
        Text = tostring(self.state.count)
    })
end

function MyComponent:componentDidMount()
    -- Runs after component mounts
end

function MyComponent:componentDidUpdate(prevProps, prevState)
    -- Runs after props or state change
end

function MyComponent:componentWillUnmount()
    -- Runs before component unmounts
    -- Clean up resources here
end
```

### Lifecycle Methods
- `init()` - Constructor (initialize state)
- `componentDidMount()` - After first render
- `componentDidUpdate(prevProps, prevState)` - After update
- `componentWillUnmount()` - Before removal

### Methods
- `self:setState(table | function)` - Update state and trigger re-render
- `self:forceUpdate()` - Force re-render without state change

## React.PureComponent

Like `React.Component` but with automatic shallow prop/state comparison for optimization.

```lua
local OptimizedComponent = React.PureComponent:extend("OptimizedComponent")

function OptimizedComponent:render()
    return React.createElement("TextLabel", {
        Text = self.props.text
    })
end

-- Component only re-renders if props change
```

## React.memo

Wraps a functional component to memoize it. Use only when performance optimization is needed.

```lua
local ExpensiveComponent = React.memo(function(props)
    return React.createElement("Frame", {
        -- Complex rendering logic
    })
end)
```

## React.Fragment

Renders multiple elements without creating a parent element.

```lua
return React.createElement(React.Fragment, nil,
    React.createElement("TextLabel", { Text = "Item 1" }),
    React.createElement("TextLabel", { Text = "Item 2" })
)
```

## React.createRef

Creates a ref to access underlying Roblox instances directly.

```lua
local MyComponent = React.Component:extend("MyComponent")

function MyComponent:init()
    self.textBoxRef = React.createRef()
end

function MyComponent:render()
    return React.createElement("TextBox", {
        ref = self.textBoxRef
    })
end

function MyComponent:componentDidMount()
    -- Access the TextBox instance
    self.textBoxRef.current:CaptureFocus()
end
```

## React.forwardRef

Forwards a ref from a parent component to a child component.

```lua
local FancyButton = React.forwardRef(function(props, ref)
    return React.createElement("TextButton", {
        ref = ref,
        Text = props.text,
        [React.Event.Activated] = props.onClick
    })
end)

-- Parent component can now get direct ref to TextButton
local ref = React.createRef()
React.createElement(FancyButton, {
    ref = ref,
    text = "Click me",
    onClick = function() print("Clicked") end
})
```

## React.cloneElement

Clones an element with modified props.

```lua
local original = React.createElement("TextLabel", { Text = "Original" })
local cloned = React.cloneElement(original, { Text = "Cloned" })
```

## React.isValidElement

Checks if a value is a valid React element.

```lua
if React.isValidElement(props.content) then
    return props.content
else
    return React.createElement("TextLabel", { Text = "Invalid content" })
end
```

## React.Children

Utilities for working with the `children` prop.

### React.Children.map
Transforms each child element.

```lua
React.Children.map(props.children, function(child, index)
    return React.cloneElement(child, { LayoutOrder = index })
end)
```

### React.Children.forEach
Iterates over children without creating new elements.

```lua
React.Children.forEach(props.children, function(child, index)
    print("Child", index, child)
end)
```

### React.Children.count
Returns the number of children.

```lua
local childCount = React.Children.count(props.children)
```

### React.Children.only
Asserts that there is exactly one child.

```lua
local onlyChild = React.Children.only(props.children)
```

### React.Children.toArray
Converts children to an array for manipulation.

```lua
local childArray = React.Children.toArray(props.children)
table.sort(childArray, function(a, b) return a.props.priority > b.props.priority end)
```

## Roblox-Specific APIs

### React.Event
Connect to Roblox events within props.

```lua
React.createElement("TextButton", {
    [React.Event.Activated] = function(rbx)
        print("Button clicked:", rbx.Name)
    end,
    [React.Event.MouseEnter] = function(rbx)
        print("Mouse entered")
    end
})
```

### React.Change
Listen to property changes.

```lua
React.createElement("Frame", {
    [React.Change.AbsoluteSize] = function(rbx)
        print("Size changed:", rbx.AbsoluteSize)
    end
})
```

### React.Tag
Tag system for Roblox instances.

```lua
React.createElement("Frame", {
    [React.Tag] = "myTag"
})
```

### React.None
Represents "no value" (use instead of nil for clarity).

```lua
React.createElement("TextLabel", {
    Text = condition and "Value" or React.None
})
```

## Context API

### React.createContext

Creates a context object for passing data through the component tree.

```lua
local ThemeContext = React.createContext(defaultTheme)

-- Provider component
React.createElement(ThemeContext.Provider, {
    value = { darkMode = true, primaryColor = Color3.new(0, 0, 0) }
},
    -- Child components
)

-- Consumer component
React.createElement(ThemeContext.Consumer, nil, function(theme)
    return React.createElement("Frame", {
        BackgroundColor3 = theme.primaryColor
    })
end)
```

---

**See also**: [Hooks API](./hooks.md), [Advanced Features](./advanced.md)
