# Project Structure and Organization

A comprehensive guide to organizing your React-Roblox project following modern community conventions and best practices.

## Core Philosophy

Your project structure should make it easy to:
- **Find files quickly** - Organized by feature, not type
- **Scale gracefully** - Add features without restructuring
- **Maintain code** - Clear separation of concerns
- **Reuse components** - Export and compose easily
- **Test effectively** - Testable, isolated modules

This guide emphasizes:
- 📁 **kebab-case** for file and folder names
- 🔠 **PascalCase** for component names
- 🎯 **Feature-based** organization (when scaling)
- 🪡 **Consistent conventions** across the project

## Starter Project Structure

For small to medium projects:

```
src/
├── components/              # Reusable components
│   ├── common/
│   │   ├── my-button/
│   │   │   ├── my-button.tsx
│   │   │   ├── my-button.stories.tsx    (optional)
│   │   │   └── index.ts
│   │   ├── my-card/
│   │   │   ├── my-card.tsx
│   │   │   └── index.ts
│   │   └── index.ts
│   ├── layouts/
│   │   ├── app-layout/
│   │   │   ├── app-layout.tsx
│   │   │   └── index.ts
│   │   └── index.ts
│   └── pages/
│       ├── home-page/
│       │   ├── home-page.tsx
│       │   └── index.ts
│       └── index.ts
├── hooks/                   # Custom hooks
│   ├── use-form-input.ts
│   ├── use-local-storage.ts
│   ├── use-fetch.ts
│   └── index.ts
├── context/                 # Context providers
│   ├── theme-context.ts
│   ├── user-context.ts
│   └── index.ts
├── utils/                   # Utility functions
│   ├── formatting.ts
│   ├── validation.ts
│   └── helpers.ts
├── types/                   # Type definitions
│   ├── component-props.ts
│   ├── models.ts
│   └── index.ts
├── constants/               # Constants
│   ├── colors.ts
│   ├── config.ts
│   └── index.ts
├── app.tsx                  # Root component
└── client/
    └── init.client.tsx      # Roblox entry point
```

## File and Folder Naming Conventions

### 📁 Folder Names (kebab-case)

```typescript
// ✅ Good
src/components/my-button/
src/hooks/use-form-input.ts
src/context/theme-context.ts
src/utils/formatting.ts

// ❌ Bad
src/components/MyButton/
src/hooks/useFormInput.ts
src/context/ThemeContext.ts
src/utils/Formatting.ts
```

### 📄 File Names (kebab-case)

```typescript
// ✅ Good
my-button.tsx
use-form-input.ts
theme-context.ts
component-props.ts

// ❌ Bad
MyButton.tsx
useFormInput.ts
ThemeContext.ts
ComponentProps.ts
```

### 🔠 Component Names (PascalCase)

```typescript
// ✅ Good - Component file content
const MyButton: React.FC<MyButtonProps> = (props) => { ... }
const AlertDialog: React.FC<AlertDialogProps> = (props) => { ... }

// ❌ Bad
const myButton = ...
const alert_dialog = ...
```

## Directory Guide

### `components/`

Reusable UI components organized by category.

**Sub-folders:**
- `common/` - Shared, reusable components (Button, Card, Input, etc.)
- `layouts/` - Page layout components (AppLayout, Sidebar, Header, etc.)
- `pages/` - Page-level components (HomePage, ProfilePage, etc.)

**Each component folder structure:**

```
src/components/my-button/
├── my-button.tsx           # Component implementation
├── my-button.stories.tsx   # (optional) Storybook stories
└── index.ts                # Export barrel
```

**Example component:**

```typescript
// src/components/my-button/my-button.tsx
import React from "@rbxts/react"

export interface MyButtonProps {
  text: string
  onClick?: () => void
  disabled?: boolean
}

const MyButton: React.FC<MyButtonProps> = ({
  text,
  onClick,
  disabled = false,
}) => {
  return (
    <textbutton
      Text={text}
      Event={{ Activated: onClick }}
      AutoButtonColor={!disabled}
    />
  )
}

export default MyButton
```

```typescript
// src/components/my-button/index.ts
export { default as MyButton } from "./my-button"
export type { MyButtonProps } from "./my-button"
```

**Importing:**

```typescript
// ✅ Good - Use barrel import
import { MyButton } from "@/components/common"

// ✅ Also good - Direct import
import { MyButton } from "@/components/my-button"

// ❌ Bad - Deep import
import MyButton from "@/components/my-button/my-button"
```

### `hooks/`

Custom React hooks for reusable stateful logic.

```typescript
// src/hooks/use-form-input.ts
import { useState } from "@rbxts/react"

export function useFormInput(initialValue: string = "") {
  const [value, setValue] = useState(initialValue)
  return {
    value,
    onChange: (newValue: string) => setValue(newValue),
    reset: () => setValue(initialValue),
  }
}
```

```typescript
// src/hooks/use-fetch.ts
import { useState, useEffect } from "@rbxts/react"

export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Fetch implementation
  }, [url])

  return { data, loading, error }
}
```

**Export barrel:**

```typescript
// src/hooks/index.ts
export { useFormInput } from "./use-form-input"
export { useFetch } from "./use-fetch"
export { useLocalStorage } from "./use-local-storage"
```

### `context/`

Context providers for global state management.

```typescript
// src/context/theme-context.ts
import React from "@rbxts/react"

export interface Theme {
  primaryColor: Color3
  darkMode: boolean
}

export const ThemeContext = React.createContext<Theme>({
  primaryColor: Color3.fromRGB(0, 0, 255),
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
    primaryColor: darkMode ? Color3.fromRGB(50, 50, 50) : Color3.fromRGB(255, 255, 255),
    darkMode,
  }

  return (
    <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
  )
}

export default ThemeProvider
```

### `utils/`

Pure utility functions and helpers.

```typescript
// src/utils/formatting.ts
export function formatCurrency(value: number): string {
  return `$${value.toFixed(2)}`
}

export function truncateString(str: string, length: number): string {
  return str.length > length ? str.substring(0, length) + "..." : str
}
```

### `types/`

TypeScript type definitions and interfaces.

```typescript
// src/types/models.ts
export interface User {
  id: number
  name: string
  email: string
}

export interface Post {
  id: number
  title: string
  content: string
  authorId: number
}
```

### `constants/`

Application constants.

```typescript
// src/constants/colors.ts
export const COLORS = {
  primary: Color3.fromRGB(0, 0, 255),
  secondary: Color3.fromRGB(200, 200, 200),
  danger: Color3.fromRGB(255, 0, 0),
  success: Color3.fromRGB(0, 255, 0),
} as const
```

## Scaling to Feature-Based Structure

As your project grows, reorganize by feature:

```
src/
├── features/
│   ├── auth/                    # Authentication feature
│   │   ├── components/
│   │   │   ├── login-form/
│   │   │   └── sign-up-form/
│   │   ├── hooks/
│   │   │   ├── use-login.ts
│   │   │   └── use-auth.ts
│   │   ├── context/
│   │   │   └── auth-context.ts
│   │   ├── types/
│   │   │   └── auth.ts
│   │   └── index.ts
│   ├── dashboard/               # Dashboard feature
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── index.ts
│   └── settings/                # Settings feature
│       ├── components/
│       ├── hooks/
│       └── index.ts
├── shared/                      # Shared across features
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   └── types/
└── app.tsx
```

## Best Practices

### 1. Barrel Exports

Create `index.ts` files to simplify imports:

```typescript
// src/components/index.ts
export { MyButton } from "./common/my-button"
export { MyCard } from "./common/my-card"
export { AppLayout } from "./layouts/app-layout"

// Usage
import { MyButton, MyCard } from "@/components"
```

### 2. Component Organization

Keep related files together:

```
my-component/
├── my-component.tsx         # Component
├── my-component.test.ts     # Tests (if using)
├── my-component.styles.ts   # Styles (if needed)
├── my-component.stories.tsx # Storybook (if using)
└── index.ts                 # Export
```

### 3. Type Safety

Define interfaces near where they're used:

```typescript
// src/components/user-card/user-card.tsx
interface UserCardProps {
  userId: number
  onSelect: (id: number) => void
}

const UserCard: React.FC<UserCardProps> = ({ userId, onSelect }) => {
  // ...
}
```

For shared types, use `src/types/`:

```typescript
// src/types/models.ts
export interface User {
  id: number
  name: string
}
```

### 4. Import Paths

Use path aliases for cleaner imports:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

```typescript
// ✅ Good - Clean imports with alias
import { MyButton } from "@/components/common"
import { useForm } from "@/hooks"
import { User } from "@/types/models"

// ❌ Bad - Relative paths
import { MyButton } from "../../../components/common"
import { useForm } from "../../hooks"
import { User } from "../../types/models"
```

### 5. Avoid Deep Nesting

Maximum nesting depth: 3 levels

```
src/
├── components/          # 1
│   └── common/          # 2
│       └── my-button/   # 3
│           └── src      # DON'T GO DEEPER

❌ src/features/auth/components/forms/login/form/input.tsx
✅ src/features/auth/components/login-form/login-form.tsx
```

### 6. Module Organization

Organize modules by responsibility:

```
src/
├── components/     # UI components only
├── hooks/          # Custom hooks only
├── context/        # Context definitions only
├── utils/          # Pure functions only
├── types/          # Interfaces only
├── constants/      # Constants only
└── client/         # Roblox entry point only
```

## Responsive Design with ui-scaler

Always use `usePx` from `@rbxts/ui-scaler`:

```typescript
// src/components/responsive-frame/responsive-frame.tsx
import React from "@rbxts/react"
import { usePx } from "@rbxts/ui-scaler"

const ResponsiveFrame: React.FC = () => {
  const px = usePx()

  return (
    <frame
      Size={new UDim2(
        0,
        px(300),  // ✅ Good - responsive width
        0,
        px(200)   // ✅ Good - responsive height
      )}
    />
  )
}

export default ResponsiveFrame
```

See [UI Scaler Guide](./ui-scaler.md) for more details.

## Real-World Examples

### Small Project (Starter)
Suitable for: Learning, small games, simple UIs

Follow the **Starter Project Structure** above. All components in one folder.

### Medium Project (Feature-Based)
Suitable for: Multiple features, growing team, reusable components

Switch to feature-based structure when:
- You have 20+ components
- Features are independent
- Multiple developers

### Large Project (Modular)
Suitable for: Multiple teams, complex applications

Each feature is a module with:
- Own components, hooks, types, utils
- Internal organization
- Clear public API (index.ts)

## Common Patterns

### Component with Subcomponents

```
my-dialog/
├── my-dialog.tsx           # Main component
├── my-dialog-header.tsx    # Subcomponent
├── my-dialog-footer.tsx    # Subcomponent
└── index.ts
```

```typescript
// src/components/my-dialog/index.ts
export { MyDialog } from "./my-dialog"
export { MyDialogHeader } from "./my-dialog-header"
export { MyDialogFooter } from "./my-dialog-footer"
```

### Shared Types Between Modules

```
src/types/
├── shared.ts       # Types used across features
├── auth.ts         # Auth-specific types
└── models.ts       # Data models
```

### Private vs Public

```
feature/
├── components/
│   ├── _internal-component/  # Private (underscore prefix)
│   └── public-component/     # Public
└── index.ts                  # Export only public
```

## Migration Path

Starting with the Starter structure:

1. **Month 1-2**: Use flat structure, everything in folders
2. **Month 2-3**: Extract common hooks, create context providers
3. **Month 3+**: Move to feature-based when you have 3+ independent features

---

**See also**: [File Naming](./file-naming.md), [Component Organization](./component-organization.md), [UI Scaler](./ui-scaler.md)
