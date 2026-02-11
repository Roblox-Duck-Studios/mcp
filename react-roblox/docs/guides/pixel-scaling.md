# Pixel Scaling (Px)

## Overview

Most projects implement a `px` function and corresponding `usePx` hook to handle responsive scaling. These functions compute values based on screen size, allowing UI to scale properly across different devices.

## How It Works

- **`px(value)`** - Converts a design pixel value to the appropriate scale for the current screen
- **`usePx()`** - React hook that provides the px function and re-renders when screen size changes

## Usage Example

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

## Important Rules

1. **Offset Only** - Only use `px()` for the offset parameter (second argument in UDim/UDim2)
2. **Scale for Layout** - Use scale for responsive layout, offset for fixed sizes
3. **Screen-based** - Values are computed based on configured screen size reference

## Roblox UI Fundamentals

Understanding Roblox's UI positioning system is essential:

**UDim Structure:**
- `UDim.new(scale, offset)` - Single dimension
- `UDim2.new(xScale, xOffset, yScale, yOffset)` - Two dimensions

**Reference:** 
- [UI Position and Size](https://create.roblox.com/docs/ui/position-and-size)
- [Roblox UI Documentation](https://create.roblox.com/docs/ui)
