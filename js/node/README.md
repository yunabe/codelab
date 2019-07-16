# Tips of Node.js

## SIGINT (Ctrl-C)

- By default, `Ctrl-C` terminates the process immediately like Go.
  Any exception (e.g. `KeyboardInterrupt` in Python) is not thrown by `Ctrl-C`.
    - `node ./dist/sigint0.js`
- You can hook `SIGINT` with `process.on('SIGINT', ...)`. But it does not interrupt a runninng task (e.g. an infinite loop).
    - `node ./dist/sigint1.js`
    - `node ./dist/sigint2.js`

# exit of processes

`node ./dist/exit.js`

- *[Normally, the Node.js process will exit when there is no work scheduled](https://nodejs.org/api/process.html#process_event_beforeexit)*
- *'beforeExit' event can make asynchronous calls, and thereby cause the Node.js process to continue.*
- `process.exit` terminates the process immeidately, after calling a handler of `'exit'` event.

## TypeScript

- `isolatedModules`
  - [In TypeScript, just as in ECMAScript 2015, any file containing a top-level import or export is considered a module. ](https://www.typescriptlang.org/docs/handbook/modules.html#introduction)
  - `isolatedModuels` declares that all files amodules must be modules (errors if there is no export or import in a file).
    You need to define `export {}` in the file in that case.

## Misc

- `.vscode/settings.json`
  - In mac, the user config is available on `~/Library/Application Support/Code/User/settings.json`
