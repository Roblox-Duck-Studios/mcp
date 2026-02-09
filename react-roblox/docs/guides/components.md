# Component Patterns and Best Practices

Common patterns and best practices for building React components in Roblox with **roblox-typescript**.

## Functional Components (Recommended)

The modern approach using hooks and TypeScript:

```typescript
// src/components/my-frame/my-frame.tsx
import React from "@rbxts/react"

interface MyFrameProps {
  size?: UDim2
}

const MyFrame: React.FC<MyFrameProps> = ({ size = new UDim2(1, 0, 1, 0) }) => {
  return <frame Size={size} />
}

export default MyFrame
```

**Conventions:**
- Component name: `MyFrame` (PascalCase)
- File name: `my-frame.tsx` (kebab-case)
- Props interface: `MyFrameProps`

## Composition Over Inheritance

Build complex UIs by combining simpler components:

```typescript
// src/components/card/card.tsx
import React from "@rbxts/react"

interface CardHeaderProps {
  title: string
}

const CardHeader: React.FC<CardHeaderProps> = ({ title }) => (
  <textlabel Text={title} Size={new UDim2(1, 0, 0.1, 0)} />
)

interface CardContentProps {
  children?: React.ReactNode
}

const CardContent: React.FC<CardContentProps> = ({ children }) => (
  <frame Size={new UDim2(1, 0, 0.8, 0)} Position={new UDim2(0, 0, 0.1, 0)}>
    {children}
  </frame>
)

interface CardProps {
  title: string
  size?: UDim2
  children?: React.ReactNode
}

const Card: React.FC<CardProps> = ({
  title,
  size = new UDim2(0, 400, 0, 300),
  children,
}) => (
  <frame Size={size}>
    <CardHeader title={title} />
    <CardContent>{children}</CardContent>
  </frame>
)

export default Card
```

**Key Points:**
- Each sub-component has its own interface
- Child components are exported if reusable
- Main component is the default export

## Higher-Order Components (HOC)

Enhance components with additional functionality:

```typescript
// src/utils/with-theme.ts
import React from "@rbxts/react"
import { ThemeContext, Theme } from "@/context/theme-context"

interface WithThemeProps {
  theme: Theme
}

export function withTheme<P extends WithThemeProps>(
  Component: React.ComponentType<P>
): React.FC<Omit<P, "theme">> {
  const WithThemeComponent: React.FC<Omit<P, "theme">> = (props) => {
    const theme = React.useContext(ThemeContext)
    return <Component {...(props as P)} theme={theme} />
  }
  return WithThemeComponent
}
```

Usage:
```typescript
// src/components/themed-button/themed-button.tsx
interface ThemedButtonProps extends WithThemeProps {
  text: string
  onClick?: () => void
}

const ThemedButton: React.FC<ThemedButtonProps> = ({
  theme,
  text,
  onClick,
}) => (
  <textbutton
    Text={text}
    BackgroundColor3={theme.primaryColor}
    Event={{ Activated: onClick }}
  />
)

export default withTheme(ThemedButton)
```

## Custom Hooks Pattern

Extract reusable stateful logic into hooks:

```typescript
// src/hooks/use-local-storage.ts
import React, { useState, useEffect } from "@rbxts/react"

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(() => {
    // Load from storage on init
    // (Implementation depends on your storage solution)
    return initialValue
  })

  useEffect(() => {
    // Save to storage whenever value changes
    // (Implementation depends on your storage solution)
  }, [value])

  return [value, setValue]
}
```

Usage:
```typescript
// src/components/persistent-form/persistent-form.tsx
import { useLocalStorage } from "@/hooks/use-local-storage"

const PersistentForm: React.FC = () => {
  const [name, setName] = useLocalStorage("formName", "")

  return (
    <textbox
      Text={name}
      PlaceholderText="Enter name"
      Event={{
        FocusLost: (rbx: TextBox) => setName(rbx.Text),
      }}
    />
  )
}

export default PersistentForm
```

## Container/Presentational Pattern

Separate data logic from UI rendering:

```typescript
// src/components/user-list/user-list-presentation.tsx
export interface UserListPresentationProps {
  users: User[]
  onSelectUser: (userId: number) => void
  isLoading?: boolean
}

const UserListPresentation: React.FC<UserListPresentationProps> = ({
  users,
  onSelectUser,
  isLoading,
}) => {
  if (isLoading) {
    return <textlabel Text="Loading..." />
  }

  return (
    <scrollingframe Size={new UDim2(1, 0, 1, 0)}>
      <uilistlayout />
      {users.map((user) => (
        <textbutton
          key={user.id}
          Text={user.name}
          Event={{
            Activated: () => onSelectUser(user.id),
          }}
        />
      ))}
    </scrollingframe>
  )
}

export default UserListPresentation
```

```typescript
// src/components/user-list/user-list-container.tsx
import { useState, useEffect } from "@rbxts/react"
import UserListPresentation from "./user-list-presentation"

interface User {
  id: number
  name: string
}

const UserListContainer: React.FC = () => {
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Fetch users
    setUsers([
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" },
    ])
    setIsLoading(false)
  }, [])

  return (
    <UserListPresentation
      users={users}
      isLoading={isLoading}
      onSelectUser={(userId) => console.log("Selected:", userId)}
    />
  )
}

export default UserListContainer
```

## Context Provider Pattern

Share global state across the component tree:

```typescript
// src/context/theme-context.ts
import React from "@rbxts/react"

export interface Theme {
  primaryColor: Color3
  secondaryColor: Color3
  darkMode: boolean
}

export const ThemeContext = React.createContext<Theme>({
  primaryColor: Color3.fromRGB(0, 0, 255),
  secondaryColor: Color3.fromRGB(200, 200, 200),
  darkMode: false,
})
```

```typescript
// src/components/theme-provider/theme-provider.tsx
import React, { useState } from "@rbxts/react"
import { ThemeContext, Theme } from "@/context/theme-context"

interface ThemeProviderProps {
  children?: React.ReactNode
}

const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false)

  const theme: Theme = {
    primaryColor: darkMode
      ? Color3.fromRGB(50, 50, 50)
      : Color3.fromRGB(255, 255, 255),
    secondaryColor: Color3.fromRGB(200, 200, 200),
    darkMode,
  }

  return (
    <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
  )
}

export default ThemeProvider
```

## Conditional Rendering

Render different components based on state or props:

```typescript
interface GreetingProps {
  isLoggedIn: boolean
  userName?: string
}

const Greeting: React.FC<GreetingProps> = ({ isLoggedIn, userName }) => {
  return (
    <textlabel
      Text={isLoggedIn ? `Welcome, ${userName}` : "Please log in"}
    />
  )
}

// Or using early returns
const Message: React.FC<{ error?: string }> = ({ error }) => {
  if (error) {
    return <textlabel Text={`Error: ${error}`} TextColor3={Color3.fromRGB(255, 0, 0)} />
  }

  return <textlabel Text="All good!" TextColor3={Color3.fromRGB(0, 255, 0)} />
}

// Or returning null to render nothing
interface OptionalContentProps {
  show: boolean
  children?: React.ReactNode
}

const OptionalContent: React.FC<OptionalContentProps> = ({ show, children }) => {
  return show ? <frame>{children}</frame> : null
}
```

## List Rendering with Keys

Render lists efficiently with proper keys:

```typescript
interface TodoListProps {
  todos: Todo[]
}

const TodoList: React.FC<TodoListProps> = ({ todos }) => {
  return (
    <scrollingframe Size={new UDim2(1, 0, 1, 0)}>
      <uilistlayout />
      {todos.map((todo) => (
        <textlabel
          key={todo.id}
          Text={todo.text}
          LayoutOrder={todo.id}
          Size={new UDim2(1, 0, 0, 30)}
        />
      ))}
    </scrollingframe>
  )
}

export default TodoList
```

**Important:** Always use a unique, stable `key` prop (not array index):
```typescript
// ❌ Bad - uses array index
items.map((item, index) => <frame key={index} />)

// ✅ Good - uses item ID
items.map((item) => <frame key={item.id} />)
```

## Form Handling

Managing form state with custom hooks:

```typescript
// src/hooks/use-form-input.ts
import { useState } from "@rbxts/react"

interface FormInputHandlers {
  value: string
  onChange: (value: string) => void
  reset: () => void
}

export function useFormInput(initialValue: string = ""): FormInputHandlers {
  const [value, setValue] = useState(initialValue)

  return {
    value,
    onChange: (newValue: string) => setValue(newValue),
    reset: () => setValue(initialValue),
  }
}
```

```typescript
// src/components/contact-form/contact-form.tsx
import { useFormInput } from "@/hooks/use-form-input"

const ContactForm: React.FC = () => {
  const name = useFormInput("")
  const email = useFormInput("")

  const handleSubmit = () => {
    console.log("Submitting:", { name: name.value, email: email.value })
    name.reset()
    email.reset()
  }

  return (
    <frame>
      <textbox
        Text={name.value}
        PlaceholderText="Name"
        Event={{
          FocusLost: (rbx: TextBox) => name.onChange(rbx.Text),
        }}
      />
      <textbox
        Text={email.value}
        PlaceholderText="Email"
        Event={{
          FocusLost: (rbx: TextBox) => email.onChange(rbx.Text),
        }}
      />
      <textbutton
        Text="Submit"
        Event={{
          Activated: handleSubmit,
        }}
      />
    </frame>
  )
}

export default ContactForm
```

## Performance Optimization

Memoize components and callbacks to prevent unnecessary re-renders:

```typescript
// Memoize component - only re-renders if props change
interface ExpensiveComponentProps {
  data: unknown
}

const ExpensiveComponent = React.memo<ExpensiveComponentProps>(({ data }) => {
  // This only re-renders when `data` changes
  return <frame />
})

// Memoize callbacks
interface ParentProps {}

const Parent: React.FC<ParentProps> = () => {
  const handleClick = React.useCallback(() => {
    console.log("Clicked")
  }, [])

  return <ChildButton onClick={handleClick} />
}

// Memoize computed values
interface FilteredListProps {
  items: string[]
  filterFn: (item: string) => boolean
}

const FilteredList: React.FC<FilteredListProps> = ({ items, filterFn }) => {
  const filtered = React.useMemo(
    () => items.filter(filterFn),
    [items, filterFn]
  )

  return (
    <frame>
      {filtered.map((item) => (
        <textlabel key={item} Text={item} />
      ))}
    </frame>
  )
}
```

---

**See also**: [Getting Started](./getting-started.md), [Hooks API](../api/hooks.md), [Project Structure](./project-structure.md)
