# Tips of Node.js

## SIGINT (Ctrl-C)

- By default, `Ctrl-C` terminates the process immediately like Go.
  Any exception (e.g. `KeyboardInterrupt` in Python) is not thrown by `Ctrl-C`.
- You can hook `SIGINT` with `process.on('SIGINT', ...)`. But it does not interrupt a runninng task (e.g. an infinite loop).
