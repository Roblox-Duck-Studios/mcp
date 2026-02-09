# Getting Started with React in Roblox TypeScript

This guide walks you through building your first React component with **roblox-typescript**. All examples use modern TypeScript and JSX syntax.

## Prerequisites

- TypeScript knowledge
- Basic React concepts understanding
- roblox-ts development environment
- npm or pnpm package manager

## Installation

Install the core React dependencies:

```bash
npm install @rbxts/react @rbxts/react-roblox
# or
pnpm add @rbxts/react @rbxts/react-roblox
```

For responsive UI and pixel-based sizing, install ui-scaler:

```bash
npm install @rbxts/ui-scaler
```

## Your First Component

Create a simple component following TypeScript and naming conventions:

```typescript
// src/components/hello-world/hello-world.tsx
import React from "@rbxts/react"

interface HelloWorldProps {
  name: string
}

const HelloWorld: React.FC<HelloWorldProps> = ({ name }) => {
  return (
    <textlabel
      Text={`Hello, ${name}`}
      Size={new UDim2(0, 200, 0, 50)}
      TextSize={24}
    />
  )
}

export default HelloWorld
```

**File Structure:** `src/components/hello-world/hello-world.tsx`
- **Folder:** kebab-case (`hello-world`)
- **Component:** PascalCase in code (`HelloWorld`)
- **File:** kebab-case (`hello-world.tsx`)

## Barrel Export Pattern

Create an `index.ts` file for cleaner imports throughout your project:

```typescript
// src/components/hello-world/index.ts
export { default as HelloWorld } from "./hello-world"
```

Now import without the deep path:

```typescript
import { HelloWorld } from "@/components/hello-world"
// Instead of: import HelloWorld from "@/components/hello-world/hello-world"
```

## Rendering Your Component

Set up your root component in a LocalScript or require a Module from your main entry point:

```typescript
// src/client/init.client.tsx
import React from "@rbxts/react"
import { createRoot } from "@rbxts/react-roblox"
import { App } from "@/components/app"

const playerGui = game.Players.LocalPlayer.WaitForChild("PlayerGui") as Instance
const root = createRoot(playerGui)

root.render(<App />)
```

## Interactive State with Hooks

Create an interactive component using the `useState` hook:

```typescript
// src/components/counter/counter.tsx
import React, { useState } from "@rbxts/react"

const Counter: React.FC = () => {
  const [count, setCount] = useState(0)

  return (
    <frame
      Size={new UDim2(0, 300, 0, 100)}
      BackgroundColor3={new Color3(0.94, 0.94, 0.94)}
    >
      <textlabel
        Text={`Count: ${count}`}
        Size={new UDim2(1, 0, 0.5, 0)}
        TextSize={20}
      />
      <textbutton
        Text="Increment"
        Size={new UDim2(1, 0, 0.5, 0)}
        Position={new UDim2(0, 0, 0.5, 0)}
        Event={{
          Activated: () => setCount(count + 1),
        }}
      />
    </frame>
  )
}

export default Counter
```

**Key Points:**
- `useState(0)` returns a tuple: `[value, setValue]`
- Event handlers go in the `Event` object
- Component names are always **PascalCase**
- Files are always **kebab-case**

## Handling Events

Use the `Event` prop object to handle Roblox events:

```typescript
// src/components/custom-button/custom-button.tsx
import React from "@rbxts/react"

interface CustomButtonProps {
  label: string
  onClick?: () => void
}

const CustomButton: React.FC<CustomButtonProps> = ({ label, onClick }) => {
  return (
    <textbutton
      Text={label}
      Size={new UDim2(0, 100, 0, 50)}
      Event={{
        Activated: onClick,
        InputBegan: (rbx, input) => {
          if (input.UserInputType === Enum.UserInputType.MouseButton1) {
            print("Mouse button 1 pressed on", rbx.Name)
          }
        },
      }}
    />
  )
}

export default CustomButton
```

## Effects and Side Effects

Use `useEffect` to run code when the component mounts or updates:

```typescript
// src/components/keyboard-listener/keyboard-listener.tsx
import React, { useState, useEffect } from "@rbxts/react"
import { UserInputService } from "@rbxts/services"

const KeyboardListener: React.FC = () => {
  const [lastKey, setLastKey] = useState<string | undefined>(undefined)

  useEffect(() => {
    const connection = UserInputService.InputBegan.Connect((input, gameProcessed) => {
      if (!gameProcessed) {
        setLastKey(tostring(input.KeyCode))
      }
    })

    // Cleanup function - disconnects when component unmounts
    return () => {
      connection.Disconnect()
    }
  }, []) // Empty dependency array = run once on mount

  return (
    <textlabel
      Text={`Last key: ${lastKey ?? "None"}`}
      Size={new UDim2(0, 200, 0, 50)}
    />
  )
}

export default KeyboardListener
```

## Props and Children

Pass data through props and render child components:

```typescript
// src/components/card/card.tsx
import React from "@rbxts/react"

interface CardProps {
  title: string
  size?: UDim2
  backgroundColor?: Color3
  children?: React.ReactNode
}

const Card: React.FC<CardProps> = ({
  title,
  size = new UDim2(0, 400, 0, 300),
  backgroundColor = new Color3(1, 1, 1),
  children,
}) => {
  return (
    <frame
      Size={size}
      BackgroundColor3={backgroundColor}
    >
      <textlabel
        Text={title}
        Size={new UDim2(1, 0, 0.1, 0)}
        TextSize={18}
      />
      <frame
        Size={new UDim2(1, 0, 0.9, 0)}
        Position={new UDim2(0, 0, 0.1, 0)}
        BackgroundTransparency={1}
      >
        {children}
      </frame>
    </frame>
  )
}

export default Card
```

## Responsive Sizing with usePx

Use the `usePx` hook from `@rbxts/ui-scaler` for consistent pixel-based scaling:

```typescript
// src/components/responsive-box/responsive-box.tsx
import React from "@rbxts/react"
import { usePx } from "@rbxts/ui-scaler"

const ResponsiveBox: React.FC = () => {
  const px = usePx()

  return (
    <frame
      Size={new UDim2(1, 0, 1, 0)}
      BackgroundColor3={new Color3(1, 1, 1)}
    >
      <uipadding
        PaddingTop={px(16)}
        PaddingBottom={px(16)}
        PaddingLeft={px(16)}
        PaddingRight={px(16)}
      />
      <textlabel
        Text="Responsive Box"
        Size={new UDim2(1, 0, 0, px(40))}
        TextSize={px(16)}
      />
    </frame>
  )
}

export default ResponsiveBox
```

**Note:** Always use `usePx()` from `@rbxts/ui-scaler` for pixel values - don't use alternative approaches like manual calculations or ratio-based sizing for pixel measurements.

## Recommended Project Structure

Follow this proven folder structure for scalability:

```
src/
├── components/
│   ├── common/                 # Reusable UI components
│   │   ├── button/
│   │   │   ├── button.tsx
│   │   │   └── index.ts
│   │   ├── card/
│   │   │   ├── card.tsx
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
├── hooks/                      # Custom hooks
│   ├── use-form-input.ts
│   ├── use-fetch.ts
│   └── index.ts
├── context/                    # Context providers
│   ├── theme-context.ts
│   ├── user-context.ts
│   └── index.ts
├── types/                      # Type definitions
│   ├── models.ts
│   └── api.ts
├── utils/                      # Utility functions
│   ├── formatting.ts
│   └── validation.ts
├── constants/                  # Constants
│   └── colors.ts
├── app.tsx                     # Root component
└── client/
    └── init.client.tsx         # Entry point
```

See [Project Structure](./project-structure.md) for a detailed guide on organizing larger applications.

## Component Best Practices

1. **Keep components focused** - One responsibility per component
2. **Use props for configuration** - Make components reusable and composable
3. **Extract custom hooks** - Share stateful logic between components
4. **Leverage TypeScript** - Use types and interfaces for better safety
5. **Separate concerns** - Keep UI, logic, and state separated
6. **Use PascalCase for components** - Always, without exception
7. **Use kebab-case for files and folders** - Always, without exception

## Next Steps

- Review [Project Structure Guide](./project-structure.md) for detailed organizational patterns
- Learn [Core API Concepts](../api/core.md)
- Explore [Hooks in Detail](../api/hooks.md)
- Study [Real-World Examples](../examples/)

---

**Official References**:
- [React Concepts](https://react.dev) - Learn React fundamentals
- [roblox-ts Documentation](https://roblox-ts.com/docs)
- [@rbxts/react](https://github.com/littensy/rbxts-react)
- [@rbxts/react-roblox](https://github.com/littensy/rbxts-react-roblox)
- [@rbxts/ui-scaler](https://github.com/littensy/rbxts-ui-scaler)
