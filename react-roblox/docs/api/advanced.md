# Advanced React Features

Advanced patterns and APIs for experienced React developers.

## React.lazy and Code Splitting

Lazily load components to improve performance:

```lua
local HeavyComponent = React.lazy(function()
    return require(script.Parent.HeavyComponent)
end)

-- Use within Suspense boundary
React.createElement(React.Suspense, {
    fallback = React.createElement("TextLabel", { Text = "Loading..." })
},
    React.createElement(HeavyComponent, {})
)
```

**Note**: React.lazy may have limited utility in Roblox since modules are already loaded quickly. Use if you have measurable performance issues.

## React.createMutableSource and useMutableSource

For integrating external mutable data sources (advanced):

```lua
local mutableSource = React.createMutableSource(
    dataStore,
    function(a, b) return a.version == b.version end
)

local function Component()
    local snapshot = React.useMutableSource(
        mutableSource,
        function(source) return source:getSnapshot() end,
        function(source, callback) return source:subscribe(callback) end
    )
    
    return React.createElement("TextLabel", {
        Text = snapshot.data
    })
end
```

## Ref Forwarding with useImperativeHandle

Create custom ref interfaces:

```lua
local TextInputWithButton = React.forwardRef(function(props, ref)
    local inputRef = React.useRef(nil)
    
    React.useImperativeHandle(ref, function()
        return {
            focus = function()
                inputRef.current:CaptureFocus()
            end,
            clear = function()
                inputRef.current.Text = ""
            end,
            getValue = function()
                return inputRef.current.Text
            end
        }
    end, {})
    
    return React.createElement("TextBox", {
        ref = inputRef,
        Size = UDim2.fromOffset(200, 30)
    })
end)

-- Usage
local function Form()
    local inputRef = React.useRef(nil)
    
    return React.createElement("Frame", {},
        React.createElement(TextInputWithButton, {
            ref = inputRef
        }),
        React.createElement("TextButton", {
            Text = "Get Value",
            [React.Event.Activated] = function()
                print(inputRef.current.getValue())
            end
        })
    )
end
```

## Binding and useBinding

Roblox-specific: Create reactive bindings for property changes:

```lua
local function useBinding(initialValue)
    local binding, setBinding = React.createBinding(initialValue)
    
    return {
        binding = binding,
        setBinding = setBinding
    }
end

local function AnimatedFrame()
    local size = React.createBinding(UDim2.fromOffset(100, 100))
    
    React.useEffect(function()
        local TweenService = game:GetService("TweenService")
        
        -- Animate size
        local tween = TweenService:Create(
            size,
            TweenInfo.new(1),
            { X = UDim2.fromOffset(200, 200) }
        )
        tween:Play()
        
        return function()
            tween:Cancel()
        end
    end, {})
    
    return React.createElement("Frame", {
        Size = size
    })
end
```

## Error Boundaries

Handle errors gracefully in component trees (limited support):

```lua
local ErrorBoundary = React.Component:extend("ErrorBoundary")

function ErrorBoundary:init()
    self:setState({ hasError = false, error = nil })
end

function ErrorBoundary:render()
    if self.state.hasError then
        return React.createElement("TextLabel", {
            Text = "Error: " .. tostring(self.state.error),
            TextColor3 = Color3.new(1, 0, 0)
        })
    end
    
    return self.props.children
end

-- Note: Error boundaries have limited support in React-Lua
-- Use try-catch as fallback
```

## Compound Components Pattern

Components that manage state together:

```lua
-- Tabs.tsx
local Tabs = React.Component:extend("Tabs")

function Tabs:init()
    self:setState({ activeTab = 1 })
end

function Tabs:render()
    return React.createElement("Frame", {
        Size = UDim2.fromScale(1, 1)
    },
        -- Render tabs header
        React.createElement("Frame", {
            Size = UDim2.fromScale(1, 0.1)
        },
            React.Children.map(self.props.children, function(child, index)
                return React.cloneElement(child, {
                    isActive = self.state.activeTab == index,
                    onClick = function()
                        self:setState({ activeTab = index })
                    end
                })
            end)
        ),
        -- Render active tab content
        React.Children.toArray(self.props.children)[self.state.activeTab]
    )
end

-- TabItem.tsx
local function TabItem(props)
    return React.createElement("TextButton", {
        Text = props.label,
        BackgroundColor3 = if props.isActive then Color3.new(0, 0, 1) else Color3.new(1, 1, 1),
        [React.Event.Activated] = props.onClick
    })
end

-- Usage
React.createElement(Tabs, {},
    React.createElement(TabItem, { label = "Tab 1" }),
    React.createElement(TabItem, { label = "Tab 2" }),
    React.createElement(TabItem, { label = "Tab 3" })
)
```

## Integrating with External State

Connect React to external Roblox systems:

```lua
local RunService = game:GetService("RunService")

local function useHeartbeat()
    local deltaTime, setDeltaTime = React.useState(0)
    
    React.useEffect(function()
        local connection = RunService.Heartbeat:Connect(function(dt)
            setDeltaTime(dt)
        end)
        
        return function()
            connection:Disconnect()
        end
    end, {})
    
    return deltaTime
end

-- Usage
local function GameLoopComponent()
    local dt = useHeartbeat()
    local elapsed, setElapsed = React.useState(0)
    
    React.useEffect(function()
        setElapsed(elapsed + dt)
    end, { dt })
    
    return React.createElement("TextLabel", {
        Text = string.format("Elapsed: %.2f", elapsed)
    })
end
```

## Dynamic Component Selection

Render different components based on type:

```lua
local componentMap = {
    button = require(script.Button),
    input = require(script.Input),
    card = require(script.Card)
}

local function DynamicComponent(props)
    local Component = componentMap[props.type]
    
    if not Component then
        return React.createElement("TextLabel", {
            Text = "Unknown component type: " .. props.type
        })
    end
    
    return React.createElement(Component, props)
end

-- Usage
React.createElement(DynamicComponent, {
    type = "button",
    label = "Click me"
})
```

## Performance Profiling

Identify performance bottlenecks:

```lua
local function useRenderCount()
    local count, setCount = React.useState(0)
    
    React.useEffect(function()
        setCount(count + 1)
        print("Rendered", count, "times")
    end)
    
    return count
end

local function ProfiledComponent()
    local renderCount = useRenderCount()
    
    return React.createElement("TextLabel", {
        Text = "Render count: " .. tostring(renderCount)
    })
end
```

## Debugging Tips

1. **React DevTools** - Inspect component tree (if available)
2. **Console logging** - Add print statements strategically
3. **Performance monitoring** - Track render counts
4. **Error tracking** - Wrap components in error handlers
5. **Props validation** - Check prop types in development

## Best Practices for Advanced Usage

1. **Keep it simple** - Don't over-engineer solutions
2. **Profile first** - Measure performance before optimizing
3. **Use standard patterns** - Stick to documented React patterns
4. **Test thoroughly** - Advanced features need careful testing
5. **Document complex logic** - Help future maintainers understand
6. **Avoid premature optimization** - Fix real problems, not theoretical ones

---

**See also**: [Core API](../api/core.md), [Hooks API](../api/hooks.md)
