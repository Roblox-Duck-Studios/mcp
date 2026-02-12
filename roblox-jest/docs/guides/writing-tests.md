# Writing Tests

This guide covers the basics of writing tests with Roblox Jest.

## Basic Test Structure

A basic test file in Roblox TypeScript:

```typescript
import { describe, it, expect } from "@rbxts/jest-globals";
import { add } from "shared/utils/math";

describe("Math utils", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });
    
    it("should handle negative numbers", () => {
      expect(add(-2, 3)).toBe(1);
    });
  });
});
```

## Test Functions

### describe

Groups related tests together:

```typescript
describe("PlayerManager", () => {
  // All PlayerManager tests here
});
```

You can nest describes:

```typescript
describe("PlayerManager", () => {
  describe("createPlayer", () => {
    it("should create player with default stats", () => {
      // Test code
    });
  });
  
  describe("removePlayer", () => {
    it("should clean up player data", () => {
      // Test code
    });
  });
});
```

### it / test

Defines individual test cases:

```typescript
it("should do something", () => {
  // Test code
});

// Alternative syntax
test("should do something", () => {
  // Test code
});
```

### beforeEach / afterEach

Run code before/after each test:

```typescript
describe("Inventory", () => {
  let inventory: Inventory;
  
  beforeEach(() => {
    inventory = new Inventory();
  });
  
  afterEach(() => {
    inventory.destroy();
  });
  
  it("should add items", () => {
    inventory.addItem("sword");
    expect(inventory.getItems()).toContain("sword");
  });
});
```

### beforeAll / afterAll

Run code once before/after all tests:

```typescript
describe("Database", () => {
  beforeAll(() => {
    // Connect to test database once
  });
  
  afterAll(() => {
    // Clean up database connection
  });
  
  // Tests here
});
```

## Assertions

### Basic Matchers

```typescript
// Equality
expect(value).toBe(expected);
expect(value).toEqual(expected);  // Deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();

// Numbers
expect(value).toBeGreaterThan(5);
expect(value).toBeGreaterThanOrEqual(5);
expect(value).toBeLessThan(10);
expect(value).toBeLessThanOrEqual(10);

// Strings
expect(string).toContain("substring");
expect(string).toMatch(/regex/);

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
```

### Negation

Use `.not` to negate:

```typescript
expect(value).not.toBe(expected);
expect(array).not.toContain(item);
```

### Async Testing

```typescript
it("should resolve promise", async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});

it("should reject promise", async () => {
  await expect(fetchInvalidData()).rejects.toThrow();
});
```

## Testing Roblox-specific Code

### Testing Services

```typescript
import { Players, ReplicatedStorage } from "@rbxts/services";

describe("PlayerService", () => {
  it("should get all players", () => {
    const players = Players.GetPlayers();
    expect(players).toBeDefined();
  });
});
```

### Testing Events

```typescript
describe("EventSystem", () => {
  it("should fire event", () => {
    const event = new Instance("BindableEvent");
    let fired = false;
    
    event.Event.Connect(() => {
      fired = true;
    });
    
    event.Fire();
    expect(fired).toBe(true);
  });
});
```

### Testing Instance Creation

```typescript
describe("PartFactory", () => {
  it("should create part with properties", () => {
    const part = new Instance("Part");
    part.Size = new Vector3(1, 1, 1);
    part.Position = new Vector3(0, 10, 0);
    
    expect(part.Size).toEqual(new Vector3(1, 1, 1));
    expect(part.Position.Y).toBe(10);
  });
});
```

## Advanced Patterns

### Parameterized Tests

```typescript
describe("Math utils", () => {
  const testCases = [
    { input: [1, 2], expected: 3 },
    { input: [5, 5], expected: 10 },
    { input: [-1, 1], expected: 0 },
  ];
  
  testCases.forEach(({ input, expected }) => {
    it(`should add ${input[0]} + ${input[1]} = ${expected}`, () => {
      expect(add(input[0], input[1])).toBe(expected);
    });
  });
});
```

### Testing Exceptions

```typescript
describe("Validation", () => {
  it("should throw on invalid input", () => {
    expect(() => {
      validatePlayerId(-1);
    }).toThrow();
  });
  
  it("should throw specific error", () => {
    expect(() => {
      validatePlayerId(-1);
    }).toThrow("Invalid player ID");
  });
});
```
