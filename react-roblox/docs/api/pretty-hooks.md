# Pretty React Hooks

## Overview

**`pretty-react-hooks`** provides utility hooks for common React patterns in Roblox development. It offers hooks for debouncing, throttling, previous values, and more.

## Installation

```bash
npm install @rbxts/pretty-react-hooks
```

## Available Hooks

The library includes hooks such as:

- **`usePrevious`** - Track previous values
- **`useDebouncedState`** - Debounce state updates
- **`useThrottle`** - Throttle function calls
- **`useMount`** - Run effect on mount only
- **`useUnmount`** - Cleanup on unmount
- **`useUpdateEffect`** - Skip first render effect

## Basic Usage

```tsx
import { usePrevious, useDebouncedState } from "@rbxts/pretty-react-hooks";

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
