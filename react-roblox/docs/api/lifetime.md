# React Lifetime

## Overview

**`@rbxts/react-lifetime`** provides utilities for delaying component unmounting, useful for exit animations and cleanup operations.

## Installation

```bash
npm install @rbxts/react-lifetime-component
```

## Core Concepts

- **`LifetimeComponent`** - Wrapper that manages child component lifetimes
- **Delayed Unmount** - Components aren't immediately removed when taken out of the tree
- **Controlled Cleanup** - Children control when they actually unmount

## Important Constraints

- Only works with React Components (not intrinsic elements like `<frame />`)
- Only works with fragments
- Uses internal React APIs (may break with React updates)
- Props are modified (extra keys added via `newproxy()`)
- Must use provided hooks to control unmounting

## Basic Example

```tsx
import React, { PropsWithChildren, useEffect, useMemo } from "@rbxts/react";
import { LifetimeComponent, useLifetimeAsync } from "@rbxts/react-lifetime-component";
import { useMotion } from "@rbxts/ripple";

// State management for windows
const windowsList = new Map<string, React.Element>();

function WindowsRenderer() {
  const [windows, setWindows] = useState(new Map(windowsList));

  const windowsRender = useMemo(() => {
    const toRender = new Map<string, React.Element>();
    windows.forEach((render, key) => {
      const element = <Window key={key}>{render}</Window>;
      toRender.set(key, element);
    });
    return toRender;
  }, [windows]);

  return <LifetimeComponent>{windowsRender}</LifetimeComponent>;
}

function Window(props: PropsWithChildren) {
  const [anchor, motion] = useMotion(-0.5);

  useEffect(() => {
    motion.spring(0.5); // Animate in
  }, []);

  // Delay unmount until animation completes
  useLifetimeAsync(props, async () => {
    motion.spring(1.5); // Animate out
    await Promise.delay(1); // Wait for animation
  });

  const position = anchor.map(x => UDim2.fromScale(x, 0.5));

  return (
    <frame Position={position} AnchorPoint={new Vector2(0.5, 0.5)} Size={UDim2.fromOffset(200, 200)}>
      {props.children}
    </frame>
  );
}
```

## Available Hooks

| Hook | Description |
|------|-------------|
| `useComponentIsActive` | Check if component is active in the controller |
| `useIsLifetimeComponent` | Check if component is inside a LifetimeComponent |
| `useComponentLifetime` | Set lifetime in seconds |
| `useDeferLifetime` | Defer unmount by N frames |
| `useLifetimeAsync` | Set async cleanup function |
| `SanitizeProps` | Remove injection keys from props |

## CanRecover Prop

The `CanRecover` prop allows recovering a component if it's re-added with the same key:

```tsx
<LifetimeComponent CanRecover={true}>
  {windowsRender}
</LifetimeComponent>
```

When enabled, if a component is removed and re-added with the same key, the old instance is recovered instead of creating a new one.

**Reference:** [React Lifetime Documentation](https://raw.githubusercontent.com/PepeElToro41/react-lifetime-component/refs/heads/main/README.md)
