import { SSL_OP_EPHEMERAL_RSA } from "constants";

export {};

let counter = 0;
let forceExit = false;

process.on("beforeExit", () => {
  console.log("on beforeExit:", counter);
  counter++;
  if (counter < 60) {
    setTimeout(() => {}, 1000);
  }
});

process.on("exit", () => {
  console.log("on exit");
});

process.on("SIGINT", () => {
  if (forceExit) {
    console.log("Received SIGINT twice. Exiting.");
    process.exit(1);
  } else {
    console.log("Received SIGINT. Press C-c again to force exit.");
    forceExit = true;
  }
});
