# Test Structure

This guide covers the recommended directory structure and organization for Roblox Jest tests.

## Directory Structure Overview

```
project-root/
├── src/
│   ├── client/
│   │   ├── components/
│   │   ├── controllers/
│   │   └── __tests__/
│   │       ├── components/
│   │       └── controllers/
│   ├── server/
│   │   ├── services/
│   │   ├── systems/
│   │   └── __tests__/
│   │       ├── services/
│   │       └── systems/
│   └── shared/
│       ├── utils/
│       ├── types/
│       └── __tests__/
│           ├── utils/
│           └── types/
├── setup-tests.ts
├── jest.server.config.ts
├── jest.client.config.ts
└── jest.shared.config.ts
```

## Test File Naming

### Convention

- **Test files**: Must end with `.test.ts`
- **Test configuration**: `jest.{environment}.config.ts`
- **Setup files**: `setup-tests.ts`, `{name}-setup.ts`

### Examples

```
src/server/__tests__/
├── playerService.test.ts
├── gameLoop.test.ts
└── matchmaking.test.ts
```

## Environment-Specific Structure

### Server Tests (🟢 SERVER)

```
src/server/
├── services/
│   ├── PlayerService.ts
│   ├── GameService.ts
│   └── DataService.ts
└── __tests__/
    └── services/
        ├── PlayerService.test.ts
        ├── GameService.test.ts
        └── DataService.test.ts
```

Configuration:

```typescript
// jest.server.config.ts
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests],
  testMatch: ["**/server/**/*.test"],
} satisfies Config;
```

### Client Tests (🔵 CLIENT)

```
src/client/
├── controllers/
│   ├── UIController.ts
│   ├── InputController.ts
│   └── CameraController.ts
└── __tests__/
    └── controllers/
        ├── UIController.test.ts
        ├── InputController.test.ts
        └── CameraController.test.ts
```

Configuration:

```typescript
// jest.client.config.ts
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🔵 CLIENT",
  setupFiles: [setupTests],
  testMatch: ["**/client/**/*.test"],
} satisfies Config;
```

### Shared Tests (🟠 SHARED)

```
src/shared/
├── utils/
│   ├── math.ts
│   ├── validation.ts
│   └── formatting.ts
└── __tests__/
    └── utils/
        ├── math.test.ts
        ├── validation.test.ts
        └── formatting.test.ts
```

Configuration:

```typescript
// jest.shared.config.ts
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟠 SHARED",
  setupFiles: [setupTests],
  testMatch: ["**/shared/**/*.test"],
} satisfies Config;
```

## Organizing Tests by Feature

Alternative structure organizing by feature instead of layer:

```
src/
├── features/
│   ├── combat/
│   │   ├── server/
│   │   │   └── CombatService.ts
│   │   ├── shared/
│   │   │   └── CombatTypes.ts
│   │   └── __tests__/
│   │       ├── CombatService.test.ts
│   │       └── CombatTypes.test.ts
│   └── inventory/
│       ├── client/
│       │   └── InventoryUI.ts
│       ├── server/
│       │   └── InventoryService.ts
│       └── __tests__/
│           ├── InventoryUI.test.ts
│           └── InventoryService.test.ts
```

Configuration for feature-based structure:

```typescript
// jest.config.ts (for all tests)
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🎮 FEATURES",
  setupFiles: [setupTests],
  testMatch: ["**/__tests__/**/*.test"],
} satisfies Config;
```

## Test Utilities

Create reusable test utilities:

```
src/
├── shared/
│   └── test-utils/
│       ├── mockPlayers.ts
│       ├── mockData.ts
│       └── testHelpers.ts
```

Example test utility:

```typescript
// src/shared/test-utils/mockPlayers.ts
import { Players } from "@rbxts/services";

export function createMockPlayer(userId: number): Player {
  const player = new Instance("Player");
  player.UserId = userId;
  player.Name = `Player${userId}`;
  return player as Player;
}

export function mockPlayerList(count: number): Player[] {
  const players: Player[] = [];
  for (let i = 1; i <= count; i++) {
    players.push(createMockPlayer(i));
  }
  return players;
}
```

## Configuration Files

### Root Directory Files

```
project-root/
├── jest.server.config.ts      # Server test config
├── jest.client.config.ts      # Client test config
├── jest.shared.config.ts      # Shared test config
├── setup-tests.ts             # Required setup module
├── jest.config.ts             # Default/merged config (optional)
└── package.json               # Test scripts
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "jestrbx",
    "test:server": "jestrbx --config jest.server.config.ts",
    "test:client": "jestrbx --config jest.client.config.ts",
    "test:shared": "jestrbx --config jest.shared.config.ts",
    "test:watch": "jestrbx --watch",
    "test:coverage": "jestrbx --coverage"
  }
}
```
