# Core React API

Core API for creating and managing React components in Roblox TypeScript using JSX syntax.

## JSX Syntax (Recommended)

The recommended way to write React components in roblox-ts is using JSX syntax. JSX transpiles to function calls under the hood:

```typescript
// JSX syntax
const MyFrame: React.FC = () => {
  return <frame Size={new UDim2(1, 0, 1, 0)} />
}

// Equivalent to:
const MyFrameVerbose: React.FC = () => {
  return React.createElement("frame", { Size: new UDim2(1, 0, 1, 0) })
}
```

**Use JSX for readability** - it's cleaner and more intuitive.

## JSX Elements and Children

Create elements with Roblox instances as JSX tags:

```typescript
// Basic element
const SimpleFrame: React.FC = () => {
  return <frame Size={new UDim2(1, 0, 1, 0)} BackgroundColor3={new Color3(1, 1, 1)} />
}

// With children
const FrameWithChildren: React.FC = () => {
  return (
    <frame Size={new UDim2(1, 0, 1, 0)}>
      <textlabel Text="Child 1" />
      <textlabel Text="Child 2" />
    </frame>
  )
}

// With component children
interface CardProps {
  title: string
  children?: React.ReactNode
}

const Card: React.FC<CardProps> = ({ title, children }) => {
  return (
    <frame>
      <textlabel Text={title} />
      {children}
    </frame>
  )
}

// Usage
const App: React.FC = () => (
  <Card title="My Card">
    <textlabel Text="Card content" />
  </Card>
)
```

## Functional Components

The modern standard for React components in TypeScript:

```typescript
// Simple functional component
const HelloWorld: React.FC = () => {
  return <textlabel Text="Hello, World!" />
}

// With typed props
interface GreetingProps {
  name: string
  age?: number
}

const Greeting: React.FC<GreetingProps> = ({ name, age }) => {
  return (
    <frame>
      <textlabel Text={`Hello, ${name}`} />
      {age && <textlabel Text={`Age: ${age}`} />}
    </frame>
  )
}

// With default props
interface ButtonProps {
  label: string
  onClick?: () => void
  size?: UDim2
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  size = new UDim2(0, 100, 0, 50),
}) => {
  return (
    <textbutton
      Text={label}
      Size={size}
      Event={{ Activated: onClick }}
    />
  )
}
```

## Memoization

Use `React.memo` to prevent unnecessary re-renders when props haven't changed:

```typescript
interface ExpensiveComponentProps {
  data: unknown
  isLoading?: boolean
}

const ExpensiveComponent = React.memo<ExpensiveComponentProps>(({ data, isLoading }) => {
  // This component only re-renders when `data` or `isLoading` changes
  if (isLoading) {
    return <textlabel Text="Loading..." />
  }
  return <textlabel Text={tostring(data)} />
})

// Custom comparison for memoization
interface ComparisonProps {
  id: number
  name: string
}

const CustomMemo = React.memo<ComparisonProps>(
  ({ id, name }) => {
    return <textlabel Text={`${id}: ${name}`} />
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (don't re-render)
    return prevProps.id === nextProps.id
  }
)
```

## Fragments

Render multiple elements without creating a wrapper element:

```typescript
const Fragment: React.FC = () => {
  return (
    <>
      <textlabel Text="Item 1" />
      <textlabel Text="Item 2" />
      <textlabel Text="Item 3" />
    </>
  )
}

// Equivalent to:
const FragmentVerbose: React.FC = () => {
  return (
    <React.Fragment>
      <textlabel Text="Item 1" />
      <textlabel Text="Item 2" />
      <textlabel Text="Item 3" />
    </React.Fragment>
  )
}
```

## Refs and Direct Instance Access

Use refs to access Roblox instances directly when needed:

```typescript
import React, { useRef } from "@rbxts/react"

interface TextInputProps {
  placeholder?: string
}

const TextInput: React.FC<TextInputProps> = ({ placeholder }) => {
  const textBoxRef = useRef<TextBox>(null)

  const handleFocus = () => {
    if (textBoxRef.current) {
      textBoxRef.current.CaptureFocus()
    }
  }

  return (
    <>
      <textbox ref={textBoxRef} PlaceholderText={placeholder} />
      <textbutton Text="Focus" Event={{ Activated: handleFocus }} />
    </>
  )
}
```

**Use refs sparingly** - prefer controlled components with state when possible.

## Forwarding Refs

Forward refs from parent to child components:

```typescript
import React, { forwardRef } from "@rbxts/react"

interface FancyButtonProps {
  text: string
  onClick?: () => void
}

const FancyButton = forwardRef<TextButton, FancyButtonProps>(
  ({ text, onClick }, ref) => {
    return (
      <textbutton
        ref={ref}
        Text={text}
        Event={{ Activated: onClick }}
      />
    )
  }
)

// Parent component can access the TextButton directly
const ParentComponent: React.FC = () => {
  const buttonRef = useRef<TextButton>(null)

  return (
    <FancyButton
      ref={buttonRef}
      text="Click me"
      onClick={() => {
        if (buttonRef.current) {
          print("Button clicked:", buttonRef.current.Name)
        }
      }}
    />
  )
}
```

## Roblox-Specific Props

### Event Handlers

Use the `Event` prop object to handle Roblox events:

```typescript
const InteractiveFrame: React.FC = () => {
  return (
    <frame
      Size={new UDim2(1, 0, 1, 0)}
      Event={{
        MouseEnter: (rbx: Frame) => {
          print("Mouse entered frame:", rbx.Name)
        },
        MouseLeave: (rbx: Frame) => {
          print("Mouse left frame")
        },
      }}
    >
      <textbutton
        Text="Click me"
        Event={{
          Activated: (rbx: TextButton) => {
            print("Button activated")
          },
          MouseButton1Down: (rbx: TextButton) => {
            print("Mouse button 1 down")
          },
        }}
      />
    </frame>
  )
}
```

### Change Handlers

Listen to property changes with the `Change` prop:

```typescript
interface SizeChangeProps {
  onSizeChange?: (size: Vector2) => void
}

const SizeTracker: React.FC<SizeChangeProps> = ({ onSizeChange }) => {
  return (
    <frame
      Size={new UDim2(1, 0, 1, 0)}
      Change={{
        AbsoluteSize: (rbx: Frame) => {
          onSizeChange?.(rbx.AbsoluteSize)
        },
      }}
    />
  )
}
```

### Tags

Apply Roblox tags to instances:

```typescript
const TaggedFrame: React.FC = () => {
  return (
    <frame
      Tags={["interactive", "ui-element"]}
    />
  )
}
```

## Context API

### Creating Context

```typescript
import React, { createContext, useContext } from "@rbxts/react"

interface Theme {
  primaryColor: Color3
  secondaryColor: Color3
  darkMode: boolean
}

interface ThemeContextType {
  theme: Theme
  toggleDarkMode: () => void
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider")
  }
  return context
}
```

### Provider Component

```typescript
import React, { useState } from "@rbxts/react"

interface ThemeProviderProps {
  children?: React.ReactNode
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false)

  const theme: Theme = {
    primaryColor: darkMode ? Color3.fromRGB(50, 50, 50) : Color3.fromRGB(0, 0, 255),
    secondaryColor: Color3.fromRGB(200, 200, 200),
    darkMode,
  }

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleDarkMode: () => setDarkMode(!darkMode),
      }}
    >
      {children}
    </ThemeContext.Provider>
  )
}
```

### Consuming Context

```typescript
const ThemedButton: React.FC = () => {
  const { theme } = useTheme()

  return (
    <textbutton
      Text="Click me"
      BackgroundColor3={theme.primaryColor}
    />
  )
}

// In your app
const App: React.FC = () => (
  <ThemeProvider>
    <ThemedButton />
  </ThemeProvider>
)
```

## Conditional Rendering

Render content conditionally based on state or props:

```typescript
interface MessageProps {
  type: "success" | "error" | "info"
  text: string
}

const Message: React.FC<MessageProps> = ({ type, text }) => {
  // Early return pattern
  if (type === "success") {
    return <textlabel Text={text} TextColor3={Color3.fromRGB(0, 255, 0)} />
  }

  if (type === "error") {
    return <textlabel Text={text} TextColor3={Color3.fromRGB(255, 0, 0)} />
  }

  return <textlabel Text={text} TextColor3={Color3.fromRGB(100, 100, 100)} />
}

// Ternary operator
const Greeting: React.FC<{ isLoggedIn: boolean; userName?: string }> = ({
  isLoggedIn,
  userName,
}) => {
  return (
    <textlabel Text={isLoggedIn ? `Welcome, ${userName}` : "Please log in"} />
  )
}

// Logical AND operator
const OptionalContent: React.FC<{ show: boolean }> = ({ show }) => {
  return show && <textlabel Text="This is shown conditionally" />
}
```

## List Rendering

Render lists of elements with proper keys:

```typescript
interface Item {
  id: number
  name: string
  price: number
}

interface ItemListProps {
  items: Item[]
  onSelectItem?: (id: number) => void
}

const ItemList: React.FC<ItemListProps> = ({ items, onSelectItem }) => {
  return (
    <scrollingframe
      Size={new UDim2(1, 0, 1, 0)}
      CanvasSize={new UDim2(0, 0, 0, items.size() * 40)}
    >
      <uilistlayout />
      {items.map((item) => (
        <textbutton
          key={item.id}
          Text={`${item.name} - $${item.price}`}
          Size={new UDim2(1, 0, 0, 40)}
          Event={{
            Activated: () => onSelectItem?.(item.id),
          }}
        />
      ))}
    </scrollingframe>
  )
}
```

**Important:** Always use a unique, stable `key` prop (not array indices):

```typescript
// ❌ Bad - keys based on array index change when list is reordered
items.map((item, index) => <frame key={index} />)

// ✅ Good - keys are stable identifiers
items.map((item) => <frame key={item.id} />)
```

## Children Patterns

Work with the `children` prop in various ways:

```typescript
// Simple children
interface ContainerProps {
  children?: React.ReactNode
}

const Container: React.FC<ContainerProps> = ({ children }) => {
  return (
    <frame Size={new UDim2(1, 0, 1, 0)} BackgroundTransparency={0.5}>
      {children}
    </frame>
  )
}

// Multiple named "slots"
interface TabsProps {
  tabBar?: React.ReactNode
  content?: React.ReactNode
}

const Tabs: React.FC<TabsProps> = ({ tabBar, content }) => {
  return (
    <frame Size={new UDim2(1, 0, 1, 0)}>
      <frame Size={new UDim2(1, 0, 0, 40)}>
        {tabBar}
      </frame>
      <frame Position={new UDim2(0, 0, 0, 40)} Size={new UDim2(1, 0, 1, -40)}>
        {content}
      </frame>
    </frame>
  )
}

// React.Children utilities
import React from "@rbxts/react"

interface ListProps {
  children?: React.ReactNode
}

const List: React.FC<ListProps> = ({ children }) => {
  const childCount = React.Children.count(children)

  return (
    <frame>
      <textlabel Text={`Number of items: ${childCount}`} />
      <frame>
        {React.Children.map(children, (child, index) => (
          <frame key={index} LayoutOrder={index}>
            {child}
          </frame>
        ))}
      </frame>
    </frame>
  )
}
```

---

**See also**: [Hooks API](./hooks.md), [Advanced Features](./advanced.md)
