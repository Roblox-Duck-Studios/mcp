# Context API

Managing global state and shared data through React Context.

## React.createContext

Creates a context object for sharing data across the component tree.

```lua
local MyContext = React.createContext(defaultValue)
```

### Parameters
- `defaultValue` (any): Default value if no provider is found

### Returns
A context object with `Provider` and `Consumer` components

## Context.Provider

Provides a value to all descendant components:

```lua
React.createElement(MyContext.Provider, {
    value = { theme = "dark", fontSize = 14 }
},
    -- Child components
)
```

### Usage Example

```lua
local ThemeContext = React.createContext({ theme = "light" })

local function App()
    return React.createElement(ThemeContext.Provider, {
        value = { theme = "dark", primaryColor = Color3.new(0, 0, 0) }
    },
        React.createElement(MainContent, {})
    )
end

local function MainContent()
    return React.createElement(React.Fragment, nil,
        React.createElement(Header, {}),
        React.createElement(Body, {}),
        React.createElement(Footer, {})
    )
end
```

## Context.Consumer

Reads context values using render props pattern:

```lua
React.createElement(MyContext.Consumer, nil, function(value)
    return React.createElement("TextLabel", {
        Text = value.theme
    })
end)
```

### Example

```lua
local ThemeContext = React.createContext({ theme = "light" })

local function ThemedButton()
    return React.createElement(ThemeContext.Consumer, nil, function(theme)
        local bgColor = theme.theme == "dark" and Color3.new(0, 0, 0) or Color3.new(1, 1, 1)
        
        return React.createElement("TextButton", {
            Text = "Styled Button",
            BackgroundColor3 = bgColor
        })
    end)
end
```

## useContext Hook (Recommended)

Modern approach using the `useContext` hook:

```lua
local value = React.useContext(MyContext)
```

### Example

```lua
local ThemeContext = React.createContext({
    darkMode = false,
    primaryColor = Color3.new(1, 1, 1)
})

local function ThemedComponent()
    local theme = React.useContext(ThemeContext)
    
    return React.createElement("Frame", {
        BackgroundColor3 = theme.darkMode and Color3.new(0, 0, 0) or Color3.new(1, 1, 1)
    })
end
```

## Multi-Context Setup

Combine multiple contexts:

```lua
local ThemeContext = React.createContext({ dark = false })
local UserContext = React.createContext({ name = "Guest" })
local NotificationContext = React.createContext({ message = "" })

local function AppProviders(props)
    return React.createElement(ThemeContext.Provider, {
        value = { dark = true }
    },
        React.createElement(UserContext.Provider, {
            value = { name = "Alice", id = 123 }
        },
            React.createElement(NotificationContext.Provider, {
                value = { message = "Welcome!" }
            },
                props.children
            )
        )
    )
end

-- Usage
React.createElement(AppProviders, {},
    React.createElement(HomePage, {})
)

-- Access in components
local function Component()
    local theme = React.useContext(ThemeContext)
    local user = React.useContext(UserContext)
    local notification = React.useContext(NotificationContext)
    
    return React.createElement("TextLabel", {
        Text = string.format("Hello %s, Theme: %s", user.name, theme.dark and "dark" or "light")
    })
end
```

## Provider Components with State

Wrap context with stateful logic:

```lua
local ThemeContext = React.createContext({
    darkMode = false,
    toggleTheme = function() end
})

local function ThemeProvider(props)
    local darkMode, setDarkMode = React.useState(false)
    
    return React.createElement(ThemeContext.Provider, {
        value = {
            darkMode = darkMode,
            toggleTheme = function()
                setDarkMode(not darkMode)
            end,
            colors = {
                background = darkMode and Color3.new(0.1, 0.1, 0.1) or Color3.new(1, 1, 1),
                text = darkMode and Color3.new(1, 1, 1) or Color3.new(0, 0, 0)
            }
        }
    }, props.children)
end

-- Usage
React.createElement(ThemeProvider, {},
    React.createElement(App, {})
)
```

## Pattern: Custom Context Hook

Create a custom hook for cleaner context consumption:

```lua
local UserContext = React.createContext(nil)

local function UserProvider(props)
    local user, setUser = React.useState(nil)
    
    React.useEffect(function()
        -- Fetch user data
        setUser({ id = 1, name = "Alice", email = "alice@example.com" })
    end, {})
    
    return React.createElement(UserContext.Provider, {
        value = { user = user, setUser = setUser }
    }, props.children)
end

-- Custom hook
local function useUser()
    local context = React.useContext(UserContext)
    
    if not context then
        error("useUser must be used inside UserProvider")
    end
    
    return context
end

-- Usage in component
local function UserProfile()
    local context = useUser()
    
    return React.createElement("TextLabel", {
        Text = context.user and context.user.name or "Loading..."
    })
end
```

## Real-World Example: Theme System

```lua
local ThemeContext = React.createContext({
    primaryColor = Color3.fromRGB(59, 89, 152),
    secondaryColor = Color3.fromRGB(243, 114, 69),
    fontSize = 12
})

local THEMES = {
    light = {
        primaryColor = Color3.fromRGB(59, 89, 152),
        secondaryColor = Color3.fromRGB(243, 114, 69),
        backgroundColor = Color3.new(1, 1, 1),
        textColor = Color3.new(0, 0, 0),
        fontSize = 12
    },
    dark = {
        primaryColor = Color3.fromRGB(100, 150, 200),
        secondaryColor = Color3.fromRGB(255, 150, 100),
        backgroundColor = Color3.fromRGB(30, 30, 30),
        textColor = Color3.new(1, 1, 1),
        fontSize = 12
    }
}

local function ThemeProvider(props)
    local themeName, setThemeName = React.useState("light")
    local currentTheme = THEMES[themeName]
    
    return React.createElement(ThemeContext.Provider, {
        value = table.assign({}, currentTheme, {
            themeName = themeName,
            setThemeName = setThemeName
        })
    }, props.children)
end

-- Usage
local function App()
    return React.createElement(ThemeProvider, {},
        React.createElement(MainContent, {})
    )
end

local function ThemedButton(props)
    local theme = React.useContext(ThemeContext)
    
    return React.createElement("TextButton", {
        Text = props.label,
        BackgroundColor3 = theme.primaryColor,
        TextColor3 = theme.textColor,
        TextSize = theme.fontSize,
        [React.Event.Activated] = function()
            -- Toggle theme
            theme.setThemeName(theme.themeName == "light" and "dark" or "light")
        end
    })
end
```

## Pattern: Combining Context with Reducer

Complex state management:

```lua
local StateContext = React.createContext(nil)
local DispatchContext = React.createContext(nil)

local function reducer(state, action)
    if action.type == "INCREMENT" then
        return { count = state.count + 1 }
    elseif action.type == "DECREMENT" then
        return { count = state.count - 1 }
    elseif action.type == "RESET" then
        return { count = 0 }
    end
    return state
end

local function CounterProvider(props)
    local state, dispatch = React.useReducer(reducer, { count = 0 })
    
    return React.createElement(StateContext.Provider, {
        value = state
    },
        React.createElement(DispatchContext.Provider, {
            value = dispatch
        }, props.children)
    )
end

-- Custom hooks
local function useCounterState()
    local context = React.useContext(StateContext)
    if not context then
        error("useCounterState must be used inside CounterProvider")
    end
    return context
end

local function useCounterDispatch()
    local context = React.useContext(DispatchContext)
    if not context then
        error("useCounterDispatch must be used inside CounterProvider")
    end
    return context
end

-- Usage
local function Counter()
    local state = useCounterState()
    local dispatch = useCounterDispatch()
    
    return React.createElement("Frame", {},
        React.createElement("TextLabel", {
            Text = "Count: " .. tostring(state.count)
        }),
        React.createElement("TextButton", {
            Text = "Increment",
            [React.Event.Activated] = function()
                dispatch({ type = "INCREMENT" })
            end
        }),
        React.createElement("TextButton", {
            Text = "Decrement",
            [React.Event.Activated] = function()
                dispatch({ type = "DECREMENT" })
            end
        })
    )
end
```

## Performance Considerations

- Context causes re-renders of all consuming components when value changes
- Split contexts by update frequency
- Use memoization to prevent unnecessary re-renders

```lua
local function OptimizedProvider(props)
    local data, setData = React.useState({ ... })
    
    -- Memoize the value to prevent unnecessary re-renders
    local value = React.useMemo(function()
        return {
            data = data,
            setData = setData
        }
    end, { data })
    
    return React.createElement(MyContext.Provider, {
        value = value
    }, props.children)
end
```

---

**See also**: [Core API](./core.md), [Hooks API](./hooks.md)
