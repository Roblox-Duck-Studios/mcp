# File Naming Conventions

Strict conventions for file and folder names in React-Roblox projects to maintain consistency and ease of navigation.

## Quick Reference

| Type | Pattern | Example |
|------|---------|---------|
| **Folders** | kebab-case | `my-component`, `use-form` |
| **Component Files** | kebab-case | `my-button.tsx` |
| **Component Name** | PascalCase | `const MyButton: React.FC` |
| **Hook Files** | kebab-case | `use-form-input.ts` |
| **Hook Name** | camelCase with use prefix | `export function useFormInput()` |
| **Utility Files** | kebab-case | `formatting.ts`, `helpers.ts` |
| **Type Files** | kebab-case | `component-props.ts`, `models.ts` |
| **Context Files** | kebab-case | `theme-context.ts` |
| **Constants** | kebab-case | `colors.ts`, `config.ts` |

## Component Files

### Structure

```
my-component/
├── my-component.tsx          # Main component
├── index.ts                  # Barrel export
├── my-component.test.ts      # Tests (optional)
└── my-component.stories.tsx  # Storybook (optional)
```

### Naming Rules

✅ **Good:**
```
src/components/
├── my-button/
│   └── my-button.tsx
├── user-profile/
│   └── user-profile.tsx
├── form-input/
│   └── form-input.tsx
└── alert-dialog/
    └── alert-dialog.tsx
```

❌ **Bad:**
```
src/components/
├── MyButton/
│   └── MyButton.tsx           # Folder name wrong
├── userProfile/
│   └── userProfile.tsx        # Folder name wrong
├── form-input/
│   └── FormInput.tsx          # File name wrong
└── alertDialog/
    └── alertDialog.tsx        # Folder name wrong
```

### Component Declaration vs Filename

```typescript
// src/components/my-button/my-button.tsx
// ✅ Good - PascalCase component name, kebab-case filename
const MyButton: React.FC<MyButtonProps> = (props) => {
  return <textbutton {...props} />
}

// ❌ Bad - camelCase component name
const myButton: React.FC<MyButtonProps> = (props) => {
  return <textbutton {...props} />
}

// ❌ Bad - snake_case component name
const my_button: React.FC<MyButtonProps> = (props) => {
  return <textbutton {...props} />
}
```

## Hook Files

### Naming Rules

✅ **Good:**
```
src/hooks/
├── use-form-input.ts         # ✅ kebab-case file
├── use-local-storage.ts
├── use-fetch.ts
└── use-theme.ts
```

❌ **Bad:**
```
src/hooks/
├── useFormInput.ts           # ❌ camelCase file
├── use_local_storage.ts      # ❌ snake_case file
├── UseFetch.ts               # ❌ PascalCase file
└── use-theme.tsx             # ❌ .tsx instead of .ts
```

### Hook Declaration

```typescript
// src/hooks/use-form-input.ts
// ✅ Good - camelCase function name with 'use' prefix
export function useFormInput(initialValue: string) {
  const [value, setValue] = useState(initialValue)
  return [value, setValue] as const
}

// ❌ Bad - wrong naming
export function UseFormInput() { }       // PascalCase
export function form_input() { }         // snake_case, no 'use'
export const useFormInput = () => { }    // const (use export function)
```

## Type/Interface Files

### Naming Rules

✅ **Good:**
```
src/types/
├── component-props.ts        # Props interfaces
├── models.ts                 # Data models
├── api.ts                    # API types
└── enums.ts                  # Enumerations
```

❌ **Bad:**
```
src/types/
├── ComponentProps.ts         # ❌ PascalCase
├── Models.ts
├── API.ts
└── Enums.ts
```

### Type/Interface Declaration

```typescript
// src/types/component-props.ts
// ✅ Good - PascalCase interface names
export interface MyButtonProps {
  text: string
  onClick?: () => void
}

export interface UserCardProps {
  userId: number
  onSelect: (id: number) => void
}

// ❌ Bad - camelCase interface names
export interface myButtonProps { }
export interface userCardProps { }
```

## Context Files

### Naming Rules

✅ **Good:**
```
src/context/
├── theme-context.ts          # ✅ kebab-case
├── user-context.ts
├── app-context.ts
└── auth-context.ts
```

❌ **Bad:**
```
src/context/
├── ThemeContext.ts           # ❌ PascalCase
├── userContext.ts            # ❌ camelCase
├── AppContext.tsx            # ❌ .tsx instead of .ts
└── AuthContext.ts
```

### Context Declaration

```typescript
// src/context/theme-context.ts
// ✅ Good - PascalCase context name
export const ThemeContext = React.createContext<Theme>(...)

// ❌ Bad - camelCase context name
export const themeContext = React.createContext<Theme>(...)
```

## Utility Files

### Naming Rules

✅ **Good:**
```
src/utils/
├── formatting.ts             # Formatting utilities
├── validation.ts             # Validation helpers
├── helpers.ts                # General helpers
└── math-utils.ts
```

❌ **Bad:**
```
src/utils/
├── Formatting.ts             # ❌ PascalCase
├── validation-helpers.ts     # ❌ Too verbose
├── Helpers.ts                # ❌ PascalCase
└── math_utils.ts             # ❌ snake_case
```

### Function Declaration

```typescript
// src/utils/formatting.ts
// ✅ Good - camelCase function names
export function formatCurrency(value: number): string { }
export function truncateString(str: string, length: number): string { }

// ❌ Bad - PascalCase function names
export function FormatCurrency(value: number): string { }
export function TruncateString(str: string, length: number): string { }
```

## Constants Files

### Naming Rules

✅ **Good:**
```
src/constants/
├── colors.ts                 # ✅ kebab-case
├── config.ts
├── app-config.ts
└── ui-defaults.ts
```

❌ **Bad:**
```
src/constants/
├── Colors.ts                 # ❌ PascalCase
├── APP_CONFIG.ts             # ❌ SCREAMING_SNAKE_CASE
├── uiDefaults.ts             # ❌ camelCase
└── appConfig.ts
```

### Constant Declaration

```typescript
// src/constants/colors.ts
// ✅ Good - SCREAMING_SNAKE_CASE for constants
export const PRIMARY_COLOR = Color3.fromRGB(0, 0, 255)
export const SECONDARY_COLOR = Color3.fromRGB(200, 200, 200)

// Or for objects, PascalCase
export const Colors = {
  primary: Color3.fromRGB(0, 0, 255),
  secondary: Color3.fromRGB(200, 200, 200),
} as const

// ❌ Bad - camelCase constant names
export const primaryColor = Color3.fromRGB(0, 0, 255)
export const colors = { ... }
```

## Folder Organization

### Feature Folders

✅ **Good:**
```
src/
├── components/
│   ├── common/
│   ├── layouts/
│   └── pages/
├── hooks/
├── context/
├── utils/
├── types/
└── constants/
```

❌ **Bad:**
```
src/
├── Components/               # ❌ PascalCase
├── Hooks/
├── Context/
├── Utils/
└── Types/
```

### Feature Sub-folders

✅ **Good:**
```
src/features/auth/
├── components/
│   ├── login-form/
│   └── sign-up-form/
├── hooks/
│   ├── use-auth.ts
│   └── use-login.ts
├── context/
│   └── auth-context.ts
└── types/
    └── auth.ts
```

❌ **Bad:**
```
src/features/Auth/           # ❌ PascalCase
├── Components/              # ❌ PascalCase
├── Hooks/
├── Context/
└── Types/
```

## Import Statements

### Recommended Import Style

```typescript
// ✅ Good - Barrel imports (clean)
import { MyButton, MyCard } from "@/components"
import { useFormInput, useFetch } from "@/hooks"
import { User, Post } from "@/types"

// ✅ Good - Named imports (explicit)
import { MyButton } from "@/components/common"
import { useFormInput } from "@/hooks"

// ❌ Bad - Deep imports (avoid)
import MyButton from "@/components/common/my-button/my-button.tsx"
import { useFormInput } from "@/hooks/use-form-input.ts"

// ❌ Bad - Incorrect paths
import { MyButton } from "../../../components/common"
import { useFormInput } from "../../hooks"
```

## Real-World Example

Complete file structure with naming:

```
src/
├── components/
│   ├── common/
│   │   ├── my-button/
│   │   │   ├── my-button.tsx              ← Component: MyButton
│   │   │   ├── my-button.test.ts          ← Test file
│   │   │   └── index.ts
│   │   ├── user-card/
│   │   │   ├── user-card.tsx
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
├── hooks/
│   ├── use-form-input.ts                  ← Function: useFormInput
│   ├── use-fetch.ts
│   ├── use-local-storage.ts
│   └── index.ts
├── context/
│   ├── theme-context.ts                   ← Const: ThemeContext
│   ├── user-context.ts
│   └── index.ts
├── utils/
│   ├── formatting.ts                      ← Functions: formatCurrency, etc.
│   ├── validation.ts
│   └── index.ts
├── types/
│   ├── component-props.ts                 ← Interfaces: MyButtonProps, etc.
│   ├── models.ts
│   └── index.ts
├── constants/
│   ├── colors.ts                          ← Consts: PRIMARY_COLOR, etc.
│   └── config.ts
├── app.tsx                                ← App component
└── client/
    └── init.client.tsx                    ← Roblox entry point
```

## Checklist

Before committing, verify:

- [ ] All folders are kebab-case (except `src/`)
- [ ] All files are kebab-case (except `index.ts`)
- [ ] All components are PascalCase (in code)
- [ ] All hooks follow `useHookName` pattern
- [ ] All interfaces are PascalCase (in code)
- [ ] All constants are SCREAMING_SNAKE_CASE (or PascalCase objects)
- [ ] All utilities are camelCase functions
- [ ] No deep imports beyond 3 levels
- [ ] Barrel exports (index.ts) present where needed

---

**See also**: [Project Structure](./project-structure.md), [Component Organization](./component-organization.md)
