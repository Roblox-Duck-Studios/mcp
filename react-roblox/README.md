# React Roblox Documentation

> **Hand-written documentation covering the React Roblox ecosystem**
> 
> This documentation covers: `@rbxts/react`, `@rbxts/react-roblox`, `@rbxts/ui-labs`, `@rbxts/ripple`, `@rbxts/react-lifetime`, `pretty-react-hooks`, `@rbxts/ultimate-list`, and standard tools used in React Roblox development.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [React Roblox Fundamentals](#react-roblox-fundamentals)
4. [Component Patterns](#component-patterns)
5. [Writing React Stories](#writing-react-stories)
6. [Pixel Scaling (Px)](#pixel-scaling-px)
7. [Ripple - Animation Library](#ripple---animation-library)
8. [Pretty React Hooks](#pretty-react-hooks)
9. [React Lifetime](#react-lifetime)
10. [Ultimate List](#ultimate-list)
11. [Roblox-Specific APIs](#roblox-specific-apis)
12. [API Reference Summary](#api-reference-summary)

---

## Introduction

React Roblox brings React's declarative programming model to the Roblox platform. It is split into two key packages:

- **`@rbxts/react@alpha`** - The core React library containing all internal logic
- **`@rbxts/react-roblox@alpha`** - React DOM equivalent for Roblox, providing the rendering system

Every concept in React JS applies to Roblox, but with Roblox's own rendering system and some slight deviations to accommodate the Luau language and Roblox engine.

**Key Philosophy**: React Roblox maintains API alignment with React JS where possible, while introducing Roblox-specific features for better integration with the platform.

---

## Installation

### Basic Installation

```bash
npm install @rbxts/react @rbxts/react-roblox
```

### Full Ecosystem Installation

```bash
# Core
npm install @rbxts/react @rbxts/react-roblox

# Development & Testing
npm install @rbxts/ui-labs

# Animation
npm install @rbxts/ripple

# Utility Hooks
npm install pretty-react-hooks

# Lifecycle Management
npm install @rbxts/react-lifetime-component

# Virtualized Lists
npm install @rbxts/ultimate-list
```

---

## React Roblox Fundamentals

### React vs React Roblox

| Aspect | React (JS) | React Roblox |
|--------|------------|--------------|
| **Logic Package** | `react` | `@rbxts/react` |
| **DOM Package** | `react-dom` | `@rbxts/react-roblox` |
| **Language** | JavaScript/TypeScript | TypeScript → Luau |
| **Rendering Target** | Browser DOM | Roblox GUI instances |
| **Component Model** | Classes or Functions | Classes or Functions |

### Why React on Roblox?

1. **Declarative UI** - Describe what your UI should look like at any given state
2. **Component Reusability** - Build modular, reusable components
3. **State Management** - Easy state and lifecycle management with hooks
4. **Developer Experience** - Familiar patterns from React JS
5. **Type Safety** - Full TypeScript support for catching errors early

### JSX in React Roblox

React Roblox supports JSX syntax, which gets compiled to `React.createElement` calls:

```tsx
// JSX
const element = <frame Size={new UDim2(1, 0, 1, 0)} />

// Compiled equivalent
const element = React.createElement("frame", { Size: new UDim2(1, 0, 1, 0) })
```

---

## Component Patterns

### Basic Component Structure

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

### Component Best Practices

| Practice | Description | Example |
|----------|-------------|---------|
| **PascalCase Props** | Use PascalCase for all component properties | `OnClick`, `Disabled` |
| **Arrow Functions** | Use arrow functions for component definitions | `export const MyButton = (props) => ...` |
| **Named Exports** | Never use `export default` | `export function MyButton()` |
| **Readonly Props** | Apply `Readonly` to props | `Readonly<MyButtonProps>` |
| **Return Type** | Always specify `React.ReactElement` return type | `: React.ReactElement` |
| **Single File** | Keep components in one file | One component per file |

### Function Components vs Class Components

#### Function Components (Recommended)

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

#### Class Components

```tsx
import React from "@rbxts/react";

interface CounterState {
  count: number;
}

interface CounterProps {
  initialCount: number;
}

const Counter = React.Component:extend("Counter");

function Counter:init(props: CounterProps)
  self:setState({ count = props.initialCount })
end

function Counter:render()
  return React.createElement("TextButton", {
    Text = `Count: ${this.state.count}`,
    [React.Event.Activated] = function()
      self:setState({ count = self.state.count + 1 })
    end
  })
end
```

**Key Differences from React JS:**
- Use `Component:extend` instead of ES6 class syntax
- Implement `init` method instead of constructor
- Use `setState` even for initial state (inherited from Legacy Roact)
- Error boundaries not fully supported due to Luau pcall limitations

---

## Writing React Stories

### UI Labs Integration

We use **`@rbxts/ui-labs`** to render and visualize stories. Every component should have a corresponding story for development and testing.

### Basic Story Structure

```tsx
// button.story.tsx
import React, { StrictMode } from "@rbxts/react";
import ReactRoblox from "@rbxts/react-roblox";
import { CreateReactStory } from "@rbxts/ui-labs";
import { Button } from "./button";
import { RootProvider } from "./root-provider";

export = CreateReactStory({ 
  react: React, 
  reactRoblox: ReactRoblox 
}, () => {
  return (
    <StrictMode>
      <RootProvider>
        <Button />
      </RootProvider>
    </StrictMode>
  );
});
```

### Story Best Practices

1. **Wrap with StrictMode** - Always wrap the top layer with StrictMode
2. **Use Root Provider** - Most projects have a root provider for global state/context
3. **Component Isolation** - Render only the component being tested
4. **Controls** - Add controls to test different props values

### Adding Controls

Controls allow you to modify component props without changing code:

```tsx
import React, { StrictMode } from "@rbxts/react";
import ReactRoblox from "@rbxts/react-roblox";
import { CreateReactStory } from "@rbxts/ui-labs";
import { Button } from "./button";

const controls = {
  text: "Click Me",
  disabled: false,
  size: new UDim2(0, 200, 0, 50)
};

export = CreateReactStory({ 
  react: React, 
  reactRoblox: ReactRoblox,
  controls: controls
}, (props) => {
  return (
    <StrictMode>
      <Button 
        Text={props.controls.text}
        Disabled={props.controls.disabled}
        Size={props.controls.size}
      />
    </StrictMode>
  );
});
```

**Reference:** [UI Labs Controls Documentation](https://ui-labs.luau.page/docs/controls/adding)

---

## Pixel Scaling (Px)

### Overview

Most projects implement a `px` function and corresponding `usePx` hook to handle responsive scaling. These functions compute values based on screen size, allowing UI to scale properly across different devices.

### How It Works

- **`px(value)`** - Converts a design pixel value to the appropriate scale for the current screen
- **`usePx()`** - React hook that provides the px function and re-renders when screen size changes

### Implementation Examples

Some projects use **`@rbxts/ui-scaler`** for px functionality, others implement it manually.

### Usage Example

```tsx
import type { ReactNode } from "@rbxts/react";
import React from "@rbxts/react";
import { usePx } from "common/client/ui/hooks/use-px";

export function DetailsView(): ReactNode {
  const px = usePx();

  return (
    <>
      <imagelabel Size={new UDim2(1, px(-450), 1, 0)} />
      <frame
        AnchorPoint={new Vector2(1)}
        Position={UDim2.fromScale(1)}
        Size={new UDim2(0, px(400), 1, 0)}
      />
    </>
  );
}
```

### Important Rules

1. **Offset Only** - Only use `px()` for the offset parameter (second argument in UDim/UDim2)
2. **Scale for Layout** - Use scale for responsive layout, offset for fixed sizes
3. **Screen-based** - Values are computed based on configured screen size reference

### Roblox UI Fundamentals

Understanding Roblox's UI positioning system is essential:

**UDim Structure:**
- `UDim.new(scale, offset)` - Single dimension
- `UDim2.new(xScale, xOffset, yScale, yOffset)` - Two dimensions

**Reference:** 
- [UI Position and Size](https://create.roblox.com/docs/ui/position-and-size)
- [Roblox UI Documentation](https://create.roblox.com/docs/ui)

---

## Ripple - Animation Library

### Overview

**`@rbxts/ripple`** is an animation library inspired by react-spring, providing an imperative API for smooth transitions and animations in Roblox.

### Installation

```bash
npm install @rbxts/ripple
```

### Core Concepts

Ripple provides three main animation primitives:

1. **`useSpring`** - Physics-based spring animations
2. **`useTween`** - Time-based easing animations
3. **`useMotion`** - Hybrid that can switch between spring and tween

### Supported Types

Ripple supports animating these data types:

| Type | Notes |
|------|-------|
| `number` | Basic numeric values |
| `Vector2` | 2D vectors |
| `Vector3` | 3D vectors |
| `Color3` | Colors (converted to Oklab color space) |
| `UDim` | UI dimension |
| `UDim2` | 2D UI dimensions |
| `CFrame` | Coordinate frames |
| `Rect` | Rectangles |

### Spring Animation Example

```tsx
import React, { useEffect } from "@rbxts/react";
import { useSpring } from "@rbxts/ripple";

interface AnimatedButtonProps {
  isHovered: boolean;
}

export function AnimatedButton({ isHovered }: Readonly<AnimatedButtonProps>): React.ReactElement {
  const [scale, scaleSpring] = useSpring(1, {
    tension: 300,
    friction: 30
  });

  useEffect(() => {
    scaleSpring.setGoal(isHovered ? 1.1 : 1);
  }, [isHovered, scaleSpring]);

  return (
    <textbutton
      Size={scale.map(s => UDim2.fromScale(0.2 * s, 0.1 * s))}
      Text="Hover Me"
    />
  );
}
```

### Motion Animation Example

```tsx
interface AnimatedLineProps {
  Active: boolean;
  ActiveColor: Color3;
  AnchorPoint?: Vector2;
  disableColor: Color3;
  Position?: UDim2;
  Size: UDim2;
  Transparency?: BindingOrValue<number>;
}

export function AnimatedLine({
  Active,
  ActiveColor,
  AnchorPoint,
  children,
  disableColor,
  Position,
  Size,
  Transparency,
}: Readonly<AnimatedLineProps>): ReactNode {
  const [frameSize, frameSizeMotion] = useMotion<UDim2>(new UDim2(new UDim(), Size.Y));
  const [frameColor, frameColorMotion] = useMotion<Color3>(Color3.fromRGB(128, 128, 128));

  useEffect(() => {
    if (Active) {
      frameSizeMotion.spring(Size);
      frameColorMotion.spring(ActiveColor);
    } else {
      frameSizeMotion.spring(new UDim2(0, 0, Size.Y.Scale, Size.Y.Offset));
      frameColorMotion.spring(disableColor);
    }
  }, [Active, ActiveColor, disableColor, frameColorMotion, frameSizeMotion, Size]);

  return (
    <frame
      AnchorPoint={AnchorPoint}
      BackgroundColor3={frameColor}
      BorderSizePixel={0}
      Position={Position}
      Size={frameSize}
      Transparency={Transparency}
    >
      {children}
    </frame>
  );
}
```

### Spring Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `tension` | `number` | Number of bounces (default: 170) |
| `friction` | `number` | Spring damping (default: 26) |
| `mass` | `number` | Speed and bounce height (default: 1) |
| `frequency` | `number` | Response speed (alternative to tension) |
| `dampingRatio` | `number` | Decay rate (alternative to friction) |
| `precision` | `number` | Distance to goal before idle (default: 0.001) |
| `start` | `boolean` | Auto-start animation (default: false) |

### Tween Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `easing` | `string` | Easing function name |
| `duration` | `number` | Animation duration in seconds |
| `repeats` | `number` | Number of times to repeat |
| `reverses` | `boolean` | Reverse on repeat |

### Available Easing Functions

- `linear`, `instant`, `smoothstep`
- `sineIn`, `sineOut`, `sineInOut`
- `backIn`, `backOut`, `backInOut`
- `quadIn`, `quadOut`, `quadInOut`
- `quartIn`, `quartOut`, `quartInOut`
- `quintIn`, `quintOut`, `quintInOut`
- `bounceIn`, `bounceOut`, `bounceInOut`
- `elasticIn`, `elasticOut`, `elasticInOut`
- `expoIn`, `expoOut`, `expoInOut`
- `circIn`, `circOut`, `circInOut`
- `cubicIn`, `cubicOut`, `cubicInOut`

**Reference:** [Ripple GitHub Repository](https://github.com/littensy/ripple)

---

## Pretty React Hooks

### Overview

**`pretty-react-hooks`** provides utility hooks for common React patterns in Roblox development. It offers hooks for debouncing, throttling, previous values, and more.

### Installation

```bash
npm install pretty-react-hooks
```

### Available Hooks

The library includes hooks such as:

- **`usePrevious`** - Track previous values
- **`useDebouncedState`** - Debounce state updates
- **`useThrottle`** - Throttle function calls
- **`useMount`** - Run effect on mount only
- **`useUnmount`** - Cleanup on unmount
- **`useUpdateEffect`** - Skip first render effect

### Basic Usage

```tsx
import { usePrevious, useDebouncedState } from "pretty-react-hooks";

function SearchComponent() {
  const [searchTerm, setSearchTerm] = useDebouncedState("", 300);
  const previousTerm = usePrevious(searchTerm);

  useEffect(() => {
    if (searchTerm !== previousTerm) {
      // Perform search
    }
  }, [searchTerm, previousTerm]);

  return (
    <textbox
      Text={searchTerm}
      Event={{
        Changed: (rbx) => setSearchTerm(rbx.Text)
      }}
    />
  );
}
```

**Reference:** [Pretty React Hooks GitHub](https://github.com/littensy/pretty-react-hooks/tree/master/src)

---

## React Lifetime

### Overview

**`@rbxts/react-lifetime`** provides utilities for delaying component unmounting, useful for exit animations and cleanup operations.

### Installation

```bash
npm install @rbxts/react-lifetime-component
```

### Core Concepts

- **`LifetimeComponent`** - Wrapper that manages child component lifetimes
- **Delayed Unmount** - Components aren't immediately removed when taken out of the tree
- **Controlled Cleanup** - Children control when they actually unmount

### Important Constraints

- Only works with React Components (not intrinsic elements like `<frame />`)
- Only works with fragments
- Uses internal React APIs (may break with React updates)
- Props are modified (extra keys added via `newproxy()`)
- Must use provided hooks to control unmounting

### Basic Example

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

### Available Hooks

| Hook | Description |
|------|-------------|
| `useComponentIsActive` | Check if component is active in the controller |
| `useIsLifetimeComponent` | Check if component is inside a LifetimeComponent |
| `useComponentLifetime` | Set lifetime in seconds |
| `useDeferLifetime` | Defer unmount by N frames |
| `useLifetimeAsync` | Set async cleanup function |
| `SanitizeProps` | Remove injection keys from props |

### CanRecover Prop

The `CanRecover` prop allows recovering a component if it's re-added with the same key:

```tsx
<LifetimeComponent CanRecover={true}>
  {windowsRender}
</LifetimeComponent>
```

When enabled, if a component is removed and re-added with the same key, the old instance is recovered instead of creating a new one.

**Reference:** [React Lifetime Documentation](https://raw.githubusercontent.com/PepeElToro41/react-lifetime-component/refs/heads/main/README.md)

---

## Ultimate List

### Overview

**`@rbxts/ultimate-list`** creates fast, efficient virtualized lists in Roblox. It only renders items that are actually visible, reducing engine load and improving performance.

### Key Benefits

1. **Performance** - Only visible items are created/rendered
2. **Deferred Execution** - Components only run when visible
3. **Zero Re-renders** - Can update without React re-renders using bindings
4. **Type Safety** - Full TypeScript/Luau type support

### Features

- Arbitrarily sized and positioned elements
- Grid and list layouts
- State-based or binding-based rendering
- Optimizations for consistent-sized elements

### Installation

```bash
npm install @rbxts/ultimate-list
```

### Basic List Example

```tsx
import { UltimateList } from "@rbxts/ultimate-list";

const letters: string[] = [];
for (let i = 0; i < 26; i++) {
  letters.push(String.fromCharCode(65 + i)); // A-Z
}

function LetterList() {
  return (
    <frame Size={UDim2.fromOffset(300, 300)}>
      <UltimateList.Components.ScrollingFrame
        dataSource={UltimateList.DataSources.array(letters)}
        dimensions={UltimateList.Dimensions.consistentSize(48)}
        renderer={UltimateList.Renderers.byState((value: string) => (
          <textlabel
            BackgroundColor3={Color3.fromRGB(255, 255, 255)}
            Font={Enum.Font.BuilderSansBold}
            Text={value}
            TextColor3={Color3.fromRGB(0, 0, 0)}
            TextSize={36}
            Size={UDim2.fromScale(1, 1)}
          />
        ))}
        direction="y"
      />
    </frame>
  );
}
```

### Grid Example

```tsx
<UltimateList.Components.ScrollingFrame
  dataSource={UltimateList.DataSources.array(letters)}
  dimensions={UltimateList.Dimensions.consistentUDim2(
    new UDim2(0.33, 0, 0, 72) // 3 columns
  )}
  renderer={UltimateList.Renderers.byState((value: string) => (
    <textlabel
      BackgroundColor3={Color3.fromRGB(255, 255, 255)}
      Font={Enum.Font.BuilderSansBold}
      Text={value}
      TextColor3={Color3.fromRGB(0, 0, 0)}
      TextSize={36}
      Size={UDim2.fromScale(1, 1)}
    />
  ))}
  direction="y"
/>
```

### Binding-Based Renderer (Zero Re-renders)

```tsx
renderer={UltimateList.Renderers.byBinding((valueBinding) => (
  <textlabel
    BackgroundColor3={Color3.fromRGB(255, 255, 255)}
    Font={Enum.Font.BuilderSansBold}
    Text={valueBinding.map((value: string | undefined) => value ?? "")}
    TextColor3={Color3.fromRGB(0, 0, 0)}
    TextSize={36}
    Size={UDim2.fromScale(1, 1)}
  />
))}
```

### Key Components

| Component | Description |
|-----------|-------------|
| `UltimateList.Components.ScrollingFrame` | Virtualized scrolling container |
| `UltimateList.DataSources.array` | Array data source |
| `UltimateList.Dimensions.consistentSize` | Fixed size dimensions |
| `UltimateList.Dimensions.consistentUDim2` | Fixed UDim2 dimensions |
| `UltimateList.Renderers.byState` | State-based rendering |
| `UltimateList.Renderers.byBinding` | Binding-based rendering |

**Reference:** [Ultimate List Documentation](https://kampfkarren.github.io/ultimate-list/)

---

## Roblox-Specific APIs

### Overview

React Roblox includes APIs unique to the Roblox platform that have no React JS equivalent.

### React.None

A placeholder to remove fields from tables (set to nil):

```tsx
// Remove state field
self:setState({ myField = React.None })

// In getDerivedStateFromProps
function MyComponent.getDerivedStateFromProps(props, state)
  return {
    value = props.condition ? state.value : React.None
  }
end
```

### React.Event

Connect to Roblox Instance events:

```tsx
<textbutton
  Event={{
    Activated: (rbx) => print("Clicked!"),
    MouseEnter: (rbx) => print("Mouse entered")
  }}
/>

// Alternative syntax
<textbutton
  {...{ [React.Event.Activated]: () => print("Clicked!") }}
/>
```

### React.Change

Connect to property change signals:

```tsx
<scrollingframe
  Change={{
    CanvasPosition: (rbx) => print("Scrolled to", rbx.CanvasPosition)
  }}
/>
```

### React.Tag

Apply CollectionService tags:

```tsx
<frame
  {...{ [React.Tag]: "my-tag another-tag" }}
/>
```

### Bindings

Bindings are reactive containers that auto-update:

```tsx
// useBinding hook
const [position, setPosition] = React.useBinding(new UDim2());

// createBinding (for class components)
const [position, setPosition] = React.createBinding(new UDim2());

// joinBindings
const combined = React.joinBindings({ x: bindingX, y: bindingY });
```

---

## API Reference Summary

### Core React Hooks

| Hook | Description |
|------|-------------|
| `useState` | State management |
| `useEffect` | Side effects |
| `useContext` | Context consumption |
| `useReducer` | Complex state logic |
| `useCallback` | Memoized callbacks |
| `useMemo` | Memoized values |
| `useRef` | Mutable references |
| `useLayoutEffect` | Synchronous effects |
| `useBinding` | Roblox binding hook |

### React Roblox Unique

| API | Description |
|-----|-------------|
| `React.None` | Remove fields |
| `React.Event` | Event connections |
| `React.Change` | Change signals |
| `React.Tag` | CollectionService tags |
| `React.createBinding` | Create bindings |
| `React.joinBindings` | Combine bindings |

### Component Utilities

| Utility | Description |
|---------|-------------|
| `React.Children.map` | Transform children |
| `React.Children.forEach` | Iterate children |
| `React.Children.count` | Count children |
| `React.Children.only` | Single child assert |
| `React.Children.toArray` | Convert to array |
| `React.memo` | Memoize components |
| `React.forwardRef` | Forward refs |

### Full API Reference

For complete API documentation, visit: [React Lua API Reference](https://react.luau.page/api-reference/react/)

---

## Additional Resources

### Official Documentation

- [React Lua API Reference](https://react.luau.page/api-reference/react/) - Complete API documentation
- [Roblox UI Position and Size](https://create.roblox.com/docs/ui/position-and-size)
- [Roblox UI Documentation](https://create.roblox.com/docs/ui)

### Package Documentation

- [UI Labs](https://ui-labs.luau.page/docs/controls/adding) - Story visualization
- [Ultimate List](https://kampfkarren.github.io/ultimate-list/) - Virtualized lists
- [Ripple](https://github.com/littensy/ripple) - Animation library
- [Pretty React Hooks](https://github.com/littensy/pretty-react-hooks) - Utility hooks
- [React Lifetime](https://github.com/PepeElToro41/react-lifetime-component) - Lifetime management

### Community

- [roblox-ts Discord](https://discord.gg/roblox-ts)
- [React Lua GitHub](https://github.com/jsdotlua/react-lua)

---

## Migration Notes

### From Legacy Roact

If migrating from Legacy Roact:

1. Replace `Roact.Children` with direct `children` prop
2. Use `Component:extend` instead of ES6 classes
3. Replace `self.state = {}` with `self:setState()`
4. Update event handlers to use `React.Event`
5. Remove `Roact.Ref` in favor of `React.createRef`

### Key Differences Summary

| Legacy Roact | React Roblox |
|--------------|--------------|
| `Roact.createElement` | `React.createElement` or JSX |
| `Roact.Component` | `React.Component:extend` |
| `Roact.Children` | `children` prop directly |
| `Roact.Event` | `React.Event` |
| `Roact.Change` | `React.Change` |
| `Roact.Ref` | `React.createRef` |

---

*Last Updated: February 2026*

*Note: This is hand-written documentation. When modifying, maintain the structure and accuracy of the information provided.*
