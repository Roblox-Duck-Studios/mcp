# Writing React Stories

## UI Labs Integration

We use **`@rbxts/ui-labs`** to render and visualize stories. Every component should have a corresponding story for development and testing.

## Basic Story Structure

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

## Story Best Practices

1. **Wrap with StrictMode** - Always wrap the top layer with StrictMode
2. **Use Root Provider** - Most projects have a root provider for global state/context
3. **Component Isolation** - Render only the component being tested
4. **Controls** - Add controls to test different props values

## Adding Controls

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
