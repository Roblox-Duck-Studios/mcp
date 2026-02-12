# Setup Tests Module

The setup tests module is a **critical** component of Roblox Jest. Without it, tests will fail with runtime errors.

## Purpose

The setup tests module clears registered modules to reset the roblox-ts runtime between test runs. This prevents module caching issues that can cause tests to fail or produce inconsistent results.

## Implementation

Create a file named `setup-tests.ts` (or similar) with the following content:

```typescript
for (const [key] of pairs(_G)) {
  // Clear registered modules to reset the roblox-ts runtime
  if (typeIs(key, "Instance") && key.IsA("ModuleScript")) {
    _G[key as unknown as keyof typeof _G] =
      undefined as unknown as (typeof _G)[keyof typeof _G];
  }
}

export = script as ModuleScript;
```

## How It Works

1. **Iterates through _G**: The global table `_G` contains all registered modules
2. **Identifies ModuleScripts**: Checks if a key is an Instance of type ModuleScript
3. **Clears References**: Sets module references to `undefined`
4. **Exports Script**: Returns the current script as a ModuleScript

This process ensures a clean state for each test run, preventing:
- Module caching issues
- State leakage between tests
- Inconsistent test results

## Placement

Place `setup-tests.ts` at the root of your test directory:

```
project/
├── src/
│   ├── client/
│   ├── server/
│   └── shared/
├── setup-tests.ts
├── jest.server.config.ts
├── jest.client.config.ts
└── jest.shared.config.ts
```

## Configuration

Import and include in your Jest config:

```typescript
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests],  // Must be included
  testMatch: ["**/server/**/*.test"],
} satisfies Config;
```

⚠️ **Warning**: Never omit `setupFiles: [setupTests]` from your configuration. Doing so will result in runtime errors that cause all tests to fail.

## Multiple Setup Files

If you need additional setup logic, create separate files:

```typescript
// setup-tests.ts - Required cleanup
for (const [key] of pairs(_G)) {
  if (typeIs(key, "Instance") && key.IsA("ModuleScript")) {
    _G[key as unknown as keyof typeof _G] =
      undefined as unknown as (typeof _G)[keyof typeof _G];
  }
}

export = script as ModuleScript;
```

```typescript
// test-helpers.ts - Optional additional setup
import { expect } from "@rbxts/jest-globals";

// Add custom matchers
expect.extend({
  // Custom matchers here
});

export = script as ModuleScript;
```

Then include both in your config:

```typescript
export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests, testHelpers],
  testMatch: ["**/server/**/*.test"],
} satisfies Config;
```
