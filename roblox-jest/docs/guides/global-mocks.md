# Global Mocks

Global mocks allow you to track and control how your implementation interacts with Luau globals. This is useful for testing console output, controlling random number generation for deterministic tests, and mocking other global functions.

## Overview

Jest can replace global function implementations, giving you a familiar interface for mocking functions like `print()`, `math.random()`, and more. This is done using `jest.globalEnv` as if you're spying on a table.

## Limitations

Not all globals can be mocked. Jest Roblox only supports mocking whitelisted globals. If you try to mock a non-whitelisted global, you'll see an error like:

```
Jest does not yet support mocking the require global.
```

### Unsupported Globals

The following globals **cannot** be mocked:

- `game:GetService()` and other Instance methods
- The `require()` function (use `jest.mock()` instead)
- Task scheduling functions (use Timer Mocks instead)

## Mocking Global Functions

### Mocking print()

Track and control console output in your tests:

```typescript
import { describe, it, expect, jest } from "@rbxts/jest-globals";
import { logMessage } from "shared/utils/logging";

describe("logMessage", () => {
  it("should print the correct message", () => {
    const mockPrint = jest.spyOn(jest.globalEnv, "print");
    mockPrint.mockImplementationOnce((message: string) => {
      expect(message).toContain("Player joined");
    });

    logMessage("Player joined the game");
    
    expect(mockPrint).toHaveBeenCalledTimes(1);
  });
});
```

### Mocking warn()

Test warning messages:

```typescript
import { describe, it, expect, jest } from "@rbxts/jest-globals";
import { validateInput } from "shared/validation";

describe("validateInput", () => {
  it("should warn on invalid input", () => {
    const mockWarn = jest.spyOn(jest.globalEnv, "warn");
    
    validateInput(-5); // Should trigger a warning
    
    expect(mockWarn).toHaveBeenCalledWith(expect.stringContaining("Invalid"));
  });
});
```

## Mocking Library Functions

### Mocking math.random()

Get deterministic, predictable random numbers for testing:

```typescript
import { describe, it, expect, jest } from "@rbxts/jest-globals";
import { rollDice } from "shared/game/dice";

describe("rollDice", () => {
  it("should return correctly formatted message", () => {
    // Mock math.random to always return 5
    const mockRandom = jest.spyOn(jest.globalEnv.math, "random");
    mockRandom.mockImplementationOnce(() => 5);
    
    const result = rollDice(6); // Roll a 6-sided die
    
    expect(result).toBe("You rolled a 5");
    expect(mockRandom).toHaveBeenCalledWith(1, 6);
  });
  
  it("should handle multiple rolls", () => {
    const mockRandom = jest.spyOn(jest.globalEnv.math, "random");
    
    // Return different values for consecutive calls
    mockRandom
      .mockReturnValueOnce(2)
      .mockReturnValueOnce(4)
      .mockReturnValueOnce(6);
    
    expect(rollDice(6)).toBe("You rolled a 2");
    expect(rollDice(6)).toBe("You rolled a 4");
    expect(rollDice(6)).toBe("You rolled a 6");
  });
});
```

### Mocking math.randomseed()

Control random seed for reproducible tests:

```typescript
import { describe, it, expect, jest, beforeEach } from "@rbxts/jest-globals";
import { generateWorld } from "server/world/generator";

describe("generateWorld", () => {
  beforeEach(() => {
    // Reset the random seed before each test
    const mockSeed = jest.spyOn(jest.globalEnv.math, "randomseed");
    mockSeed.mockImplementation(() => {});
  });
  
  it("should generate consistent world with same seed", () => {
    const mockRandom = jest.spyOn(jest.globalEnv.math, "random");
    mockRandom.mockReturnValue(0.5);
    
    const world1 = generateWorld(12345);
    const world2 = generateWorld(12345);
    
    expect(world1).toEqual(world2);
  });
});
```

### Mocking os.time()

Test time-dependent logic:

```typescript
import { describe, it, expect, jest } from "@rbxts/jest-globals";
import { isDailyRewardAvailable } from "shared/rewards/daily";

describe("isDailyRewardAvailable", () => {
  it("should return true after 24 hours", () => {
    const mockTime = jest.spyOn(jest.globalEnv.os, "time");
    const baseTime = 1609459200; // Jan 1, 2021 00:00:00
    
    // First call returns base time (last claim)
    // Second call returns base time + 25 hours
    mockTime
      .mockReturnValueOnce(baseTime)
      .mockReturnValueOnce(baseTime + 90000);
    
    expect(isDailyRewardAvailable()).toBe(true);
  });
});
```

## Accessing Original Implementations

You can access the original (non-mocked) implementation at any time:

```typescript
import { describe, it, expect, jest } from "@rbxts/jest-globals";

describe("original implementations", () => {
  it("can access original math.random", () => {
    const mockRandom = jest.spyOn(jest.globalEnv.math, "random");
    mockRandom.mockImplementation(() => 5);
    
    // This will return 5 (mocked)
    const mocked = math.random();
    
    // This will return actual random number (unmocked)
    const unmocked = jest.globalEnv.math.random();
    
    expect(mocked).toBe(5);
    expect(unmocked).not.toBe(5);
    expect(unmocked).toBeGreaterThanOrEqual(0);
    expect(unmocked).toBeLessThan(1);
  });
});
```

## Restoring Mocks

Always clean up mocks after tests:

```typescript
import { describe, it, expect, jest, beforeEach, afterEach } from "@rbxts/jest-globals";

describe("with restored mocks", () => {
  let mockPrint: jest.SpyInstance;
  
  beforeEach(() => {
    mockPrint = jest.spyOn(jest.globalEnv, "print");
  });
  
  afterEach(() => {
    mockPrint.mockRestore();
  });
  
  it("test with mocked print", () => {
    mockPrint.mockImplementation(() => {});
    // Test code
  });
  
  it("test with different mock", () => {
    mockPrint.mockImplementation((msg) => `Logged: ${msg}`);
    // Test code
  });
});
```

## Common Patterns

### Suppressing Console Output

Keep test output clean:

```typescript
beforeAll(() => {
  jest.spyOn(jest.globalEnv, "print").mockImplementation(() => {});
  jest.spyOn(jest.globalEnv, "warn").mockImplementation(() => {});
});
```

### Testing Error Conditions

Mock error functions:

```typescript
it("should handle errors gracefully", () => {
  const mockError = jest.spyOn(jest.globalEnv, "error");
  mockError.mockImplementation(() => {});
  
  riskyOperation();
  
  expect(mockError).not.toHaveBeenCalled();
});
```

### Deterministic UUID Generation

For testing UUID generation logic:

```typescript
it("should generate expected UUID", () => {
  const mockRandom = jest.spyOn(jest.globalEnv.math, "random");
  let counter = 0;
  mockRandom.mockImplementation(() => {
    counter += 0.1;
    return counter % 1;
  });
  
  const uuid = generateUUID();
  expect(uuid).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
});
```

## Best Practices

1. **Always restore mocks** after tests to prevent interference
2. **Use mockImplementationOnce** when you only need one specific return value
3. **Access original implementations** via `jest.globalEnv` when you need real behavior
4. **Don't mock unsupported globals** - use alternative approaches
5. **Document why** you're mocking a global to help future maintainers
