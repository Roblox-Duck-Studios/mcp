# Best Practices

Follow these best practices to get the most out of Roblox Jest and ensure comprehensive test coverage.

## Test Coverage Goals

Aim for the highest possible test coverage:

- **Target**: 80%+ coverage minimum
- **Ideal**: 100% coverage for critical paths
- **Focus**: Cover every case in your code

### Coverage Metrics

Track these metrics using @rbxts/coverage:

- **Line Coverage**: Percentage of lines executed
- **Branch Coverage**: Percentage of decision branches taken
- **Function Coverage**: Percentage of functions called

## Test Organization

### File Structure

```
src/
├── client/
│   ├── components/
│   ├── services/
│   └── __tests__/
│       ├── components/
│       └── services/
├── server/
│   ├── services/
│   └── __tests__/
│       └── services/
└── shared/
    ├── utils/
    └── __tests__/
        └── utils/
```
you do not always need `services` or `components` in a project.

### Naming Conventions

- Test files: `*.test.ts`
- Test suites: Describe the module being tested
- Test cases: Describe the behavior being tested

```typescript
// Good naming
describe("PlayerService", () => {
  describe("joinPlayer", () => {
    it("should create player data for new players", () => {
      // Test code
    });
    
    it("should load existing player data", () => {
      // Test code
    });
  });
});
```

## Writing Effective Tests

### AAA Pattern

Structure tests using Arrange-Act-Assert:

```typescript
import { describe, it, expect } from "@rbxts/jest-globals";
import { calculateDamage } from "shared/combat/damage";

describe("calculateDamage", () => {
  it("should calculate damage with weapon modifier", () => {
    // Arrange
    const baseDamage = 100;
    const weaponMultiplier = 1.5;
    
    // Act
    const result = calculateDamage(baseDamage, weaponMultiplier);
    
    // Assert
    expect(result).toBe(150);
  });
});
```

### Test Independence

Each test should be independent:

```typescript
// Good - independent tests
describe("Inventory", () => {
  it("should add item", () => {
    const inventory = new Inventory();
    inventory.addItem("sword");
    expect(inventory.hasItem("sword")).toBe(true);
  });
  
  it("should remove item", () => {
    const inventory = new Inventory();
    inventory.addItem("shield");
    inventory.removeItem("shield");
    expect(inventory.hasItem("shield")).toBe(false);
  });
});
```

### Edge Cases

Always test edge cases:

```typescript
describe("divide", () => {
  it("should divide two positive numbers", () => {
    expect(divide(10, 2)).toBe(5);
  });
  
  it("should handle division by zero", () => {
    expect(() => divide(10, 0)).toThrow();
  });
  
  it("should handle negative numbers", () => {
    expect(divide(-10, 2)).toBe(-5);
  });
  
  it("should handle zero dividend", () => {
    expect(divide(0, 5)).toBe(0);
  });
});
```

## Mocking

Mocking modules with module script is currently hacky and no easy way is found, but jest.fn still works as intended.

### Global Mocks

Roblox Jest supports mocking global functions like `print()`, `math.random()`, `warn()`, and more using `jest.globalEnv`. This is particularly useful for:

- Capturing and testing console output
- Controlling random number generation for deterministic tests
- Testing time-dependent logic with `os.time()`
- Suppressing unwanted output during tests

Example of mocking `print()`:

```typescript
import { describe, it, expect, jest } from "@rbxts/jest-globals";

describe("console output", () => {
  it("should print the correct message", () => {
    const mockPrint = jest.spyOn(jest.globalEnv, "print");
    mockPrint.mockImplementationOnce((message: string) => {
      expect(message).toContain("Player joined");
    });

    // Your code that calls print()
    
    expect(mockPrint).toHaveBeenCalledTimes(1);
  });
});
```

See the [Global Mocks guide](./global-mocks.md) for detailed documentation on mocking global functions.

**Note:** Not all globals can be mocked. Unsupported globals include:
- `game:GetService()` and other Instance methods
- The `require()` function (use `jest.mock()` instead)
- Task scheduling functions (use Timer Mocks instead)

## Performance

### Fast Tests

Keep tests fast:
- Avoid real network calls
- Use mocks for external dependencies
- Don't test implementation details

### Test Suites

Group related tests:

```typescript
describe("CombatSystem", () => {
  describe("damage calculation", () => {
    // Damage tests
  });
  
  describe("status effects", () => {
    // Status effect tests
  });
  
  describe("knockback", () => {
    // Knockback tests
  });
});
```

## Continuous Integration

### CI Configuration

Run tests in CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### Pre-commit Hooks

Run tests before committing:

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "npm test"
    }
  }
}
```
