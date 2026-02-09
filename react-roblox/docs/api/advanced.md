# Advanced React Features

Advanced patterns and APIs for experienced React developers in TypeScript.

## Compound Components Pattern

Create components that manage state together with a flexible composition API:

```typescript
// src/components/tabs/tabs-context.ts
import React, { createContext, useContext, useState } from "@rbxts/react"

interface TabsContextType {
  activeTab: string
  setActiveTab: (id: string) => void
}

const TabsContext = createContext<TabsContextType | undefined>(undefined)

function useTabsContext() {
  const context = useContext(TabsContext)
  if (!context) {
    throw new Error("useTabsContext must be used within Tabs component")
  }
  return context
}

// src/components/tabs/tabs.tsx
interface TabsProps {
  defaultTab?: string
  children?: React.ReactNode
}

const Tabs: React.FC<TabsProps> = ({ defaultTab = "", children }) => {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <frame Size={new UDim2(1, 0, 1, 0)}>
        {children}
      </frame>
    </TabsContext.Provider>
  )
}

// src/components/tabs/tab-list.tsx
interface TabListProps {
  children?: React.ReactNode
}

const TabList: React.FC<TabListProps> = ({ children }) => {
  return (
    <frame Size={new UDim2(1, 0, 0, 40)}>
      <uilistlayout Orientation={Enum.UIListLayout.FillDirection.Horizontal} />
      {children}
    </frame>
  )
}

// src/components/tabs/tab-button.tsx
interface TabButtonProps {
  id: string
  label: string
}

const TabButton: React.FC<TabButtonProps> = ({ id, label }) => {
  const { activeTab, setActiveTab } = useTabsContext()
  const isActive = activeTab === id

  return (
    <textbutton
      Text={label}
      BackgroundColor3={isActive ? Color3.fromRGB(0, 0, 255) : Color3.fromRGB(200, 200, 200)}
      Event={{ Activated: () => setActiveTab(id) }}
    />
  )
}

// src/components/tabs/tab-panel.tsx
interface TabPanelProps {
  id: string
  children?: React.ReactNode
}

const TabPanel: React.FC<TabPanelProps> = ({ id, children }) => {
  const { activeTab } = useTabsContext()

  return activeTab === id ? <frame>{children}</frame> : null
}

// Usage
const App: React.FC = () => (
  <Tabs defaultTab="tab1">
    <TabList>
      <TabButton id="tab1" label="Tab 1" />
      <TabButton id="tab2" label="Tab 2" />
      <TabButton id="tab3" label="Tab 3" />
    </TabList>
    <TabPanel id="tab1">
      <textlabel Text="Content of Tab 1" />
    </TabPanel>
    <TabPanel id="tab2">
      <textlabel Text="Content of Tab 2" />
    </TabPanel>
    <TabPanel id="tab3">
      <textlabel Text="Content of Tab 3" />
    </TabPanel>
  </Tabs>
)
```

## Dynamic Component Selection

Render different components based on a type or key:

```typescript
import React from "@rbxts/react"

interface ButtonComponentProps {
  label: string
  onClick?: () => void
}

interface InputComponentProps {
  placeholder?: string
}

interface CardComponentProps {
  title: string
  children?: React.ReactNode
}

const componentMap: Record<string, React.ComponentType<any>> = {
  button: ({ label, onClick }: ButtonComponentProps) => (
    <textbutton Text={label} Event={{ Activated: onClick }} />
  ),
  input: ({ placeholder }: InputComponentProps) => (
    <textbox PlaceholderText={placeholder} />
  ),
  card: ({ title, children }: CardComponentProps) => (
    <frame>
      <textlabel Text={title} />
      {children}
    </frame>
  ),
}

interface DynamicComponentProps {
  type: string
  [key: string]: any
}

const DynamicComponent: React.FC<DynamicComponentProps> = ({ type, ...props }) => {
  const Component = componentMap[type]

  if (!Component) {
    return <textlabel Text={`Unknown component type: ${type}`} TextColor3={Color3.fromRGB(255, 0, 0)} />
  }

  return <Component {...props} />
}

// Usage
const App: React.FC = () => (
  <frame>
    <DynamicComponent type="button" label="Click me" onClick={() => print("clicked")} />
    <DynamicComponent type="input" placeholder="Enter text" />
    <DynamicComponent type="card" title="My Card">
      <textlabel Text="Card content" />
    </DynamicComponent>
  </frame>
)
```

## Integrating with Roblox Services

Connect React to Roblox game loop and services:

```typescript
import { useEffect, useState } from "@rbxts/react"
import { RunService, UserInputService } from "@rbxts/services"

// Custom hook for Heartbeat
export function useHeartbeat() {
  const [deltaTime, setDeltaTime] = useState(0)

  useEffect(() => {
    const connection = RunService.Heartbeat.Connect((dt) => {
      setDeltaTime(dt)
    })

    return () => {
      connection.Disconnect()
    }
  }, [])

  return deltaTime
}

// Custom hook for keyboard input
export function useKeyPress(keyCode: Enum.KeyCode) {
  const [isPressed, setIsPressed] = useState(false)

  useEffect(() => {
    const inputBegan = UserInputService.InputBegan.Connect((input) => {
      if (input.KeyCode === keyCode) {
        setIsPressed(true)
      }
    })

    const inputEnded = UserInputService.InputEnded.Connect((input) => {
      if (input.KeyCode === keyCode) {
        setIsPressed(false)
      }
    })

    return () => {
      inputBegan.Disconnect()
      inputEnded.Disconnect()
    }
  }, [keyCode])

  return isPressed
}

// Usage
const GameStatus: React.FC = () => {
  const dt = useHeartbeat()
  const wPressed = useKeyPress(Enum.KeyCode.W)

  return (
    <textlabel
      Text={`FPS: ${(1 / dt).toFixed(1)}, W Key: ${wPressed ? "Pressed" : "Released"}`}
    />
  )
}
```

## Custom Hooks for Complex Logic

Extract and reuse complex stateful logic:

```typescript
// src/hooks/use-async.ts
import { useEffect, useState } from "@rbxts/react"

interface UseAsyncState<T> {
  data?: T
  error?: unknown
  loading: boolean
}

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
): UseAsyncState<T> {
  const [state, setState] = useState<UseAsyncState<T>>({
    loading: immediate,
  })

  useEffect(() => {
    let cancelled = false

    const execute = async () => {
      setState({ loading: true })
      try {
        const response = await asyncFunction()
        if (!cancelled) {
          setState({ data: response, loading: false })
        }
      } catch (error) {
        if (!cancelled) {
          setState({ error, loading: false })
        }
      }
    }

    if (immediate) {
      execute()
    }

    return () => {
      cancelled = true
    }
  }, [asyncFunction])

  return state
}

// src/hooks/use-local-storage.ts
import { useState, useEffect } from "@rbxts/react"

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      // In a real app, use your storage solution
      return initialValue
    } catch (error) {
      print("Error reading localStorage:", error)
      return initialValue
    }
  })

  const setValue = (value: T) => {
    try {
      setStoredValue(value)
      // Store to your persistent storage
    } catch (error) {
      print("Error setting localStorage:", error)
    }
  }

  return [storedValue, setValue]
}

// Usage
const PersistentForm: React.FC = () => {
  const [name, setName] = useLocalStorage("formName", "")

  return (
    <textbox
      Text={name}
      Event={{
        FocusLost: (rbx: TextBox) => setName(rbx.Text),
      }}
    />
  )
}
```

## Performance Optimization Patterns

### Memoization with useMemo

```typescript
import { useMemo } from "@rbxts/react"

interface DataListProps {
  items: Array<{ id: number; name: string; price: number }>
  searchText: string
  filterType?: string
}

const DataList: React.FC<DataListProps> = ({ items, searchText, filterType }) => {
  // Only recompute when items or search text changes
  const filtered = useMemo(() => {
    let result = items

    if (searchText) {
      result = result.filter((item) =>
        item.name.lower().find(searchText.lower())[0] !== undefined
      )
    }

    if (filterType) {
      result = result.filter((item) => item.price > 0) // Example filter
    }

    return result
  }, [items, searchText, filterType])

  return (
    <scrollingframe>
      <uilistlayout />
      {filtered.map((item) => (
        <textlabel key={item.id} Text={`${item.name} - $${item.price}`} />
      ))}
    </scrollingframe>
  )
}
```

### useCallback for Stable Function References

```typescript
import { useCallback } from "@rbxts/react"

interface ButtonListProps {
  items: string[]
  onSelect: (item: string) => void
}

const ButtonList: React.FC<ButtonListProps> = ({ items, onSelect }) => {
  // Stable reference - prevents child re-renders
  const handleClick = useCallback((item: string) => {
    onSelect(item)
  }, [onSelect])

  return (
    <frame>
      {items.map((item) => (
        <textbutton
          key={item}
          Text={item}
          Event={{ Activated: () => handleClick(item) }}
        />
      ))}
    </frame>
  )
}
```

## Render Count Tracking

Track component render counts for debugging:

```typescript
import { useEffect, useRef } from "@rbxts/react"

export function useRenderCount(label: string) {
  const count = useRef(0)

  useEffect(() => {
    count.current += 1
    print(`${label} rendered ${count.current} times`)
  })

  return count.current
}

// Usage
const MyComponent: React.FC = () => {
  const renderCount = useRenderCount("MyComponent")

  return <textlabel Text={`Renders: ${renderCount}`} />
}
```

## Error Handling and Recovery

Graceful error handling in components:

```typescript
import { useEffect, useState } from "@rbxts/react"

interface ErrorState {
  hasError: boolean
  error?: Error
}

const ErrorBoundaryComponent: React.FC<{ children?: React.ReactNode }> = ({
  children,
}) => {
  const [error, setError] = useState<ErrorState>({ hasError: false })

  useEffect(() => {
    const handleError = (err: unknown) => {
      setError({
        hasError: true,
        error: err instanceof Error ? err : new Error(tostring(err)),
      })
    }

    // In a real app, set up a global error handler
    // window.addEventListener("error", handleError)

    return () => {
      // Clean up
    }
  }, [])

  if (error.hasError) {
    return (
      <frame BackgroundColor3={Color3.fromRGB(255, 200, 200)}>
        <textlabel
          Text={`Error: ${error.error?.message ?? "Unknown error"}`}
          TextColor3={Color3.fromRGB(255, 0, 0)}
        />
      </frame>
    )
  }

  return <frame>{children}</frame>
}
```

## Best Practices

1. **Keep components focused** - Single responsibility principle
2. **Use custom hooks for reusable logic** - DRY principle
3. **Memoize expensive computations** - Use useMemo and useCallback wisely
4. **Type everything in TypeScript** - Leverage type safety
5. **Profile performance** - Don't optimize without measurement
6. **Avoid deeply nested components** - Extract sub-components
7. **Keep props interfaces simple** - Easier to maintain and extend
8. **Document complex patterns** - Help future maintainers

---

**See also**: [Core API](./core.md), [Hooks API](./hooks.md), [Context API](./context.md)
