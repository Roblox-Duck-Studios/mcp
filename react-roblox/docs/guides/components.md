# Component Patterns

## Basic Component Structure

```tsx
// button.tsx
import type { ReactNode } from "@rbxts/react";
import React from "@rbxts/react";

interface MyButtonProps {
  Disabled?: boolean;
  OnClick?: () => void;
  Text: string;
}

export function MyButton({
  Disabled = false,
  OnClick,
  Text,
}: Readonly<MyButtonProps>): React.ReactElement {
  return (
    <textbutton 
      AutoButtonColor={!Disabled} 
      Event={{ Activated: OnClick }} 
      Text={Text} 
    />
  );
}

// Usage
<MyButton Text="hello" />;
```

## Component Best Practices

| Practice | Description | Example |
|----------|-------------|---------|
| **PascalCase Props** | Use PascalCase for all component properties | `OnClick`, `Disabled` |
| **Arrow Functions** | Use arrow functions for component definitions | `export const MyButton = (props) => ...` |
| **Named Exports** | Never use `export default` | `export function MyButton()` |
| **Readonly Props** | Apply `Readonly` to props | `Readonly<MyButtonProps>` |
| **Return Type** | Always specify `React.ReactElement` return type | `: React.ReactElement` |
| **Single File** | Keep components in one file | One component per file |

## Function Components (Recommended)

```tsx
import React, { useState, useEffect } from "@rbxts/react";

interface CounterProps {
  initialCount: number;
}

export function Counter({ initialCount }: Readonly<CounterProps>): React.ReactElement {
  const [count, setCount] = useState(initialCount);

  useEffect(() => {
    print(`Count changed to: ${count}`);
  }, [count]);

  return (
    <textbutton
      Text={`Count: ${count}`}
      Event={{
        Activated: () => setCount(count + 1)
      }}
    />
  );
}
```

## Class Components
Never try to use react class components other than error boundaries.
