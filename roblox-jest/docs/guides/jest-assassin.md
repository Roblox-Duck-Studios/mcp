# Jest Roblox Assassin

Jestrbx (Jest Roblox Assassin) is a CLI tool for running Jest-style tests against Roblox places.

## Overview

Jestrbx wraps the Roblox Jest runtime and provides:
- Local path rewriting for test results
- Integration with roblox-ts and Rojo workflows
- Familiar Jest-style output and experience

## Installation

### Global Installation

```bash
npm install -g jestrbx
```

### Local Installation

```bash
npm install --save-dev jestrbx
```

## Basic Usage

### Run All Tests

```bash
jestrbx
```

### Run Specific Configuration

```bash
jestrbx --config jest.server.config.ts
jestrbx --config jest.client.config.ts
jestrbx --config jest.shared.config.ts
```

### Run Tests Matching Pattern

```bash
jestrbx --testNamePattern="PlayerService"
jestrbx --testPathPattern="server"
```

## CLI Options

### --config

Specify a configuration file:

```bash
jestrbx --config jest.server.config.ts
```

### --coverage

Enable code coverage:

```bash
jestrbx --coverage
```

### --testNamePattern

Run tests matching a pattern:

```bash
jestrbx --testNamePattern="should create player"
```

### --testPathPattern

Run tests in files matching a pattern:

```bash
jestrbx --testPathPattern="PlayerService"
```

### --verbose

Show detailed output:

```bash
jestrbx --verbose
```

### --watch

Run tests in watch mode (if supported):

```bash
jestrbx --watch
```

### --no-coverage

Disable coverage even if enabled in config:

```bash
jestrbx --no-coverage
```

## Configuration File

Create a `jestrbx.config.js` for default settings:

```javascript
module.exports = {
  config: "jest.shared.config.ts",
  coverage: true,
  verbose: true
};
```

## Integration with roblox-ts

### Build Before Testing

Ensure your TypeScript is compiled:

```json
{
  "scripts": {
    "build": "rbxtsc",
    "test": "npm run build && jestrbx",
    "test:server": "npm run build && jestrbx --config jest.server.config.ts"
  }
}
```

### Rojo Integration

Jestrbx works with Rojo projects:

```bash
# Sync with Rojo first
rojo build --output game.rbxlx

# Then run tests
jestrbx
```

## Output Format

Jestrbx provides Jest-style output:

```
🟢 SERVER
  PlayerService
    ✓ should create player data for new players (45ms)
    ✓ should load existing player data (32ms)
    ✓ should handle invalid player IDs (12ms)

  GameService
    ✓ should initialize game state (23ms)
    ✓ should start game with enough players (56ms)
    ✓ should reject game start with insufficient players (18ms)

Test Suites: 2 passed, 2 total
Tests:       6 passed, 6 total
Snapshots:   0 total
Time:        2.345s
```

## Path Rewriting

Jestrbx automatically rewrites Roblox paths to local source paths:

```
# Roblox path (in logs)
game.ServerScriptService.Services.PlayerService

# Rewritten to local path
src/server/services/PlayerService.ts
```

This makes it easier to:
- Identify failing tests
- Navigate to source files
- Debug test failures

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Install roblox-ts
        run: npm install -g roblox-ts
      
      - name: Install jestrbx
        run: npm install -g jestrbx
      
      - name: Build TypeScript
        run: rbxtsc
      
      - name: Run Server Tests
        run: jestrbx --config jest.server.config.ts
      
      - name: Run Client Tests
        run: jestrbx --config jest.client.config.ts
      
      - name: Run Shared Tests
        run: jestrbx --config jest.shared.config.ts
```

## Troubleshooting

### Tests Not Found

Ensure test files match your `testMatch` pattern:

```typescript
// Must end with .test.ts
testMatch: ["**/*.test"]
```

### Runtime Errors

Make sure `setupTests` is included in your config:

```typescript
setupFiles: [setupTests]
```

### Path Issues

Check that roblox-ts has been compiled before running tests:

```bash
rbxtsc && jestrbx
```

### Slow Tests

Use verbose mode to identify slow tests:

```bash
jestrbx --verbose
```

## Additional Resources

- [GitHub Repository](https://github.com/Unreal-Works/jest-roblox-assassin)
- [Issue Tracker](https://github.com/Unreal-Works/jest-roblox-assassin/issues)
- [npm Package](https://www.npmjs.com/package/jestrbx)
