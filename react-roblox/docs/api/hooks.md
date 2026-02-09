# Hooks API

Hooks allow functional components to have state and side effects. They're the modern way to write React components in TypeScript.

## useState

Adds state to a functional component.

```typescript
const [value, setValue] = useState(initialValue)
```

### Parameters
- `initialValue` (value or function): Initial state value or a function that returns it
- Returns: tuple of `[currentValue, setterFunction]`

### Setter Function
- Call with new value: `setValue(newValue)`
- Call with updater function: `setValue((prevValue) => newValue)`

### Examples

**Simple counter:**
```typescript
const Counter: React.FC = () => {
  const [count, setCount] = useState(0)

  return (
    <frame>
      <textlabel Text={`Count: ${count}`} />
      <textbutton
        Text="Increment"
        Event={{ Activated: () => setCount(count + 1) }}
      />
    </frame>
  )
}
```

**With updater function for complex logic:**
```typescript
const Counter: React.FC = () => {
  const [count, setCount] = useState(0)

  return (
    <textbutton
      Text={tostring(count)}
      Event={{
        Activated: () => {
          // Updater ensures we use the latest state value
          setCount((prevCount) => prevCount + 1)
        },
      }}
    />
  )
}
```

**With lazy initialization:**
```typescript
const ExpensiveComponent: React.FC = () => {
  // Computation only runs once on mount
  const [data, setData] = useState(() => {
    return expensiveInitialization()
  })

  return <textlabel Text={tostring(data)} />
}
```

## useEffect

Runs side effects after render. Use for connections, timers, and other effects.

```typescript
useEffect(() => {
  // Effect code runs here

  return () => {
    // Cleanup function (optional)
  }
}, dependencies)
```

### Parameters
- `effectFunction` (function): Runs after render, can return cleanup function
- `dependencies` (array): When to re-run the effect
  - Omit: runs after every render (rarely useful)
  - Empty array `[]`: runs only after first render
  - With values `[dep1, dep2]`: runs when dependencies change

### Examples

**Setup and cleanup:**
```typescript
import { useEffect, useState } from "@rbxts/react"
import { UserInputService } from "@rbxts/services"

const MouseTracker: React.FC = () => {
  const [mousePos, setMousePos] = useState(new Vector2(0, 0))

  useEffect(() => {
    const connection = UserInputService.InputChanged.Connect((input) => {
      if (input.UserInputType === Enum.UserInputType.MouseMovement) {
        setMousePos(input.Position)
      }
    })

    // Cleanup function - disconnects when component unmounts
    return () => {
      connection.Disconnect()
    }
  }, []) // Empty array = run once on mount

  return (
    <textlabel Text={`Mouse: (${mousePos.X.toFixed(0)}, ${mousePos.Y.toFixed(0)})`} />
  )
}
```

**With dependencies:**
```typescript
interface DataFetcherProps {
  userId: number
}

const DataFetcher: React.FC<DataFetcherProps> = ({ userId }) => {
  const [data, setData] = useState<unknown>(undefined)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Runs when userId changes
    setLoading(true)
    // Fetch data for userId
    setData("Loaded data")
    setLoading(false)
  }, [userId]) // Re-run when userId changes

  return (
    <textlabel
      Text={loading ? "Loading..." : tostring(data)}
    />
  )
}
```

## useContext

Reads a context value provided by a parent component.

```typescript
const contextValue = useContext(ContextObject)
```

### Example

**Using theme context:**
```typescript
import { createContext, useContext } from "@rbxts/react"

interface Theme {
  primary: Color3
  secondary: Color3
}

const ThemeContext = createContext<Theme>({
  primary: Color3.fromRGB(0, 0, 255),
  secondary: Color3.fromRGB(200, 200, 200),
})

const ThemedButton: React.FC = () => {
  const theme = useContext(ThemeContext)

  return (
    <textbutton
      Text="Click me"
      BackgroundColor3={theme.primary}
    />
  )
}

// Setup provider in app
const App: React.FC = () => (
  <ThemeContext.Provider
    value={{
      primary: Color3.fromRGB(100, 100, 255),
      secondary: Color3.fromRGB(100, 100, 100),
    }}
  >
    <ThemedButton />
  </ThemeContext.Provider>
)
```

## useReducer

Manages complex state with a reducer function. Useful for state machines and complex logic.

```typescript
const [state, dispatch] = useReducer(reducerFunction, initialState)
```

### Example

**Todo list with reducer:**
```typescript
import { useReducer } from "@rbxts/react"

interface Todo {
  id: number
  text: string
}

type TodoAction =
  | { type: "add"; text: string }
  | { type: "remove"; id: number }
  | { type: "toggle"; id: number }

interface TodoState {
  todos: Todo[]
  nextId: number
}

function todoReducer(state: TodoState, action: TodoAction): TodoState {
  switch (action.type) {
    case "add":
      return {
        todos: [...state.todos, { id: state.nextId, text: action.text }],
        nextId: state.nextId + 1,
      }
    case "remove":
      return {
        todos: state.todos.filter((t) => t.id !== action.id),
        nextId: state.nextId,
      }
    case "toggle":
      return {
        todos: state.todos, // Update logic here
        nextId: state.nextId,
      }
  }
}

const TodoApp: React.FC = () => {
  const [state, dispatch] = useReducer(todoReducer, {
    todos: [],
    nextId: 0,
  })

  return (
    <frame>
      <textlabel Text={`Todos: ${state.todos.size()}`} />
      <textbutton
        Text="Add Todo"
        Event={{
          Activated: () => {
            dispatch({ type: "add", text: "New task" })
          },
        }}
      />
    </frame>
  )
}
```

## useCallback

Memoizes a callback function to prevent unnecessary re-renders of child components that depend on it.

```typescript
const memoizedCallback = useCallback(() => {
  // Function body
}, dependencies)
```

### Example

```typescript
interface ChildProps {
  onItemClick: (item: string) => void
}

const Child: React.FC<ChildProps> = ({ onItemClick }) => {
  return (
    <textbutton
      Text="Click"
      Event={{
        Activated: () => onItemClick("clicked"),
      }}
    />
  )
}

const Parent: React.FC = () => {
  const handleClick = useCallback((value: string) => {
    print("Item clicked:", value)
  }, []) // Empty dependency array = memoize once

  return <Child onItemClick={handleClick} />
}
```

## useMemo

Memoizes a computed value to avoid expensive recalculations.

```typescript
const memoizedValue = useMemo(() => {
  // Expensive computation
  return computedValue
}, dependencies)
```

### Example

```typescript
interface FilteredListProps {
  items: Array<{ id: number; name: string }>
  searchText: string
}

const FilteredList: React.FC<FilteredListProps> = ({ items, searchText }) => {
  const filtered = useMemo(() => {
    return items.filter((item) =>
      item.name.lower().find(searchText.lower())[0] !== undefined
    )
  }, [items, searchText]) // Recompute when items or searchText changes

  return (
    <frame>
      {filtered.map((item) => (
        <textlabel key={item.id} Text={item.name} />
      ))}
    </frame>
  )
}
```

## useRef

Creates a mutable reference that persists across renders without causing re-renders.

```typescript
const ref = useRef<T>(initialValue)
// Access with: ref.current
```

### Examples

**Direct instance access:**
```typescript
import { useRef } from "@rbxts/react"

const TextBoxWithFocus: React.FC = () => {
  const textBoxRef = useRef<TextBox>(null)

  const handleFocus = () => {
    if (textBoxRef.current) {
      textBoxRef.current.CaptureFocus()
    }
  }

  return (
    <>
      <textbox ref={textBoxRef} />
      <textbutton Text="Focus" Event={{ Activated: handleFocus }} />
    </>
  )
}
```

**Storing mutable values:**
```typescript
import { useRef, useEffect } from "@rbxts/react"
import { RunService } from "@rbxts/services"

const Timer: React.FC = () => {
  const timerRef = useRef(0)

  useEffect(() => {
    const connection = RunService.Heartbeat.Connect((deltaTime: number) => {
      timerRef.current += deltaTime
    })

    return () => {
      connection.Disconnect()
    }
  }, [])

  return <textlabel Text={`Time: ${timerRef.current.toFixed(1)}`} />
}
```

## useImperativeHandle

Customizes the instance value exposed when using `forwardRef`. Rarely needed in most applications.

```typescript
useImperativeHandle(ref, () => ({
  customMethod: () => {},
  customProp: value,
}), dependencies)
```

### Example

```typescript
import { forwardRef, useImperativeHandle, useRef } from "@rbxts/react"

interface ScrollRef {
  scrollToTop: () => void
  scrollToBottom: () => void
}

const ScrollableFrame = forwardRef<ScrollRef, {}>(({}, ref) => {
  const frameRef = useRef<ScrollingFrame>(null)

  useImperativeHandle(ref, () => ({
    scrollToTop: () => {
      if (frameRef.current) {
        frameRef.current.CanvasPosition = new Vector2(0, 0)
      }
    },
    scrollToBottom: () => {
      if (frameRef.current) {
        frameRef.current.CanvasPosition = new Vector2(
          0,
          frameRef.current.CanvasSize.Y.Offset
        )
      }
    },
  }), [])

  return (
    <scrollingframe
      ref={frameRef}
      Size={new UDim2(1, 0, 1, 0)}
    />
  )
})
```

## useLayoutEffect

Like `useEffect`, but runs synchronously after mutations. Use sparingly - prefer `useEffect` for most cases.

```typescript
useLayoutEffect(() => {
  // Runs synchronously after render
  return () => {
    // Cleanup
  }
}, dependencies)
```

## Rules of Hooks

1. **Only call hooks at the top level** - Don't call hooks inside loops, conditions, or nested functions
2. **Only call hooks from React components** - Call from functional components or custom hooks
3. **Use custom hooks** - Extract hook logic into custom hooks for reusability

### Bad Example (breaks rules)
```typescript
// ❌ BAD - calling hook inside condition
const BadComponent: React.FC<{ isActive: boolean }> = ({ isActive }) => {
  if (isActive) {
    const [count, setCount] = useState(0) // ❌ WRONG
  }
  return <frame />
}

// ❌ BAD - calling hook inside loop
const items = [1, 2, 3]
items.forEach((item) => {
  useState(item) // ❌ WRONG
})
```

## Custom Hooks

Create reusable hook logic by extracting into functions starting with "use".

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

**Usage:**
```typescript
// src/components/contact-form/contact-form.tsx
import { useFormInput } from "@/hooks/use-form-input"

const ContactForm: React.FC = () => {
  const name = useFormInput("")
  const email = useFormInput("")

  const handleSubmit = () => {
    print(`Name: ${name.value}, Email: ${email.value}`)
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
        Event={{ Activated: handleSubmit }}
      />
    </frame>
  )
}
```

---

**See also**: [Core API](./core.md), [Advanced Features](./advanced.md)
