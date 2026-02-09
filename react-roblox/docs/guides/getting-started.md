# Getting Started with React in Roblox

This guide walks you through the fundamentals of React-Lua on Roblox.

## Prerequisites

- TypeScript/Luau knowledge
- Basic understanding of React concepts
- Roblox development environment set up
- Package manager (npm/pnpm)

## Installation

React-Lua is available through npm. Install it in your roblox-ts project:

```bash
npm install @react-lua/react
# or
pnpm add @react-lua/react
```

## Your First Component

Create a simple component:

```lua
-- src/components/HelloWorld.tsx
import React from "@react-lua/react"

local function HelloWorld(props: { name: string })
    return React.createElement("TextLabel", {
        Text = "Hello, " .. props.name,
        Size = UDim2.fromOffset(200, 50),
        TextSize = 24
    })
end

return HelloWorld
```

## Rendering

To render a React component in Roblox:

```lua
-- src/client/init.client.tsx
import React from "@react-lua/react"
import ReactRoblox from "@react-lua/react-roblox"
import App from "../components/App"

local root = ReactRoblox.createRoot(game.Players.LocalPlayer:WaitForChild("PlayerGui"))
root:render(React.createElement(App))
```

## State with Hooks

Create a component with state:

```lua
-- src/components/Counter.tsx
import React, { useState } from "@react-lua/react"

local function Counter()
    local count, setCount = React.useState(0)
    
    return React.createElement("Frame", {
        Size = UDim2.fromOffset(300, 100),
        BackgroundColor3 = Color3.fromRGB(240, 240, 240)
    },
        React.createElement("TextLabel", {
            Text = "Count: " .. tostring(count),
            Size = UDim2.fromScale(1, 0.5),
            TextSize = 20
        }),
        React.createElement("TextButton", {
            Text = "Increment",
            Size = UDim2.fromScale(1, 0.5),
            Position = UDim2.fromScale(0, 0.5),
            [React.Event.Activated] = function()
                setCount(count + 1)
            end
        })
    )
end

return Counter
```

## Handling Events

React uses special Roblox-specific event handlers:

```lua
local function Button(props)
    return React.createElement("TextButton", {
        Text = props.label,
        Size = UDim2.fromOffset(100, 50),
        
        -- Handle Activated event
        [React.Event.Activated] = function(rbx)
            print("Button clicked:", rbx.Name)
            if props.onClick then
                props.onClick()
            end
        end,
        
        -- Handle input events
        [React.Event.InputBegan] = function(rbx, input, gameProcessed)
            if not gameProcessed and input.UserInputType == Enum.UserInputType.MouseButton1 then
                print("Mouse button 1 pressed")
            end
        end
    })
end
```

## Effects and Side Effects

Use `useEffect` for side effects like connections:

```lua
local UserInputService = game:GetService("UserInputService")

local function KeyboardListener(props)
    local lastKey, setLastKey = React.useState(nil)
    
    React.useEffect(function()
        local connection = UserInputService.InputBegan:Connect(function(input, gameProcessed)
            if not gameProcessed then
                setLastKey(tostring(input.KeyCode))
            end
        end)
        
        -- Cleanup function - runs when component unmounts
        return function()
            connection:Disconnect()
        end
    end, {})
    
    return React.createElement("TextLabel", {
        Text = "Last key: " .. (lastKey or "None"),
        Size = UDim2.fromOffset(200, 50)
    })
end

return KeyboardListener
```

## Props and Children

Pass data through props:

```lua
-- Container component
local function Card(props)
    return React.createElement("Frame", {
        Size = props.size or UDim2.fromOffset(400, 300),
        BackgroundColor3 = props.backgroundColor or Color3.new(1, 1, 1)
    },
        React.createElement("TextLabel", {
            Text = props.title,
            Size = UDim2.fromScale(1, 0.1)
        }),
        React.createElement("Frame", {
            Size = UDim2.fromScale(1, 0.9),
            Position = UDim2.fromScale(0, 0.1),
            -- props.children contains child elements
            children = props.children
        })
    )
end

-- Usage
React.createElement(Card, {
    title = "My Card",
    size = UDim2.fromOffset(500, 400)
},
    React.createElement("TextLabel", { Text = "Content here" })
)
```

## Building Your App Structure

Follow this recommended folder structure:

```
src/
├── components/          # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   └── Layout.tsx
├── hooks/              # Custom React hooks
│   ├── useForm.ts
│   └── useTheme.ts
├── pages/              # Top-level page components
│   └── Home.tsx
├── utils/              # Utility functions
│   └── formatting.ts
├── types/              # Type definitions
│   └── models.ts
└── client/
    └── init.client.tsx  # Entry point
```

## Component Best Practices

1. **Keep components focused** - Each component should do one thing
2. **Use props for configuration** - Make components reusable
3. **Extract custom hooks** - Share stateful logic between components
4. **Use TypeScript** - Get better type safety and IDE support
5. **Separate concerns** - Keep UI, logic, and data separate

## Next Steps

- Learn [Core API Concepts](../api/core.md)
- Explore [Hooks in detail](../api/hooks.md)
- Review [Advanced patterns](../api/advanced.md)
- Study [real-world examples](../examples/)

---

**Official References**:
- React-Lua: https://react.luau.page/
- React Concepts: https://reactjs.org/docs/hello-world.html
