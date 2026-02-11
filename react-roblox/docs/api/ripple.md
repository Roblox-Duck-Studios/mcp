# Ripple - Animation Library

## Overview

**`@rbxts/ripple`** is an animation library inspired by react-spring, providing an imperative API for smooth transitions and animations in Roblox.

## Installation

```bash
npm install @rbxts/ripple
```

## Core Concepts

Ripple provides three main animation primitives:

1. **`useSpring`** - Physics-based spring animations
2. **`useTween`** - Time-based easing animations
3. **`useMotion`** - Hybrid that can switch between spring and tween

## Supported Types

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

## Spring Animation Example

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

## Motion Animation Example

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

## Spring Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `tension` | `number` | Number of bounces (default: 170) |
| `friction` | `number` | Spring damping (default: 26) |
| `mass` | `number` | Speed and bounce height (default: 1) |
| `frequency` | `number` | Response speed (alternative to tension) |
| `dampingRatio` | `number` | Decay rate (alternative to friction) |
| `precision` | `number` | Distance to goal before idle (default: 0.001) |
| `start` | `boolean` | Auto-start animation (default: false) |

## Tween Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `easing` | `string` | Easing function name |
| `duration` | `number` | Animation duration in seconds |
| `repeats` | `number` | Number of times to repeat |
| `reverses` | `boolean` | Reverse on repeat |

## Available Easing Functions

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
