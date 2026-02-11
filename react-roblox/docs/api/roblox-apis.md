# Roblox-Specific APIs

## Overview

React Roblox includes APIs unique to the Roblox platform that have no React JS equivalent.

## React.None

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

## React.Event

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

## React.Change

Connect to property change signals:

```tsx
<scrollingframe
  Change={{
    CanvasPosition: (rbx) => print("Scrolled to", rbx.CanvasPosition)
  }}
/>
```

## React.Tag

Apply CollectionService tags:

```tsx
<frame
  {...{ [React.Tag]: "my-tag another-tag" }}
/>
```

## Bindings

Bindings are reactive containers that auto-update:

```tsx
// useBinding hook
const [position, setPosition] = React.useBinding(new UDim2());

// createBinding (for class components)
const [position, setPosition] = React.createBinding(new UDim2());

// joinBindings
const combined = React.joinBindings({ x: bindingX, y: bindingY });
```
