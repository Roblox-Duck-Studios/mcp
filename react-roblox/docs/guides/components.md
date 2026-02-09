# Component Patterns

Common patterns and best practices for building React components in Roblox.

## Functional Components

The modern, recommended approach using hooks:

```lua
local function MyComponent(props)
    return React.createElement("Frame", {
        Size = props.size
    })
end
```

## Class Components

For complex state management and lifecycle control:

```lua
local MyComponent = React.Component:extend("MyComponent")

function MyComponent:init()
    self:setState({
        count = 0
    })
end

function MyComponent:render()
    return React.createElement("TextLabel", {
        Text = tostring(self.state.count)
    })
end
```

## Composition Over Inheritance

Build complex UIs by composing simpler components:

```lua
local function CardHeader(props)
    return React.createElement("TextLabel", {
        Text = props.title,
        Size = UDim2.fromScale(1, 0.1)
    })
end

local function CardContent(props)
    return React.createElement("Frame", {
        Size = UDim2.fromScale(1, 0.8),
        Position = UDim2.fromScale(0, 0.1)
    }, props.children)
end

local function Card(props)
    return React.createElement("Frame", {
        Size = props.size or UDim2.fromOffset(400, 300)
    },
        React.createElement(CardHeader, { title = props.title }),
        React.createElement(CardContent, {}, props.children)
    )
end
```

## Higher-Order Components (HOC)

Enhance components with additional functionality:

```lua
local function withTheme(Component)
    return function(props)
        local theme = React.useContext(ThemeContext)
        
        return React.createElement(Component, table.assign({}, props, {
            theme = theme
        }))
    end
end

-- Usage
local ThemedButton = withTheme(Button)
```

## Render Props Pattern

Pass rendering logic as a function:

```lua
local function DataProvider(props)
    local data, setData = React.useState(nil)
    
    React.useEffect(function()
        -- Fetch data
        setData({ id = 1, name = "Item" })
    end, {})
    
    return props.children(data)
end

-- Usage
React.createElement(DataProvider, {},
    function(data)
        return React.createElement("TextLabel", {
            Text = data and data.name or "Loading..."
        })
    end
)
```

## Custom Hooks Pattern

Extract reusable stateful logic:

```lua
local function useLocalStorage(key, initialValue)
    local value, setValue = React.useState(function()
        -- Load from storage on init
        local stored =--[[load from storage]]
        return stored or initialValue
    end)
    
    React.useEffect(function()
        -- Save to storage on change
        --[[save value]]
    end, { value })
    
    return value, setValue
end

-- Usage
local function Form()
    local name, setName = useLocalStorage("formName", "")
    
    return React.createElement("TextBox", {
        Text = name,
        [React.Event.FocusLost] = function(rbx)
            setName(rbx.Text)
        end
    })
end
```

## Container/Presentational Pattern

Separate data logic from UI:

```lua
-- Container (data logic)
local function UserListContainer(props)
    local users, setUsers = React.useState({})
    
    React.useEffect(function()
        -- Fetch users
        setUsers({ { id = 1, name = "Alice" }, { id = 2, name = "Bob" } })
    end, {})
    
    return React.createElement(UserListPresentation, {
        users = users,
        onSelectUser = function(userId)
            print("Selected:", userId)
        end
    })
end

-- Presentation (pure UI)
local function UserListPresentation(props)
    return React.createElement("ScrollingFrame", {
        Size = UDim2.fromScale(1, 1)
    },
        React.Children.map(props.users, function(user)
            return React.createElement("TextButton", {
                Text = user.name,
                [React.Event.Activated] = function()
                    props.onSelectUser(user.id)
                end
            })
        end)
    )
end
```

## Context Provider Pattern

Share global state across components:

```lua
local ThemeContext = React.createContext({
    darkMode = false
})

local function ThemeProvider(props)
    local darkMode, setDarkMode = React.useState(false)
    
    return React.createElement(ThemeContext.Provider, {
        value = {
            darkMode = darkMode,
            toggleDarkMode = function()
                setDarkMode(not darkMode)
            end
        }
    }, props.children)
end

-- Usage
local function App()
    return React.createElement(ThemeProvider, {},
        React.createElement(HomePage, {})
    )
end
```

## Conditional Rendering

Render different components based on state/props:

```lua
local function Greeting(props)
    if props.isLoggedIn then
        return React.createElement("TextLabel", {
            Text = "Welcome, " .. props.userName
        })
    else
        return React.createElement("TextLabel", {
            Text = "Please log in"
        })
    end
end

-- Or using ternary
local function Message(props)
    return React.createElement("TextLabel", {
        Text = if props.error then "Error occurred" else "All good"
    })
end

-- Or returning nil to render nothing
local function OptionalContent(props)
    return props.showContent and React.createElement("Frame", {}) or nil
end
```

## List Rendering

Render lists efficiently:

```lua
local function TodoList(props)
    return React.createElement("ScrollingFrame", {
        Size = UDim2.fromScale(1, 1)
    },
        React.Children.map(props.todos, function(todo, index)
            return React.createElement("TextLabel", {
                Text = todo.text,
                LayoutOrder = index,
                -- Always provide unique keys for lists
                key = todo.id  -- Important!
            })
        end)
    )
end

-- With UIListLayout for automatic layout
local function AutoLayoutList(props)
    return React.createElement("Frame", {
        Size = UDim2.fromScale(1, 1),
        AutomaticSize = Enum.AutomaticSize.Y
    },
        React.createElement("UIListLayout", {
            Padding = UDim.new(0, 10),
            HorizontalAlignment = Enum.HorizontalAlignment.Left
        }),
        React.Children.map(props.items, function(item, index)
            return React.createElement("TextLabel", {
                Text = item,
                LayoutOrder = index,
                Size = UDim2.fromScale(1, 0),
                AutomaticSize = Enum.AutomaticSize.Y
            })
        end)
    )
end
```

## Form Handling

Managing form state:

```lua
local function useFormInput(initialValue)
    local value, setValue = React.useState(initialValue or "")
    
    return {
        value = value,
        onChange = function(newValue)
            setValue(newValue)
        end,
        reset = function()
            setValue(initialValue or "")
        end
    }
end

local function ContactForm()
    local name = useFormInput("")
    local email = useFormInput("")
    
    return React.createElement("Frame", {},
        React.createElement("TextBox", {
            Text = name.value,
            PlaceholderText = "Name",
            [React.Event.FocusLost] = function(rbx)
                name.onChange(rbx.Text)
            end
        }),
        React.createElement("TextBox", {
            Text = email.value,
            PlaceholderText = "Email",
            [React.Event.FocusLost] = function(rbx)
                email.onChange(rbx.Text)
            end
        }),
        React.createElement("TextButton", {
            Text = "Submit",
            [React.Event.Activated] = function()
                print("Submitting:", name.value, email.value)
                name.reset()
                email.reset()
            end
        })
    )
end
```

## Performance Optimization

Memoize components and callbacks to prevent unnecessary re-renders:

```lua
-- Memoize expensive component
local ExpensiveComponent = React.memo(function(props)
    -- Only re-renders if props change
    return React.createElement("Frame", {})
end)

-- Memoize callbacks
local function Parent()
    local handleClick = React.useCallback(function()
        print("Clicked")
    end, {})
    
    return React.createElement(ChildButton, {
        onClick = handleClick
    })
end

-- Memoize computed values
local function FilteredList(props)
    local filtered = React.useMemo(function()
        return table.filter(props.items, props.filterFn)
    end, { props.items, props.filterFn })
    
    return React.createElement("Frame", {}, props.children(filtered))
end
```

---

**See also**: [Getting Started](./getting-started.md), [Hooks API](../api/hooks.md)
