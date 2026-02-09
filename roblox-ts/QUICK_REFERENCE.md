# Roblox-ts - Quick Reference Card

## File Organization

```
roblox-ts/
├── README.md                    ← Start here
├── MCP_OVERVIEW.md             ← What this MCP covers
├── QUICK_REFERENCE.md          ← This file
└── docs/
    ├── INDEX.md                ← Navigation guide
    ├── introduction.md         (What is roblox-ts?)
    ├── quick-start.md          (Getting started)
    ├── setup-guide.md          (Installation)
    ├── usage.md                (How to use)
    ├── api/
    │   └── roblox-api.md       (API reference)
    └── guides/
        ├── syncing-with-rojo.md
        ├── using-existing-luau.md
        ├── typescript-packages.md
        ├── roact-jsx.md
        ├── typescript-transformers.md
        └── ... (other guides)
```

## Quick Setup

### Installation

```bash
# Windows (PowerShell)
npm install -g roblox-ts

# macOS / Linux
npm install -g roblox-ts
```

### Create New Project

```bash
# Interactive project creation
rbxtsc init

# Project types available:
# - game      (Roblox game)
# - model     (Game asset/model)
# - plugin    (Roblox Studio plugin)
# - package   (NPM package)
```

### Compile TypeScript

```bash
# Watch mode (auto-compile on save)
rbxtsc watch

# Single compile
rbxtsc build

# Watch with output details
rbxtsc watch --verbose
```

## File Structure

```
my-game/
├── src/
│   ├── shared/           # Code for client & server
│   ├── server/           # Server-only code
│   ├── client/           # Client-only code
│   └── init.lua          # Entry point
├── out/                  # Compiled Lua output
├── tsconfig.json         # TypeScript config
├── roblox.json           # Rojo config
└── package.json          # NPM config
```

## Common Commands

| Task | Command |
|------|---------|
| Create project | `rbxtsc init` |
| Watch changes | `rbxtsc watch` |
| Build once | `rbxtsc build` |
| Check syntax | `tsc --noEmit` |
| Format code | `prettier --write src/` |
| Lint code | `eslint src/` |

## TypeScript Basics for Roblox

### Instance Creation

```typescript
// Create GUI
const button = new Instance("TextButton")
button.Name = "MyButton"
button.Text = "Click Me"
button.Parent = game.Players.LocalPlayer.PlayerGui
```

### Declaring Types

```typescript
// Instance type
const humanoid: Humanoid = character.FindFirstChild("Humanoid") as Humanoid

// Union type for multiple possibilities
const instance: Part | Model = FindPart()

// Optional property
interface Config {
    enabled: boolean
    timeout?: number
}
```

### Class Components

```typescript
class MyClass extends Model {
    constructor(parent: Instance) {
        super()
        this.Part = new Instance("Part")
        this.Part.Parent = parent
    }

    public Part: Part
}
```

### Accessing Roblox API

```typescript
// Services
const Players = game.GetService("Players")
const RunService = game.GetService("RunService")

// Properties
const humanoidState = humanoid.GetState()

// Events
character.Humanoid.Died.Connect(() => {
    print("Player died!")
})

// Remote Functions/Events
game.ReplicatedStorage.GetChild("MyRemote") as RemoteEvent
```

## Syncing with Rojo

### Configuration (roblox.json)

```json
{
    "name": "my-game",
    "tree": {
        "$path": "out"
    },
    "servePort": 34872
}
```

### Commands

```bash
# Start Rojo server
rojo serve

# Connect in Roblox Studio
# 1. Open Rojo plugin in Studio
# 2. Click "Connect"
# 3. File changes sync automatically
```

## Dependencies & Packages

### Adding NPM Packages

```bash
# Add TypeScript package
npm install @rbxts/roact

# Import in code
import React from "@rbxts/roact"
```

### Common Packages

| Package | Use |
|---------|-----|
| `@rbxts/roact` | React-like UI library |
| `@rbxts/types` | Extra type definitions |
| `@rbxts/string-utils` | String utilities |
| `@rbxts/game-utils` | Game utilities |

## Common Patterns

### Connecting to Events

```typescript
// Simple connection
character.Humanoid.Died.Connect(() => {
    print("Died!")
})

// With cleanup
const connection = humanoid.Died.Connect(() => { ... })
connection.Disconnect()
```

### Working with Players

```typescript
// Get player
const player = game.Players.FindFirstChild("PlayerName") as Player

// Listen for new players
game.Players.PlayerAdded.Connect((player) => {
    print(`${player.Name} joined`)
})

// Listen for players leaving
game.Players.PlayerRemoving.Connect((player) => {
    print(`${player.Name} left`)
})
```

### Waiting for Descendants

```typescript
// Wait for child
const humanoid = character.WaitForChild("Humanoid") as Humanoid

// Find with type assertion
const rootPart = character.FindFirstChild("HumanoidRootPart") as Part
```

### Server/Client Communication

```typescript
// Server code (src/server/init.ts)
const remote = new Instance("RemoteEvent")
remote.Name = "MyRemote"
remote.Parent = game.ReplicatedStorage

remote.OnServerEvent.Connect((player: Player, message: string) => {
    print(`${player.Name}: ${message}`)
})

// Client code (src/client/init.ts)
const remote = game.ReplicatedStorage.WaitForChild("MyRemote") as RemoteEvent
remote.FireServer("Hello server!")
```

## Configuration

### tsconfig.json

```json
{
    "compilerOptions": {
        "target": "ES2020",
        "lib": ["es2020"],
        "robloxTypes": "roblox-ts/types"
    },
    "rbxtsc": {
        "typeCheckingMode": "strict",
        "paths": {
            "@/*": ["src/*"]
        }
    }
}
```

## Debugging Tips

### Print Debugging

```typescript
// Simple print
print("Value:", value)

// Inspect table
print(debug.traceback())

// Watch variable
let x = 10
print(`x = ${x}`)
```

### Type Checking

```bash
# Check for type errors without compiling
tsc --noEmit

# Verbose compile output
rbxtsc build --verbose
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "Cannot find module" | Check import path and `tsconfig.json` |
| Instance not found | Use `WaitForChild()` instead of `FindFirstChild()` |
| Type mismatch | Add type assertion: `as InstanceType` |
| Changes not syncing | Check Rojo is running and Studio connected |
| Undefined behavior | Check for `nil` values (use optionals) |

## API at a Glance

### Instance Methods

```typescript
// Finding
instance.FindFirstChild(name)
instance.FindFirstChildOfClass(className)
instance.FindFirstAncestorOfClass(className)

// Hierarchy
instance.Parent
instance:GetChildren()
instance:GetDescendants()

// Properties
instance:Clone()
instance:Destroy()
instance:IsDescendantOf(ancestor)
```

### Common Instances

```typescript
// GUI
TextLabel, TextButton, Frame, ScrollingFrame

// Parts
Part, Model, UnionOperation

// Scripting
Script, LocalScript, ModuleScript

// Players & Characters
Player, Character, Humanoid, HumanoidRootPart
```

## Resources

| Resource | Link |
|----------|------|
| Official Docs | [roblox-ts.com](https://roblox-ts.com) |
| GitHub | [github.com/roblox-ts/roblox-ts](https://github.com/roblox-ts/roblox-ts) |
| NPM Packages | [npmjs.com/@rbxts](https://www.npmjs.com/org/rbxts) |
| Discord | [discord.roblox-ts.com](https://discord.roblox-ts.com) |
| Roblox API | [create.roblox.com/docs](https://create.roblox.com/docs) |

## Navigation

| Need | Go To |
|------|-------|
| Getting started | [Quick Start](./docs/quick-start.md) |
| Installation | [Setup Guide](./docs/setup-guide.md) |
| How to use | [Usage Guide](./docs/usage.md) |
| API reference | [Roblox API](./docs/api/roblox-api.md) |
| Rojo setup | [Syncing with Rojo](./docs/guides/syncing-with-rojo.md) |
| Packages | [TypeScript Packages](./docs/guides/typescript-packages.md) |
| Full index | [INDEX](./docs/INDEX.md) |

---

**Use this card while coding for quick lookups**
