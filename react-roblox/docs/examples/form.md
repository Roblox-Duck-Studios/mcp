# Example: Form with Validation

A more complex example showing form handling and validation.

## Code

```lua
-- src/hooks/useFormInput.ts
import React, { useState } from "@react-lua/react"

local function useFormInput(initialValue)
    local value, setValue = React.useState(initialValue or "")
    local error, setError = React.useState(nil)
    
    return {
        value = value,
        error = error,
        onChange = function(newValue)
            setValue(newValue)
            setError(nil)  -- Clear error when user types
        end,
        setError = setError,
        reset = function()
            setValue(initialValue or "")
            setError(nil)
        end
    }
end

return useFormInput
```

```lua
-- src/utils/validation.ts
local function validateEmail(email)
    if not email or #email == 0 then
        return "Email is required"
    end
    if not string.find(email, "@") then
        return "Email must be valid"
    end
    return nil
end

local function validatePassword(password)
    if not password or #password == 0 then
        return "Password is required"
    end
    if #password < 8 then
        return "Password must be at least 8 characters"
    end
    return nil
end

local function validateName(name)
    if not name or #name == 0 then
        return "Name is required"
    end
    if #name < 2 then
        return "Name must be at least 2 characters"
    end
    return nil
end

return {
    validateEmail = validateEmail,
    validatePassword = validatePassword,
    validateName = validateName
}
```

```lua
-- src/components/Form/FormInput.tsx
import React from "@react-lua/react"

local function FormInput(props: {
    label: string,
    placeholder: string,
    value: string,
    error: string?,
    onChange: (string) -> nil,
    multiline: boolean?
})
    local isError = props.error ~= nil
    local borderColor = isError and Color3.fromRGB(231, 76, 60) or Color3.fromRGB(200, 200, 200)
    
    return React.createElement("Frame", {
        Size = UDim2.fromScale(1, if props.multiline then 0.25 else 0.15),
        BackgroundTransparency = 1,
        AutomaticSize = Enum.AutomaticSize.None
    },
        React.createElement("TextLabel", {
            Text = props.label,
            Size = UDim2.fromScale(1, 0.3),
            BackgroundTransparency = 1,
            TextSize = 14,
            Font = Enum.Font.GothamSemibold,
            TextXAlignment = Enum.TextXAlignment.Left,
            TextColor3 = Color3.new(0, 0, 0)
        }),
        React.createElement("TextBox", {
            Text = props.value,
            PlaceholderText = props.placeholder,
            Size = UDim2.fromScale(1, if props.multiline then 0.6 else 0.4),
            Position = UDim2.fromScale(0, 0.3),
            BackgroundColor3 = Color3.new(1, 1, 1),
            BorderColor3 = borderColor,
            BorderSizePixel = 1,
            TextSize = 14,
            Font = Enum.Font.Gotham,
            [React.Event.FocusLost] = function(rbx)
                props.onChange(rbx.Text)
            end
        }),
        if props.error then React.createElement("TextLabel", {
            Text = props.error,
            Size = UDim2.fromScale(1, 0.3),
            Position = UDim2.fromScale(0, if props.multiline then 0.9 else 0.7),
            BackgroundTransparency = 1,
            TextSize = 12,
            Font = Enum.Font.Gotham,
            TextXAlignment = Enum.TextXAlignment.Left,
            TextColor3 = Color3.fromRGB(231, 76, 60)
        }) else nil
    )
end

return FormInput
```

```lua
-- src/components/Form/SignUpForm.tsx
import React, { useState } from "@react-lua/react"
import useFormInput from "../../hooks/useFormInput"
import { validateEmail, validatePassword, validateName } from "../../utils/validation"
import FormInput from "./FormInput"

local function SignUpForm(props: { onSuccess: ((table) -> nil)? })
    local name = useFormInput("")
    local email = useFormInput("")
    local password = useFormInput("")
    local isSubmitting, setIsSubmitting = React.useState(false)
    local submitError, setSubmitError = React.useState(nil)
    
    local function validate()
        local nameError = validateName(name.value)
        local emailError = validateEmail(email.value)
        local passwordError = validatePassword(password.value)
        
        if nameError then name.setError(nameError) end
        if emailError then email.setError(emailError) end
        if passwordError then password.setError(passwordError) end
        
        return not (nameError or emailError or passwordError)
    end
    
    local function handleSubmit()
        setSubmitError(nil)
        
        if not validate() then
            return
        end
        
        setIsSubmitting(true)
        
        -- Simulate submission
        task.wait(1)
        
        local userData = {
            name = name.value,
            email = email.value
        }
        
        if props.onSuccess then
            props.onSuccess(userData)
        end
        
        name.reset()
        email.reset()
        password.reset()
        setIsSubmitting(false)
    end
    
    return React.createElement("Frame", {
        Size = UDim2.fromOffset(400, 500),
        BackgroundColor3 = Color3.new(1, 1, 1),
        BorderMode = Enum.BorderMode.Outline
    },
        React.createElement("TextLabel", {
            Text = "Create Account",
            Size = UDim2.fromScale(1, 0.1),
            BackgroundTransparency = 1,
            TextSize = 24,
            Font = Enum.Font.GothamBold
        }),
        React.createElement("ScrollingFrame", {
            Size = UDim2.new(1, -20, 0.8, -20),
            Position = UDim2.fromOffset(10, 50),
            CanvasSize = UDim2.fromScale(1, 0),
            ScrollBarThickness = 4,
            BackgroundTransparency = 1
        },
            React.createElement("UIListLayout", {
                Padding = UDim.new(0, 15),
                HorizontalAlignment = Enum.HorizontalAlignment.Left,
                SortOrder = Enum.SortOrder.LayoutOrder
            }),
            React.createElement(FormInput, {
                label = "Full Name",
                placeholder = "John Doe",
                value = name.value,
                error = name.error,
                onChange = name.onChange,
                LayoutOrder = 1
            }),
            React.createElement(FormInput, {
                label = "Email",
                placeholder = "john@example.com",
                value = email.value,
                error = email.error,
                onChange = email.onChange,
                LayoutOrder = 2
            }),
            React.createElement(FormInput, {
                label = "Password",
                placeholder = "At least 8 characters",
                value = password.value,
                error = password.error,
                onChange = password.onChange,
                LayoutOrder = 3
            }),
            if submitError then React.createElement("TextLabel", {
                Text = submitError,
                Size = UDim2.fromScale(1, 0.05),
                BackgroundColor3 = Color3.fromRGB(255, 240, 245),
                TextColor3 = Color3.fromRGB(231, 76, 60),
                TextSize = 12,
                Font = Enum.Font.Gotham,
                TextWrapped = true,
                LayoutOrder = 4
            }) else nil
        ),
        React.createElement("TextButton", {
            Text = if isSubmitting then "Creating..." else "Create Account",
            Size = UDim2.fromScale(0.9, 0.08),
            Position = UDim2.fromScale(0.05, 0.9),
            BackgroundColor3 = Color3.fromRGB(59, 89, 152),
            TextColor3 = Color3.new(1, 1, 1),
            Font = Enum.Font.GothamBold,
            TextSize = 16,
            [React.Event.Activated] = if not isSubmitting then function()
                handleSubmit()
            end else nil
        })
    )
end

return SignUpForm
```

## Key Concepts

1. **Custom Hooks** - `useFormInput` for reusable form state
2. **Validation** - Utility functions for input validation
3. **Error Handling** - Display validation errors to user
4. **Component Composition** - `FormInput` component reused for multiple fields
5. **Form State** - Managing multiple input values
6. **User Feedback** - Loading states and error messages
7. **Event Handling** - FocusLost event for input changes

## Features

- Name, email, and password validation
- Real-time error clearing when user types
- Form submission handling
- Loading state during submission
- Error message display
- Reset form after successful submission

## Extension Ideas

1. **Password strength indicator** - Show password quality
2. **Confirmation password** - Add password confirmation field
3. **Agree to terms** - Add checkbox for terms acceptance
4. **Submit to server** - Actually send data to a server
5. **Success message** - Show confirmation after submission
6. **Disable button on invalid** - Only enable when all fields valid

---

**See also**: [Counter Example](./counter.md), [Component Patterns](../guides/components.md)
