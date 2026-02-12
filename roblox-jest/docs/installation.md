# Installation

This guide will walk you through installing Roblox Jest in your roblox-ts project.

## Required Packages

Install the following packages via npm:

```bash
npm install @rbxts/jest@alpha @rbxts/jest-globals@alpha
```

For code coverage support, also install:

```bash
npm install @rbxts/coverage
```

## Package Overview

### @rbxts/jest

The core Jest testing framework adapted for Roblox. Provides:
- Test runner functionality
- Assertion libraries
- Mocking capabilities
- Configuration types

### @rbxts/jest-globals

Global type definitions and utilities for Jest:
- Type definitions for `describe`, `it`, `expect`, etc.
- Global test environment setup

### @rbxts/coverage

Code coverage reporting for your tests:
- Line coverage tracking
- Branch coverage analysis
- Coverage reports generation

## TypeScript Configuration

Ensure your `tsconfig.json` includes the Jest types:

```json
{
  "compilerOptions": {
    "types": ["@rbxts/jest-globals"]
  }
}
```

## Installing Jestrbx CLI

For running tests, install the jestrbx CLI tool:

```bash
npm install -g jestrbx
```

Or as a dev dependency:

```bash
npm install --save-dev jestrbx
```

The CLI tool wraps the Roblox Jest runtime and provides:
- Local path rewriting for test results
- Integration with roblox-ts and Rojo workflows
- Familiar Jest-style output

## Verification

After installation, verify your setup by creating a simple test file:

```typescript
// src/__tests__/example.test.ts
import { describe, it, expect } from "@rbxts/jest-globals";

describe("Example Test", () => {
  it("should pass", () => {
    expect(true).toBe(true);
  });
});
```

## Next Steps

- [Configure your test environments](./configuration.md)
- [Learn about setup tests](./setup-tests.md)
- [Read the test structure guide](./guides/test-structure.md)
