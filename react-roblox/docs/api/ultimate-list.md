# Ultimate List

## Overview

**`@rbxts/ultimate-list`** creates fast, efficient virtualized lists in Roblox. It only renders items that are actually visible, reducing engine load and improving performance.

## Key Benefits

1. **Performance** - Only visible items are created/rendered
2. **Deferred Execution** - Components only run when visible
3. **Zero Re-renders** - Can update without React re-renders using bindings
4. **Type Safety** - Full TypeScript/Luau type support

## Features

- Arbitrarily sized and positioned elements
- Grid and list layouts
- State-based or binding-based rendering
- Optimizations for consistent-sized elements

## Installation

```bash
npm install @rbxts/ultimate-list
```

## Basic List Example

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

## Grid Example

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

## Binding-Based Renderer (Zero Re-renders)

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

## Key Components

| Component | Description |
|-----------|-------------|
| `UltimateList.Components.ScrollingFrame` | Virtualized scrolling container |
| `UltimateList.DataSources.array` | Array data source |
| `UltimateList.Dimensions.consistentSize` | Fixed size dimensions |
| `UltimateList.Dimensions.consistentUDim2` | Fixed UDim2 dimensions |
| `UltimateList.Renderers.byState` | State-based rendering |
| `UltimateList.Renderers.byBinding` | Binding-based rendering |

**Reference:** [Ultimate List Documentation](https://kampfkarren.github.io/ultimate-list/)
