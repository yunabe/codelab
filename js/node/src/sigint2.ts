export {};

process.on("beforeExit", () => {
  console.log("on beforeExit");
});

process.on("exit", () => {
  console.log("on exit");
});

let done = false;

process.on("SIGINT", () => {
  console.log("Received SIGINT");
  done = true;
});

(async () => {
  try {
    console.log("Entering an async infinite loop.");
    while (!done) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  } finally {
    console.log("Exited an async infinite loop.");
  }
})();
