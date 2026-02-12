# Code Coverage

Roblox Jest integrates with @rbxts/coverage to provide comprehensive code coverage reporting.

## Installation

Install the coverage package:

```bash
npm install @rbxts/coverage
```

## Basic Configuration

Enable coverage in your Jest configuration:

```typescript
// jest.server.config.ts
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests],
  testMatch: ["**/server/**/*.test"],
  collectCoverage: true,
  coverageDirectory: "coverage/server",
  coverageReporters: ["text", "lcov", "html"],
} satisfies Config;
```

## Coverage Options

### collectCoverage

Enable coverage collection:

```typescript
collectCoverage: true
```

### coverageDirectory

Specify where to output coverage reports:

```typescript
coverageDirectory: "coverage"
```

### coverageReporters

Choose which report formats to generate:

```typescript
coverageReporters: [
  "text",      // Console output
  "lcov",      // LCOV format for CI integration
  "html",      // HTML report
  "json",      // JSON data
  "clover"     // Clover XML format
]
```

### collectCoverageFrom

Specify which files to include/exclude:

```typescript
collectCoverageFrom: [
  "src/**/*.ts",
  "!src/**/*.test.ts",
  "!src/**/__tests__/**",
  "!src/**/*.d.ts"
]
```

### coverageThresholds

Set minimum coverage requirements:

```typescript
coverageThreshold: {
  global: {
    branches: 80,
    functions: 80,
    lines: 80,
    statements: 80
  }
}
```

## Complete Configuration Example

```typescript
// jest.shared.config.ts
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟠 SHARED",
  setupFiles: [setupTests],
  testMatch: ["**/shared/**/*.test"],
  
  // Coverage configuration
  collectCoverage: true,
  coverageDirectory: "coverage/shared",
  coverageReporters: ["text", "lcov", "html"],
  collectCoverageFrom: [
    "src/shared/**/*.ts",
    "!src/shared/**/*.test.ts",
    "!src/shared/**/__tests__/**",
    "!src/shared/**/*.d.ts"
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
} satisfies Config;
```

## Running with Coverage

### Command Line

```bash
# Run tests with coverage
jestrbx --coverage

# Run specific config with coverage
jestrbx --config jest.server.config.ts --coverage
```

### npm Scripts

```json
{
  "scripts": {
    "test:coverage": "jestrbx --coverage",
    "test:coverage:server": "jestrbx --config jest.server.config.ts --coverage",
    "test:coverage:client": "jestrbx --config jest.client.config.ts --coverage",
    "test:coverage:shared": "jestrbx --config jest.shared.config.ts --coverage"
  }
}
```

## Coverage Reports

### Text Report

Console output after test run:

```
----------|---------|----------|---------|---------|-------------------
File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
----------|---------|----------|---------|---------|-------------------
All files |   85.71 |    75.00 |   80.00 |   85.71 |                   
 utils.ts |   85.71 |    75.00 |   80.00 |   85.71 | 15,23-25         
----------|---------|----------|---------|---------|-------------------
```

### HTML Report

View detailed coverage in browser:

1. Run tests with coverage
2. Open `coverage/lcov-report/index.html`
3. Browse files and see uncovered lines highlighted

### LCOV Report

For CI/CD integration:

```
coverage/lcov.info
```

Integrate with services like:
- Codecov
- Coveralls
- SonarQube

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/coverage.yml
name: Coverage
on: [push, pull_request]
jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: npm install
      
      - name: Run tests with coverage
        run: npm run test:coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true
```

### Coverage Badges

Add coverage badges to README:

```markdown
[![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

## Best Practices

### 1. Set Realistic Thresholds

Start with achievable thresholds and increase over time:

```typescript
coverageThreshold: {
  global: {
    branches: 70,    // Start lower, increase gradually
    functions: 80,
    lines: 80,
    statements: 80
  }
}
```

### 2. Exclude Non-Testable Code

```typescript
collectCoverageFrom: [
  "src/**/*.ts",
  "!src/**/*.test.ts",
  "!src/**/__tests__/**",
  "!src/**/*.d.ts",
  "!src/types/**",           // Type definitions
  "!src/constants/**"        // Simple constants
]
```

### 3. Separate Coverage Reports

Generate separate reports for each environment:

```
coverage/
├── server/
│   └── lcov-report/
├── client/
│   └── lcov-report/
└── shared/
    └── lcov-report/
```

### 4. Watch Coverage Trends

Track coverage over time:
- Set up CI to fail if coverage drops
- Review coverage reports in PRs
- Celebrate coverage improvements!
