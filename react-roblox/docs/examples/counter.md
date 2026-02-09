# Example: Simple Counter

A basic example demonstrating React state and event handling in TypeScript.

## Basic Counter

```typescript
// src/components/counter/counter.tsx
import React, { useState } from "@rbxts/react"

interface CounterProps {
  initialValue?: number
}

const Counter: React.FC<CounterProps> = ({ initialValue = 0 }) => {
  const [count, setCount] = useState(initialValue)

  return (
    <frame
      Size={new UDim2(0, 300, 0, 150)}
      BackgroundColor3={Color3.fromRGB(240, 240, 240)}
      BorderMode={Enum.BorderMode.Outline}
    >
      <textlabel
        Text="Counter Example"
        Size={new UDim2(1, 0, 0.3, 0)}
        BackgroundTransparency={1}
        TextSize={18}
        Font={Enum.Font.GothamBold}
      />
      <textlabel
        Text={tostring(count)}
        Size={new UDim2(1, 0, 0.4, 0)}
        Position={new UDim2(0, 0, 0.3, 0)}
        BackgroundTransparency={1}
        TextSize={48}
        Font={Enum.Font.GothamBold}
        TextColor3={Color3.fromRGB(59, 89, 152)}
      />
      <frame
        Size={new UDim2(1, 0, 0.3, 0)}
        Position={new UDim2(0, 0, 0.7, 0)}
        BackgroundTransparency={1}
      >
        <uilistlayout Orientation={Enum.UIListLayout.FillDirection.Horizontal} />
        <textbutton
          Text="-"
          Size={new UDim2(0.33, 0, 1, 0)}
          BackgroundColor3={Color3.fromRGB(231, 76, 60)}
          TextColor3={new Color3(1, 1, 1)}
          Font={Enum.Font.GothamBold}
          TextSize={24}
          Event={{
            Activated: () => setCount(count - 1),
          }}
        />
        <textbutton
          Text="Reset"
          Size={new UDim2(0.33, 0, 1, 0)}
          BackgroundColor3={Color3.fromRGB(149, 165, 166)}
          TextColor3={new Color3(1, 1, 1)}
          Font={Enum.Font.GothamBold}
          TextSize={16}
          Event={{
            Activated: () => setCount(initialValue),
          }}
        />
        <textbutton
          Text="+"
          Size={new UDim2(0.33, 0, 1, 0)}
          BackgroundColor3={Color3.fromRGB(46, 204, 113)}
          TextColor3={new Color3(1, 1, 1)}
          Font={Enum.Font.GothamBold}
          TextSize={24}
          Event={{
            Activated: () => setCount(count + 1),
          }}
        />
      </frame>
    </frame>
  )
}

export default Counter
```

## Usage

```typescript
// src/components/app.tsx
import React from "@rbxts/react"
import Counter from "@/components/counter"

const App: React.FC = () => {
  return (
    <frame Size={new UDim2(1, 0, 1, 0)}>
      <Counter initialValue={10} />
    </frame>
  )
}

export default App
```

## Key Concepts

1. **useState** - Managing component state (`count`)
2. **Event Handling** - Responding to button clicks with `Event`
3. **Props** - Passing `initialValue` from parent to child
4. **Conditional Rendering** - Display count based on current state
5. **UI Composition** - Organizing elements with frames

## Custom Hook Version

Extract counter logic into a reusable custom hook:

```typescript
// src/hooks/use-counter.ts
import { useState } from "@rbxts/react"

interface UseCounterResult {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

export function useCounter(initialValue = 0): UseCounterResult {
  const [count, setCount] = useState(initialValue)

  return {
    count,
    increment: () => setCount(count + 1),
    decrement: () => setCount(count - 1),
    reset: () => setCount(initialValue),
  }
}
```

**Usage with custom hook:**

```typescript
// src/components/counter-with-hook/counter-with-hook.tsx
import React from "@rbxts/react"
import { useCounter } from "@/hooks/use-counter"

interface CounterWithHookProps {
  initialValue?: number
}

const CounterWithHook: React.FC<CounterWithHookProps> = ({ initialValue = 0 }) => {
  const { count, increment, decrement, reset } = useCounter(initialValue)

  return (
    <frame Size={new UDim2(0, 300, 0, 150)}>
      <textlabel Text={`Count: ${count}`} />
      <textbutton
        Text="-"
        Event={{ Activated: decrement }}
      />
      <textbutton
        Text="Reset"
        Event={{ Activated: reset }}
      />
      <textbutton
        Text="+"
        Event={{ Activated: increment }}
      />
    </frame>
  )
}

export default CounterWithHook
```

## Counter with Limits

Add min/max constraints:

```typescript
// src/components/limited-counter/limited-counter.tsx
import React, { useState } from "@rbxts/react"

interface LimitedCounterProps {
  initialValue?: number
  min?: number
  max?: number
}

const LimitedCounter: React.FC<LimitedCounterProps> = ({
  initialValue = 0,
  min = -10,
  max = 10,
}) => {
  const [count, setCount] = useState(initialValue)

  const canIncrement = count < max
  const canDecrement = count > min

  return (
    <frame Size={new UDim2(0, 300, 0, 100)}>
      <textlabel
        Text={`Count: ${count} (${min} to ${max})`}
        Size={new UDim2(1, 0, 0.4, 0)}
      />
      <frame
        Size={new UDim2(1, 0, 0.6, 0)}
        Position={new UDim2(0, 0, 0.4, 0)}
      >
        <uilistlayout Orientation={Enum.UIListLayout.FillDirection.Horizontal} />
        <textbutton
          Text="-"
          Event={{
            Activated: canDecrement ? () => setCount(count - 1) : undefined,
          }}
          BackgroundColor3={canDecrement ? Color3.fromRGB(200, 50, 50) : Color3.fromRGB(150, 150, 150)}
        />
        <textbutton
          Text="Reset"
          Event={{
            Activated: () => setCount(initialValue),
          }}
        />
        <textbutton
          Text="+"
          Event={{
            Activated: canIncrement ? () => setCount(count + 1) : undefined,
          }}
          BackgroundColor3={canIncrement ? Color3.fromRGB(50, 200, 50) : Color3.fromRGB(150, 150, 150)}
        />
      </frame>
    </frame>
  )
}

export default LimitedCounter
```

## Counter with Step Size

Allow configurable increment/decrement step:

```typescript
// src/components/configurable-counter/configurable-counter.tsx
import React, { useState } from "@rbxts/react"

interface ConfigurableCounterProps {
  initialValue?: number
  step?: number
}

const ConfigurableCounter: React.FC<ConfigurableCounterProps> = ({
  initialValue = 0,
  step = 1,
}) => {
  const [count, setCount] = useState(initialValue)

  return (
    <frame>
      <textlabel Text={`Count: ${count} (Step: ${step})`} />
      <textbutton
        Text={`- ${step}`}
        Event={{
          Activated: () => setCount(count - step),
        }}
      />
      <textbutton
        Text="Reset"
        Event={{
          Activated: () => setCount(initialValue),
        }}
      />
      <textbutton
        Text={`+ ${step}`}
        Event={{
          Activated: () => setCount(count + step),
        }}
      />
    </frame>
  )
}

export default ConfigurableCounter
```

---

**See also**: [Form Example](./form.md), [Getting Started](../guides/getting-started.md)
