# Configuration

Roblox Jest requires configuration files for each test environment. This guide covers the configuration structure and options.

## Test Environments

Roblox Jest supports three distinct test environments:

- **🟢 SERVER** - Server-side code tests
- **🔵 CLIENT** - Client-side code tests
- **🟠 SHARED** - Shared module tests

## Directory Structure

Your test files should follow this structure:

```
src/
├── client/
│   └── __tests__/
│       └── *.test.ts
├── server/
│   └── __tests__/
│       └── *.test.ts
└── shared/
    └── __tests__/
        └── *.test.ts
```

## Configuration Files

Create separate Jest configuration files for each environment:

### Server Configuration (jest.server.config.ts)

```typescript
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests],
  testMatch: ["**/server/**/*.test"],
} satisfies Config;
```

### Client Configuration (jest.client.config.ts)

```typescript
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🔵 CLIENT",
  setupFiles: [setupTests],
  testMatch: ["**/client/**/*.test"],
} satisfies Config;
```

### Shared Configuration (jest.shared.config.ts)

```typescript
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟠 SHARED",
  setupFiles: [setupTests],
  testMatch: ["**/shared/**/*.test"],
} satisfies Config;
```

## Configuration Options

### displayName

A string identifier shown in test output to distinguish environments:

```typescript
displayName: "🟢 SERVER"
```

### setupFiles

Array of module scripts to run before tests. **Required** to include `setupTests`:

```typescript
setupFiles: [setupTests]
```

⚠️ **Important**: Without setupTests, you'll encounter runtime errors that cause all tests to fail.

### testMatch

Glob patterns to match test files:

```typescript
testMatch: ["**/*.test"]  // Matches all .test.ts files
testMatch: ["**/server/**/*.test"]  // Server tests only
testMatch: ["**/client/**/*.test"]  // Client tests only
```

## Advanced Configuration

### Multiple Test Patterns

You can specify multiple patterns:

```typescript
testMatch: [
  "**/server/**/*.test",
  "**/services/**/*.test"
]
```

### Custom Setup Files

Add multiple setup files for different purposes:

```typescript
import serverSetup from "./server-setup";
import commonSetup from "./setup-tests";

export = {
  displayName: "🟢 SERVER",
  setupFiles: [commonSetup, serverSetup],
  testMatch: ["**/server/**/*.test"],
} satisfies Config;
```

### Coverage Configuration

Enable coverage reporting:

```typescript
export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests],
  testMatch: ["**/server/**/*.test"],
  collectCoverage: true,
  coverageDirectory: "coverage/server",
  coverageReporters: ["text", "lcov"],
} satisfies Config;
```

## Package.json Scripts

Add convenient npm scripts:

```json
{
  "scripts": {
    "test:server": "jestrbx --config jest.server.config.ts",
    "test:client": "jestrbx --config jest.client.config.ts",
    "test:shared": "jestrbx --config jest.shared.config.ts",
    "test": "npm run test:shared && npm run test:server && npm run test:client",
    "test:coverage": "jestrbx --coverage"
  }
}
```
