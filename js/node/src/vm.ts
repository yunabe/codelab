import * as vm from "vm";

const sandbox = {};
vm.createContext(sandbox);
// Top level var is a global variable.
vm.runInContext(`var x = 10;`, sandbox);
vm.runInContext(`var x = 3 * 4;`, sandbox);
try {
  vm.runInContext(`let x = 3`, sandbox);
} catch (e) {
  // Identifier 'x' has already been declared
  console.error("error:", e);
}
vm.runInContext(`let y = 20;`, sandbox);
vm.runInContext(`var z = y * y;`, sandbox);
// y is not visible in sandbox.
console.log("sandbox:", sandbox);
