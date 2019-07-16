process.on("beforeExit", () => {
  console.log("on beforeExit");
});

process.on("exit", () => {
  console.log("on exit");
});

process.on("SIGINT", () => {
  console.log("Received SIGINT");
});

try {
  console.log("Entering an infinite loop.");
  while (true) {}
} finally {
  console.log("Exited an infinite loop.");
}
