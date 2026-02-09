# Context API

Managing global state and shared data through React Context in TypeScript.

## Creating Context

Use `createContext` to create a context object for sharing data across the component tree:

```typescript
import React, { createContext } from "@rbxts/react"

interface Theme {
  darkMode: boolean
  primaryColor: Color3
  secondaryColor: Color3
}

const ThemeContext = createContext<Theme>({
  darkMode: false,
  primaryColor: Color3.fromRGB(0, 0, 255),
  secondaryColor: Color3.fromRGB(200, 200, 200),
})
```

## Provider Component

Provide context values to child components:

```typescript
import React, { useState } from "@rbxts/react"

interface ThemeProviderProps {
  children?: React.ReactNode
}

const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false)

  const theme: Theme = {
    darkMode,
    primaryColor: darkMode ? Color3.fromRGB(50, 50, 50) : Color3.fromRGB(0, 0, 255),
    secondaryColor: Color3.fromRGB(200, 200, 200),
  }

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  )
}

export default ThemeProvider
```

## Using Context with useContext Hook

The modern recommended way to consume context:

```typescript
import { useContext } from "@rbxts/react"

const ThemedButton: React.FC = () => {
  const theme = useContext(ThemeContext)

  return (
    <textbutton
      Text="Click me"
      BackgroundColor3={theme.primaryColor}
      TextColor3={theme.darkMode ? new Color3(1, 1, 1) : new Color3(0, 0, 0)}
    />
  )
}
```

## Custom Context Hook

Create a custom hook for cleaner context consumption and error handling:

```typescript
// src/context/theme-context.ts
import React, { createContext, useContext } from "@rbxts/react"

interface Theme {
  darkMode: boolean
  primaryColor: Color3
  toggleTheme: () => void
}

const ThemeContext = createContext<Theme | undefined>(undefined)

export function useTheme(): Theme {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider")
  }
  return context
}

export function ThemeProvider({ children }: { children?: React.ReactNode }) {
  const [darkMode, setDarkMode] = useState(false)

  const theme: Theme = {
    darkMode,
    primaryColor: darkMode ? Color3.fromRGB(50, 50, 50) : Color3.fromRGB(0, 0, 255),
    toggleTheme: () => setDarkMode(!darkMode),
  }

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  )
}
```

**Usage:**
```typescript
const ThemedComponent: React.FC = () => {
  const { primaryColor, toggleTheme } = useTheme()

  return (
    <textbutton
      Text="Toggle Theme"
      BackgroundColor3={primaryColor}
      Event={{ Activated: toggleTheme }}
    />
  )
}
```

## Multiple Contexts

Combine multiple contexts for different concerns:

```typescript
// src/context/index.ts
import React, { useState } from "@rbxts/react"

// Theme context
interface Theme {
  darkMode: boolean
}

const ThemeContext = createContext<Theme>({ darkMode: false })

// User context
interface User {
  id: number
  name: string
}

const UserContext = createContext<User | undefined>(undefined)

// Notification context
interface Notification {
  message: string
}

const NotificationContext = createContext<Notification>({ message: "" })

export const RootProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false)
  const [user, setUser] = useState<User | undefined>({ id: 1, name: "Alice" })
  const [notification, setNotification] = useState({ message: "Welcome!" })

  return (
    <ThemeContext.Provider value={{ darkMode }}>
      <UserContext.Provider value={user}>
        <NotificationContext.Provider value={notification}>
          {children}
        </NotificationContext.Provider>
      </UserContext.Provider>
    </ThemeContext.Provider>
  )
}
```

## Context with State Management

Combine context with `useState` for dynamic state:

```typescript
// src/context/auth-context.tsx
import React, { useState, useContext } from "@rbxts/react"

interface AuthContextType {
  isLoggedIn: boolean
  login: (username: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider")
  }
  return context
}

export const AuthProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  const login = (username: string) => {
    print(`Logging in ${username}`)
    setIsLoggedIn(true)
  }

  const logout = () => {
    print("Logging out")
    setIsLoggedIn(false)
  }

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
```

## Context with useReducer

Manage complex state with a reducer:

```typescript
// src/context/counter-context.ts
import React, { useReducer, useContext, useCallback } from "@rbxts/react"

interface CounterState {
  count: number
}

type CounterAction =
  | { type: "INCREMENT" }
  | { type: "DECREMENT" }
  | { type: "RESET" }
  | { type: "SET"; value: number }

interface CounterContextType {
  state: CounterState
  dispatch: React.Dispatch<CounterAction>
}

const CounterContext = createContext<CounterContextType | undefined>(undefined)

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case "INCREMENT":
      return { count: state.count + 1 }
    case "DECREMENT":
      return { count: state.count - 1 }
    case "RESET":
      return { count: 0 }
    case "SET":
      return { count: action.value }
  }
}

export function useCounter() {
  const context = useContext(CounterContext)
  if (!context) {
    throw new Error("useCounter must be used within CounterProvider")
  }
  return context
}

export const CounterProvider: React.FC<{ children?: React.ReactNode }> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 })

  return (
    <CounterContext.Provider value={{ state, dispatch }}>
      {children}
    </CounterContext.Provider>
  )
}
```

**Usage:**
```typescript
const Counter: React.FC = () => {
  const { state, dispatch } = useCounter()

  return (
    <frame>
      <textlabel Text={`Count: ${state.count}`} />
      <textbutton
        Text="Increment"
        Event={{ Activated: () => dispatch({ type: "INCREMENT" }) }}
      />
      <textbutton
        Text="Decrement"
        Event={{ Activated: () => dispatch({ type: "DECREMENT" }) }}
      />
    </frame>
  )
}
```

## Real-World Example: Theme System

A complete theme system with switching:

```typescript
// src/context/theme-context.ts
import React, { useState, useContext, useMemo } from "@rbxts/react"

type ThemeName = "light" | "dark"

interface Theme {
  name: ThemeName
  backgroundColor: Color3
  textColor: Color3
  primaryColor: Color3
  secondaryColor: Color3
}

interface ThemeContextType {
  theme: Theme
  themeName: ThemeName
  setThemeName: (name: ThemeName) => void
}

const THEMES: Record<ThemeName, Theme> = {
  light: {
    name: "light",
    backgroundColor: new Color3(1, 1, 1),
    textColor: new Color3(0, 0, 0),
    primaryColor: Color3.fromRGB(59, 89, 152),
    secondaryColor: Color3.fromRGB(243, 114, 69),
  },
  dark: {
    name: "dark",
    backgroundColor: Color3.fromRGB(30, 30, 30),
    textColor: new Color3(1, 1, 1),
    primaryColor: Color3.fromRGB(100, 150, 200),
    secondaryColor: Color3.fromRGB(255, 150, 100),
  },
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within ThemeProvider")
  }
  return context
}

export const ThemeProvider: React.FC<{ children?: React.ReactNode }> = ({
  children,
}) => {
  const [themeName, setThemeName] = useState<ThemeName>("light")
  const theme = THEMES[themeName]

  const value = useMemo(
    () => ({ theme, themeName, setThemeName }),
    [theme, themeName]
  )

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}
```

## Performance Optimization

Context causes all consuming components to re-render when the value changes. Optimize by:

1. **Split contexts by update frequency** - Separate frequently-changing from static data
2. **Memoize context values** - Use `useMemo` to prevent unnecessary re-renders
3. **Memoize components** - Use `React.memo` on consumers

```typescript
const MyProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const [data, setData] = useState({ /* ... */ })

  // Memoize the value to prevent unnecessary re-renders
  const value = useMemo(
    () => ({
      data,
      setData,
    }),
    [data]
  )

  return (
    <MyContext.Provider value={value}>
      {children}
    </MyContext.Provider>
  )
}
```

## Common Patterns

### Separating State and Dispatch Contexts

For better performance, separate state and dispatch contexts:

```typescript
const StateContext = createContext<State | undefined>(undefined)
const DispatchContext = createContext<Dispatch | undefined>(undefined)

export const MyProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState)

  return (
    <StateContext.Provider value={state}>
      <DispatchContext.Provider value={dispatch}>
        {children}
      </DispatchContext.Provider>
    </StateContext.Provider>
  )
}

export function useState() {
  const context = useContext(StateContext)
  if (!context) throw new Error("useState must be used within MyProvider")
  return context
}

export function useDispatch() {
  const context = useContext(DispatchContext)
  if (!context) throw new Error("useDispatch must be used within MyProvider")
  return context
}
```

---

**See also**: [Core API](./core.md), [Hooks API](./hooks.md)
