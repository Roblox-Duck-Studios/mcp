# Project Reference: UI-Labs

Component library and design system using React patterns.

**Repository**: https://github.com/PepeElToro41/ui-labs  
**Focus**: Reusable UI components, themes, and design patterns

## Project Organization

```
ui-labs/
├── src/
│   ├── UI/          # Component library
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Card/
│   │   └── ...other components
│   ├── Hooks/       # Custom hooks for UI
│   ├── Context/     # Context providers
│   ├── Themes/      # Theme management
│   ├── Stories/     # Component showcase/testing
│   ├── Utils/       # Utility functions
│   └── Plugin/      # Plugin-specific code
├── docs/            # Documentation
└── serve.project.json  # Serve configuration
```

## Component-First Architecture

UI-Labs demonstrates:
- **Component library design** - Reusable, well-organized components
- **Props-driven configuration** - Flexible component APIs
- **Type-safe components** - Full TypeScript support
- **Composition** - Building complex UIs from simple components

### Component Structure

Each component typically includes:
- Main component file
- TypeScript type definitions
- Props interface
- Default props
- Component variations/variants

Example pattern:
```lua
-- UI/Button/Button.tsx
export interface ButtonProps {
    label: string,
    onClick: (rbx: TextButton) -> nil,
    variant: "primary" | "secondary" | "ghost",
    size: "small" | "medium" | "large",
    disabled: boolean?
}

local function Button(props: ButtonProps)
    -- Implementation
end
```

## Theme Management

UI-Labs shows how to:
- **Define themes** - Color schemes, typography, spacing
- **Theme switching** - Runtime theme changes
- **Context integration** - Global theme access
- **Component theming** - Components respecting theme values

Pattern:
```lua
local ThemeContext = React.createContext(defaultTheme)

local function useTheme()
    return React.useContext(ThemeContext)
end

-- Components use useTheme() to access theme values
local function ThemedButton(props)
    local theme = useTheme()
    return React.createElement("TextButton", {
        BackgroundColor3 = theme.colors.primary
    })
end
```

## Custom Hooks

UI-Labs includes hooks for:
- **State management** - Form state, UI state
- **Theme usage** - `useTheme()` hook
- **Side effects** - Layout calculations, animations
- **Utilities** - Common UI patterns

Example:
```lua
local function useForm(initialValues, onSubmit)
    -- Form state and validation logic
    return { values, errors, handleChange, handleSubmit }
end
```

## Stories/Showcase Pattern

The "Stories" folder demonstrates:
- **Component showcasing** - How components look and behave
- **Documentation** - Interactive documentation
- **Testing** - Manual testing of components
- **Design reference** - Visual reference for developers

## Key Patterns

### 1. Props Interface Pattern
```lua
export interface ComponentProps {
    -- Configuration props
    label: string,
    variant: "primary" | "secondary",
    size: "small" | "medium" | "large",
    -- Event handlers
    onClick: (rbx: Instance) -> nil,
    -- Optional props
    disabled: boolean?
}
```

### 2. Compound Components
Group related components:
```lua
export { Card }
export { CardHeader }
export { CardContent }
export { CardFooter }

-- Usage
React.createElement(Card, {},
    React.createElement(CardHeader, { title = "Title" }),
    React.createElement(CardContent, {}, "Content"),
    React.createElement(CardFooter, {}, "Footer")
)
```

### 3. Variant Pattern
Different visual styles:
```lua
local variantStyles = {
    primary = { backgroundColor = Color3.fromRGB(59, 89, 152) },
    secondary = { backgroundColor = Color3.fromRGB(243, 114, 69) },
    ghost = { backgroundColor = Color3.new(1, 1, 1), borderColor = Color3.fromRGB(200, 200, 200) }
}
```

### 4. Context for Configuration
```lua
local ButtonGroupContext = React.createContext({
    variant = "primary",
    size = "medium"
})

local function ButtonGroup(props)
    return React.createElement(ButtonGroupContext.Provider, {
        value = { variant = props.variant, size = props.size }
    }, props.children)
end
```

## Design System Benefits

- **Consistency** - All UI follows same patterns
- **Reusability** - Components used across projects
- **Maintainability** - Centralized component logic
- **Scalability** - Easy to add new components
- **Type safety** - TypeScript ensures correct usage

## Organizational Insights

1. **Separation of concerns** - UI, hooks, context, utils clearly separated
2. **Component isolation** - Each component self-contained and testable
3. **Documentation** - Stories provide live documentation
4. **Theming support** - Built-in support for multiple themes
5. **Plugin integration** - Shows how to build plugins with React

## Lessons for Your Project

1. **Start with a component library** - Build reusable components early
2. **Use TypeScript** - Define clear prop interfaces
3. **Implement theming** - Plan for visual customization
4. **Document patterns** - Show examples of component usage
5. **Organize by feature** - Group related components together
6. **Create custom hooks** - Extract reusable logic into hooks

## Key Takeaway

UI-Labs demonstrates best practices for building a professional component library with React on Roblox, emphasizing reusability, type safety, theming, and clear organization.

## Pattern Examples

### Flexible Button Component
```lua
local function Button(props: ButtonProps)
    local theme = useTheme()
    local variantStyle = getVariantStyle(props.variant, theme)
    local sizeStyle = getSizeStyle(props.size)
    
    return React.createElement("TextButton", table.assign({},
        variantStyle,
        sizeStyle,
        {
            Text = props.label,
            [React.Event.Activated] = props.onClick,
            Disabled = props.disabled
        }
    ))
end
```

### Customizable Card
```lua
local function Card(props)
    return React.createElement("Frame", {
        Size = props.size or UDim2.fromOffset(300, 200),
        BackgroundColor3 = props.backgroundColor or Color3.new(1, 1, 1),
        BorderSizePixel = props.borderSize or 1
    }, props.children)
end
```

---

**See also**: [Slither Reference](./project-slither.md), [Component Patterns](../guides/components.md)
