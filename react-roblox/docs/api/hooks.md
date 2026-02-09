# Hooks API

Hooks allow functional components to have state and side effects. They're the modern way to write React components.

## React.useState

Adds state to a functional component.

```lua
local value, setValue = React.useState(initialValue)
```

### Parameters
- `initialValue` (any): Initial state value or function returning initial value
- Returns: `(currentValue, setterFunction)`

### Setter Function
- Can be called with a new value: `setValue(newValue)`
- Can be called with an updater function: `setValue(function(prevValue) return newValue end)`

### Example

**Simple counter:**
```lua
local function Counter(props)
    local count, setCount = React.useState(0)
    
    return React.createElement("Frame", {},
        React.createElement("TextLabel", {
            Text = "Count: " .. tostring(count)
        }),
        React.createElement("TextButton", {
            Text = "Increment",
            [React.Event.Activated] = function()
                setCount(count + 1)
            end
        })
    )
end
```

**With updater function:**
```lua
local function Counter(props)
    local count, setCount = React.useState(0)
    
    return React.createElement("TextButton", {
        Text = tostring(count),
        [React.Event.Activated] = function()
            -- Updater function ensures we use latest state
            setCount(function(prevCount)
                return prevCount + 1
            end)
        end
    })
end
```

## React.useEffect

Runs side effects after render. Replaces lifecycle methods for functional components.

```lua
React.useEffect(function()
    -- Effect code runs here
    
    return function()
        -- Cleanup function (optional)
    end
end, dependencies)
```

### Parameters
- `effectFunction` (function): Runs after render, can return cleanup function
- `dependencies` (table | nil): Dependencies array
  - If omitted: runs after every render
  - If empty: runs only after first render
  - If contains values: runs when any dependency changes

### Examples

**Setup and cleanup:**
```lua
local function MouseTracker(props)
    local mousePos, setMousePos = React.useState(Vector2.new(0, 0))
    local UserInputService = game:GetService("UserInputService")
    
    React.useEffect(function()
        local connection = UserInputService.InputChanged:Connect(function(input, gameProcessed)
            if input.UserInputType == Enum.UserInputType.MouseMovement then
                setMousePos(input.Position)
            end
        end)
        
        return function()
            connection:Disconnect()
        end
    end, {})
    
    return React.createElement("TextLabel", {
        Text = string.format("Mouse: (%.0f, %.0f)", mousePos.X, mousePos.Y)
    })
end
```

**With dependencies:**
```lua
local function DataFetcher(props)
    local data, setData = React.useState(nil)
    
    React.useEffect(function()
        -- Runs when props.userId changes
        print("Fetching data for user:", props.userId)
        -- Fetch logic here
    end, { props.userId })
    
    return React.createElement("TextLabel", {
        Text = data or "Loading..."
    })
end
```

## React.useContext

Reads a context value provided by a parent component.

```lua
local contextValue = React.useContext(ContextObject)
```

### Example

**Theme context:**
```lua
local ThemeContext = React.createContext({
    darkMode = false,
    primary = Color3.new(1, 1, 1)
})

local function ThemedButton(props)
    local theme = React.useContext(ThemeContext)
    
    return React.createElement("TextButton", {
        BackgroundColor3 = theme.primary,
        Text = props.label
    })
end

-- App setup
React.createElement(ThemeContext.Provider, {
    value = { darkMode = true, primary = Color3.new(0, 0, 0) }
},
    React.createElement(ThemedButton, { label = "Dark Button" })
)
```

## React.useReducer

Manages complex state with a reducer function.

```lua
local state, dispatch = React.useReducer(reducerFunction, initialState)
```

### Example

**Todo list reducer:**
```lua
local function reducer(state, action)
    if action.type == "add" then
        return {
            todos = {...state.todos, action.todo},
            count = state.count + 1
        }
    elseif action.type == "remove" then
        return {
            todos = {...(function()
                local new = {}
                for i, todo in ipairs(state.todos) do
                    if i ~= action.index then
                        table.insert(new, todo)
                    end
                end
                return new
            end)()},
            count = state.count - 1
        }
    end
end

local function TodoApp(props)
    local state, dispatch = React.useReducer(reducer, {
        todos = {},
        count = 0
    })
    
    return React.createElement("Frame", {},
        React.createElement("TextLabel", {
            Text = "Todos: " .. tostring(state.count)
        }),
        React.createElement("TextButton", {
            Text = "Add Todo",
            [React.Event.Activated] = function()
                dispatch({ type = "add", todo = "New task" })
            end
        })
    )
end
```

## React.useCallback

Memoizes a callback function. Use to prevent unnecessary re-renders of child components.

```lua
local memoizedCallback = React.useCallback(function(...)
    -- Function body
end, dependencies)
```

### Example

```lua
local function Parent(props)
    local onClick = React.useCallback(function(value)
        print("Item clicked:", value)
    end, {})
    
    return React.createElement(Child, {
        onItemClick = onClick
    })
end
```

## React.useMemo

Memoizes a computed value. Use for expensive calculations.

```lua
local memoizedValue = React.useMemo(function()
    -- Expensive computation
    return computedValue
end, dependencies)
```

### Example

```lua
local function FilteredList(props)
    local filtered = React.useMemo(function()
        return table.filter(props.items, function(item)
            return string.find(item.name, props.searchText) ~= nil
        end)
    end, { props.items, props.searchText })
    
    return React.createElement("Frame", {},
        -- Render filtered items
    )
end
```

## React.useRef

Creates a mutable ref that persists across renders without causing re-renders.

```lua
local ref = React.useRef(initialValue)
-- Access with: ref.current
```

### Examples

**Direct DOM access:**
```lua
local function TextBoxWithFocus(props)
    local textBoxRef = React.useRef(nil)
    
    return React.createElement("Frame", {},
        React.createElement("TextBox", {
            ref = textBoxRef
        }),
        React.createElement("TextButton", {
            Text = "Focus",
            [React.Event.Activated] = function()
                textBoxRef.current:CaptureFocus()
            end
        })
    )
end
```

**Storing mutable values:**
```lua
local function Timer(props)
    local timerRef = React.useRef(0)
    
    React.useEffect(function()
        local connection
        connection = game:GetService("RunService").Heartbeat:Connect(function(deltaTime)
            timerRef.current = timerRef.current + deltaTime
            if timerRef.current > 5 then
                connection:Disconnect()
            end
        end)
        
        return function()
            if connection then connection:Disconnect() end
        end
    end, {})
    
    return React.createElement("TextLabel", {
        Text = string.format("Time: %.1f", timerRef.current)
    })
end
```

## React.useImperativeHandle

Customizes the ref exposed by a component when using `forwardRef`.

```lua
React.useImperativeHandle(ref, function()
    return {
        customMethod = function() end,
        customProp = value
    }
end, dependencies)
```

### Example

```lua
local ScrollFrame = React.forwardRef(function(props, ref)
    local frameRef = React.useRef(nil)
    
    React.useImperativeHandle(ref, function()
        return {
            scrollToTop = function()
                frameRef.current.CanvasPosition = Vector2.new(0, 0)
            end,
            scrollToBottom = function()
                frameRef.current.CanvasPosition = Vector2.new(0, frameRef.current.CanvasSize.Y.Offset)
            end
        }
    end, {})
    
    return React.createElement("ScrollingFrame", {
        ref = frameRef,
        Size = UDim2.fromScale(1, 1)
    })
end)
```

## React.useLayoutEffect

Like `useEffect`, but runs synchronously after DOM mutations. Use sparingly.

```lua
React.useLayoutEffect(function()
    -- Runs synchronously after render
    return function()
        -- Cleanup
    end
end, dependencies)
```

## Rules of Hooks

1. **Only call hooks at the top level** - Don't call hooks inside loops, conditions, or nested functions
2. **Only call hooks from React components** - Call from functional components or custom hooks, not regular functions
3. **Use custom hooks** - Extract hook logic into custom hooks for reusability

## Custom Hooks

Create reusable hook logic by extracting into functions starting with "use".

```lua
-- Custom hook
local function useFormInput(initialValue)
    local value, setValue = React.useState(initialValue)
    
    return {
        value = value,
        onChange = function(newValue)
            setValue(newValue)
        end,
        reset = function()
            setValue(initialValue)
        end
    }
end

-- Usage
local function Form(props)
    local username = useFormInput("")
    local email = useFormInput("")
    
    return React.createElement("Frame", {},
        React.createElement("TextBox", {
            Text = username.value,
            [React.Event.FocusLost] = function(rbx)
                username.onChange(rbx.Text)
            end
        }),
        React.createElement("TextBox", {
            Text = email.value,
            [React.Event.FocusLost] = function(rbx)
                email.onChange(rbx.Text)
            end
        })
    )
end
```

---

**See also**: [Core API](./core.md), [Advanced Features](./advanced.md)
