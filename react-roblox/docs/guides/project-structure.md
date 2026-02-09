# Project Structure

Recommended folder organization for React Roblox projects, aligned with Facebook's official React project structure recommendations.

## Standard Folder Layout

```
src/
├── components/
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Form/
│   │   ├── FormInput.tsx
│   │   ├── FormCheckbox.tsx
│   │   └── Form.tsx
│   └── Layout/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       ├── Footer.tsx
│       └── Layout.tsx
├── hooks/
│   ├── useForm.ts
│   ├── useTheme.ts
│   ├── useAuth.ts
│   └── useLocalStorage.ts
├── context/
│   ├── ThemeContext.tsx
│   ├── AuthContext.tsx
│   └── UserContext.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── ProfilePage.tsx
│   └── SettingsPage.tsx
├── utils/
│   ├── formatting.ts
│   ├── validation.ts
│   └── helpers.ts
├── types/
│   └── models.ts
├── constants/
│   ├── colors.ts
│   └── config.ts
└── client/
    └── init.client.tsx
```

## Directory Guide

### `components/`

Reusable UI building blocks. Each component should:
- Be focused on a single responsibility
- Accept configuration through props
- Be testable in isolation
- Not contain business logic (keep that in hooks/context)

```lua
-- components/Button.tsx
local function Button(props)
    return React.createElement("TextButton", {
        Text = props.label,
        Size = props.size or UDim2.fromOffset(100, 50),
        BackgroundColor3 = props.color,
        [React.Event.Activated] = props.onClick
    })
end

return Button
```

**Organizing by domain:**
```
components/
├── Common/              # Shared across app
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Card.tsx
├── Form/               # Form-related components
│   ├── FormInput.tsx
│   ├── FormCheckbox.tsx
│   └── FormButton.tsx
└── Navigation/         # Navigation components
    ├── NavBar.tsx
    └── NavItem.tsx
```

### `hooks/`

Reusable stateful logic. Custom hooks for:
- State management patterns
- API interaction
- Local storage
- Form handling
- Custom business logic

```lua
-- hooks/useForm.ts
local function useForm(initialValues, onSubmit)
    local values, setValues = React.useState(initialValues)
    local errors, setErrors = React.useState({})
    
    return {
        values = values,
        errors = errors,
        handleChange = function(name, value)
            setValues(table.assign({}, values, { [name] = value }))
        end,
        handleSubmit = function()
            onSubmit(values)
        end
    }
end

return useForm
```

### `context/`

Global state providers. Organize by feature:

```lua
-- context/ThemeContext.tsx
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
            end
        }
    }, props.children)
end

return {
    Provider = ThemeProvider,
    Context = ThemeContext
}
```

### `pages/`

Top-level page components that:
- Combine multiple components
- Manage page-level state
- Integrate context providers
- Handle page-specific logic

```lua
-- pages/HomePage.tsx
local function HomePage(props)
    local data, setData = React.useState(nil)
    
    React.useEffect(function()
        -- Load page data
    end, {})
    
    return React.createElement("Frame", {
        Size = UDim2.fromScale(1, 1)
    },
        React.createElement(Header, {}),
        React.createElement("Frame", {}, 
            -- Page content
        ),
        React.createElement(Footer, {})
    )
end

return HomePage
```

### `utils/`

Utility functions for:
- String formatting
- Validation
- Math operations
- Data transformation
- Helpers

```lua
-- utils/formatting.ts
local function formatCurrency(amount)
    return "$" .. string.format("%.2f", amount)
end

local function formatDate(date)
    return os.date("%Y-%m-%d", date)
end

return {
    formatCurrency = formatCurrency,
    formatDate = formatDate
}
```

### `types/`

TypeScript/Luau type definitions:

```lua
-- types/models.ts
type User = {
    id: number,
    name: string,
    email: string,
    createdAt: number
}

type Post = {
    id: number,
    title: string,
    content: string,
    author: User,
    publishedAt: number
}

return {}
```

### `constants/`

Application constants:

```lua
-- constants/colors.ts
return {
    PRIMARY = Color3.fromRGB(59, 89, 152),
    SECONDARY = Color3.fromRGB(243, 114, 69),
    SUCCESS = Color3.fromRGB(46, 204, 113),
    ERROR = Color3.fromRGB(231, 76, 60),
    WARNING = Color3.fromRGB(241, 196, 15),
    NEUTRAL = Color3.fromRGB(127, 140, 141)
}
```

### `client/`

Application entry point:

```lua
-- client/init.client.tsx
import React from "@react-lua/react"
import ReactRoblox from "@react-lua/react-roblox"
import App from "../pages/App"

local root = ReactRoblox.createRoot(game.Players.LocalPlayer:WaitForChild("PlayerGui"))
root:render(React.createElement(App))
```

## Real-World Examples

### Slither Project Structure
- **src/client** - Client entry points
- **src/server** - Server logic
- **src/shared** - Shared utilities and components
- Demonstrates multi-environment React usage

### UI-Labs Project Structure
- **src/UI** - Component library
- **src/Hooks** - Custom hooks
- **src/Context** - Context providers
- **src/Stories** - Component showcase
- **src/Themes** - Theme management
- Shows component library best practices

## Naming Conventions

### Components
- PascalCase: `Button.tsx`, `UserCard.tsx`
- Descriptive names: `UserProfileCard` not `Card2`

### Hooks
- Start with "use": `useForm.ts`, `useAuth.ts`
- Describe what they do: `useLocalStorage` not `useStorage`

### Utilities
- camelCase: `formatting.ts`, `validation.ts`
- Clear purpose: `stringFormatting` not `utils`

### Context
- Name after domain: `ThemeContext.tsx`, `AuthContext.tsx`
- Provider component: `ThemeProvider`, `AuthProvider`

## File Organization Tips

1. **One component per file** - Easy to find and maintain
2. **Index exports** - Optional, but helps with clean imports
3. **Group related files** - Put Form components in Form/ folder
4. **Separate concerns** - Keep components, hooks, and utils separate
5. **Share across pages** - Components go in components/, page-specific logic in pages/

### Example Index File

```lua
-- components/Form/index.tsx
export { default as Form } from "./Form"
export { default as FormInput } from "./FormInput"
export { default as FormCheckbox } from "./FormCheckbox"
```

Then import cleanly:
```lua
import { Form, FormInput } from "components/Form"
```

## Growing Your Project

As your project grows:

1. **Extract features** - Separate admin, settings, etc. into feature folders
2. **Create shared libraries** - Move reusable components to packages
3. **Split stores** - Organize context by feature
4. **Lazy load** - Use React.lazy for code splitting (advanced)

---

**See also**: [Getting Started](./getting-started.md), [Component Patterns](./components.md)
