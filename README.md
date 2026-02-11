
Hand written documentation. Do not modify with AI
This documentation covers with @rbxts/react, @rbxts/react-roblox, simple button state, pixels function, ripple, react lifetime, pretty react hooks, ultimate list, ui-labs. Those are standard tools we use in react.

# React Roblox documentation
React roblox is similar to react-js, it is split into `@rbxts/react@alpha` `@rbxts/react-roblox@alpha`. React is the internal logic for react, react roblox is react DOM, but for roblox. Every concept in react is applied to roblox, but with roblox's own rendering system, and some slight deviations. For more, check here https://react.luau.page/api-reference/react/

# Simple example
```tsx
//button.tsx
interface MyButtonProps {
	Disabled?: boolean;
	OnClick?: () => void;
	Text: string;
}

export function MyButton({
	Disabled = false,
	OnClick,
	Text,
}: Readonly<MyButtonProps>): React.ReactElement {
	return <textbutton AutoButtonColor={!Disabled} Event={{ Activated: OnClick }} Text={Text} />;
}

<MyButton Text="hello" />;
```
Key notes:
* use PascalCase convention for properties
* use arrow functions component interface definitions
* export as a normal function, never **export default**
* Apply `Readonly` and have return type as `React.ReactElement`
* Components should only be one file

# Writing a React Story
We use the `@rbxts/ui-labs` library to render and visualize stories, every component you create, compose should have a corresponding story to visualize it, create it with component properties
```ts
//button.story.tsx
import React, { StrictMode } from "@rbxts/react";
import ReactRoblox from "@rbxts/react-roblox";
import { CreateReactStory } from "@rbxts/ui-labs";
import { Button } from "./button";
import { RootProvider } from "./root-provider";

export = CreateReactStory({ react: React, reactRoblox: ReactRoblox }, () => {

	return (
		<StrictMode>
			<RootProvider>
				<Button />
			</RootProvider>
		</StrictMode>
	);
});
```
Notes:
* Wrap the top layer with strict mode
* Projects usually have a root provider, wrap the logic around with a root provider
* Finally its the button in there
Check out
for AI to reference, 
`https://ui-labs.luau.page/docs/controls/adding` check this link out for referencing controls

# Px
Usually projects have some sort of implementation of `px` function and a corresponding `usePx`. They allow you to effectively utilize the offset parameter to make things rational and scales of depending on size. Some projects use `@rbxts/ui-scaler` to call the px, others just create it themselves.

Example

```tsx
import type { ReactNode } from "@rbxts/react";
import React from "@rbxts/react";

import { usePx } from "common/client/ui/hooks/use-px";

export function DetailsView(): ReactNode {
	const px = usePx();

	return (
		<>
			<imagelabel Size={new UDim2(1, px(-450), 1, 0)} />
			<frame
				AnchorPoint={new Vector2(1)}
				Position={UDim2.fromScale(1)}
				Size={new UDim2(0, px(400), 1, 0)}
			/>
		</>
	);
}
```
Notes: 
* usePx() uses the pixels depending on the configuration of the screen size, it computes the values based on the value you provide, and you should only use it for the offset parameter for the function call. 
* https://create.roblox.com/docs/ui/position-and-size this documentation explains well between ui position and ui size. You can read anything in  
* https://create.roblox.com/docs/ui explains well for roblox's ui design.

# Ripple, animation library
`@rbxts/ripple`
Ripple is like react-spring but more flexible, it exposes a useMotion, useSpring, useTween. Reference the api in https://github.com/littensy/ripple

```tsx
interface AnimatedLineProps extends PropsWithChildren {
  Active: boolean;
  ActiveColor: Color3;
  AnchorPoint?: Vector2;
  disableColor: Color3;
  Position?: UDim2;
  Size: UDim2;
  Transparency?: BindingOrValue<number>;
}

export function AnimatedLine({
  Active,
  ActiveColor,
  AnchorPoint,
  children,
  disableColor,
  Position,
  Size,
  Transparency,
}: Readonly<AnimatedLineProps>): ReactNode {
  const [frameSize, frameSizeMotion] = useMotion<UDim2>(new UDim2(new UDim(), Size.Y));
  const [frameColor, frameColorMotion] = useMotion<Color3>(COLORS.Base.Base3);

  useEffect(() => {
    if (Active) {
      frameSizeMotion.spring(Size);
      frameColorMotion.spring(ActiveColor);
    } else {
      frameSizeMotion.spring(new UDim2(0, 0, Size.Y.Scale, Size.Y.Offset));
      frameColorMotion.spring(disableColor);
    }
  }, [Active, ActiveColor, disableColor, frameColorMotion, frameSizeMotion, Size]);

  return (
    <frame
      AnchorPoint={AnchorPoint}
      BackgroundColor3={frameColor}
      BorderSizePixel={0}
      Position={Position}
      Size={frameSize}
      Transparency={Transparency}
    >
      {children}
    </frame>
  );
}
```
The useMotion is used within the component, everything is self explanatory

# Pretty react hooks
Pretty react hooks provide lots of utility hooks. Check more in the documentation here: https://github.com/littensy/pretty-react-hooks/tree/master/src

# React lifetime
in `@rbxts/react-lifetime` reference this link for further information on how to use it https://raw.githubusercontent.com/PepeElToro41/react-lifetime-component/refs/heads/main/README.md

# Ultimate List
UltimateList is a library for creating fast and efficient virtualized lists in Roblox. A virtualized list is a scrolling frame that only creates elements for items that can actually be seen. This puts less work on the engine, defers running code in React components until they can be seen (as well as cleaning up when they're not), and in some cases can do this while also performing zero React re-renders as a user interacts with the list.
Further documentation here: `https://kampfkarren.github.io/ultimate-list/`
