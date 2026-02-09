# Example: Simple Counter

A basic example demonstrating React state and event handling.

## Code

```lua
-- src/components/Counter.tsx
import React, { useState } from "@react-lua/react"

local function Counter(props: { initialValue: number? })
    local initialValue = props.initialValue or 0
    local count, setCount = React.useState(initialValue)
    
    return React.createElement("Frame", {
        Size = UDim2.fromOffset(300, 150),
        BackgroundColor3 = Color3.fromRGB(240, 240, 240),
        BorderMode = Enum.BorderMode.Outline
    },
        React.createElement("TextLabel", {
            Text = "Counter Example",
            Size = UDim2.fromScale(1, 0.3),
            BackgroundTransparency = 1,
            TextSize = 18,
            Font = Enum.Font.GothamBold
        }),
        React.createElement("TextLabel", {
            Text = tostring(count),
            Size = UDim2.fromScale(1, 0.4),
            Position = UDim2.fromScale(0, 0.3),
            BackgroundTransparency = 1,
            TextSize = 48,
            Font = Enum.Font.GothamBold,
            TextColor3 = Color3.fromRGB(59, 89, 152)
        }),
        React.createElement("Frame", {
            Size = UDim2.fromScale(1, 0.3),
            Position = UDim2.fromScale(0, 0.7),
            BackgroundTransparency = 1
        },
            React.createElement("TextButton", {
                Text = "-",
                Size = UDim2.fromScale(0.33, 1),
                BackgroundColor3 = Color3.fromRGB(231, 76, 60),
                TextColor3 = Color3.new(1, 1, 1),
                Font = Enum.Font.GothamBold,
                TextSize = 24,
                [React.Event.Activated] = function()
                    setCount(count - 1)
                end
            }),
            React.createElement("TextButton", {
                Text = "Reset",
                Size = UDim2.fromScale(0.33, 1),
                Position = UDim2.fromScale(0.33, 0),
                BackgroundColor3 = Color3.fromRGB(149, 165, 166),
                TextColor3 = Color3.new(1, 1, 1),
                Font = Enum.Font.GothamBold,
                TextSize = 16,
                [React.Event.Activated] = function()
                    setCount(initialValue)
                end
            }),
            React.createElement("TextButton", {
                Text = "+",
                Size = UDim2.fromScale(0.33, 1),
                Position = UDim2.fromScale(0.66, 0),
                BackgroundColor3 = Color3.fromRGB(46, 204, 113),
                TextColor3 = Color3.new(1, 1, 1),
                Font = Enum.Font.GothamBold,
                TextSize = 24,
                [React.Event.Activated] = function()
                    setCount(count + 1)
                end
            })
        )
    )
end

return Counter
```

## Usage

```lua
-- In your main app
React.createElement(Counter, {
    initialValue = 10
})
```

## Key Concepts Demonstrated

1. **useState** - Managing component state (count)
2. **Event Handling** - Responding to button clicks
3. **Props** - Passing initial value from parent
4. **Conditional Rendering** - Display count based on state
5. **UI Layout** - Organizing elements with frames

## Variations

### With Custom Hook

```lua
local function useCounter(initialValue)
    local count, setCount = React.useState(initialValue or 0)
    
    return {
        count = count,
        increment = function()
            setCount(count + 1)
        end,
        decrement = function()
            setCount(count - 1)
        end,
        reset = function()
            setCount(initialValue or 0)
        end
    }
end

local function Counter(props)
    local counter = useCounter(props.initialValue)
    
    return React.createElement("Frame", {
        Size = UDim2.fromOffset(300, 150)
    },
        React.createElement("TextLabel", {
            Text = tostring(counter.count)
        }),
        -- buttons...
    )
end
```

### With Limit

```lua
local function Counter(props: { min: number, max: number })
    local count, setCount = React.useState(0)
    
    local canIncrement = count < props.max
    local canDecrement = count > props.min
    
    return React.createElement("Frame", {
        Size = UDim2.fromOffset(300, 150)
    },
        React.createElement("TextLabel", {
            Text = tostring(count)
        }),
        React.createElement("TextButton", {
            Text = "-",
            [React.Event.Activated] = if canDecrement then function()
                setCount(count - 1)
            end else nil
        }),
        React.createElement("TextButton", {
            Text = "+",
            [React.Event.Activated] = if canIncrement then function()
                setCount(count + 1)
            end else nil
        })
    )
end
```

---

**See also**: [Form Example](./form.md), [Getting Started](../guides/getting-started.md)
