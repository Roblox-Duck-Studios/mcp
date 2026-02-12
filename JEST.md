Hand written documentation btw
# Roblox Jest
Basically the same as the actual jest v27.4.7 framework.
Install via
`@rbxts/jest@alpha` `@rbxts/jest-globals@alpha`

`https://jsdotlua.github.io/jest-lua/`
For deviations, check here `https://jsdotlua.github.io/jest-lua/deviations`


Other than that, the good practices of unit testing still remain here, where we should have the highest coverage possible and cover every case in the code.

# Unit testing structure
There should be a dedicated folder for unit testing, on the top level of the directory, it should follow this convention shown below. 
```ts
import type { Config } from "@rbxts/jest";
import setupTests from "./setup-tests";

export = {
  displayName: "🟢 SERVER",
  setupFiles: [setupTests],
  testMatch: ["**/*.test"],
} satisfies Config;
````
Please note that there will be `🔵 CLIENT`, `🟢 SERVER`, `🟠 SHARED`. Each file should be named as `.test.ts` to actually run through the unit testing. Those three base configurations should be following the structure of
src
- client
- - `__tests__`
- server
- - `__tests__`
- shared
- - `__tests__`

Make sure to include setupTests module script in `jest.config.ts`, or else the luau execution will include some runtime error that fails all the tests.
```ts
for (const [key] of pairs(_G)) {
  // Clear registered modules to reset the roblox-ts runtime
  if (typeIs(key, "Instance") && key.IsA("ModuleScript")) {
    _G[key as unknown as keyof typeof _G] =
      undefined as unknown as (typeof _G)[keyof typeof _G];
  }
}

export = script as ModuleScript;
````
# Jest Assassin
jestrbx is a CLI tool for running Jest-style tests against Roblox places, wrapping the Roblox Jest runtime and rewriting results for local source paths. It is designed to integrate with roblox-ts and Rojo workflows, providing a familiar Jest experience for Roblox game development.
A project with jestrbx should always have `@rbxts/coverage` library to provide users the opportunity to check for coverage

more documentation here: https://github.com/Unreal-Works/jest-roblox-assassin
