# Project Reference: Slither

Real-world React patterns from the Slither game project.

**Repository**: https://github.com/littensy/slither  
**Structure**: Client/Server/Shared architecture using React

## Project Organization

```
slither/
├── src/
│   ├── client/       # Client-side React components and logic
│   ├── server/       # Server-side game logic
│   └── shared/       # Shared utilities and types
├── scripts/          # Build and utility scripts
├── default.project.json  # Rojo project configuration
└── tsconfig.json
```

## React Usage Patterns

### Component Architecture

Slither demonstrates:
- **Functional components** with hooks as the primary pattern
- **State management** for game state (players, leaderboard, etc.)
- **Event handling** for user input and game events
- **Roblox integration** connecting React UI to game logic

### Key Patterns

1. **Game State Binding**
   - Components react to game state changes
   - Real-time UI updates during gameplay
   - Leaderboard and player status display

2. **Event-Driven UI**
   - Responding to player actions
   - Game events triggering UI changes
   - Real-time game updates reflected in UI

3. **Component Hierarchy**
   - Top-level game component
   - Sub-components for UI sections (HUD, leaderboard, settings)
   - Reusable UI elements

### Notable Files

- **Client structure**: Demonstrates how to organize client-side React code
- **Event listeners**: Shows integration with Roblox events
- **State updates**: Examples of managing game state through React
- **Type system**: TypeScript integration for type safety

## Learning Points

1. **How to structure a multiplayer game UI with React**
   - Managing player state
   - Real-time updates
   - Network synchronization

2. **Integration patterns**
   - Connecting React to Roblox services
   - Handling game events
   - Managing component lifecycle with game state

3. **Performance considerations**
   - Efficient re-rendering
   - Minimizing updates
   - Optimizing for game runtime

## Common Patterns Used

### State Management
- Uses `useState` for local component state
- Uses hooks for stateful logic
- Manages game state reactively

### Effects
- `useEffect` for initialization and cleanup
- Subscribing to game events
- Managing connections and resources

### Props Pattern
- Configuration through props
- Composition of UI components
- Data flow from parent to child

## Repository Structure Takeaways

1. **Clear separation** - Client, server, shared code clearly separated
2. **Type safety** - TypeScript for compile-time type checking
3. **Module organization** - Logical grouping of related functionality
4. **Configuration** - Proper build configuration with Rojo

## References in Your Project

When building your Roblox game with React:
- Study how Slither organizes its client code
- Reference how game state flows through components
- Learn from their component hierarchy patterns
- Understand how they integrate Roblox events with React

## Key Takeaway

Slither shows a production-ready approach to building game UIs with React on Roblox, demonstrating how to effectively integrate game logic with React's component model.

---

**See also**: [UI-Labs Reference](./ui-labs.md), [Component Patterns](../guides/components.md)
