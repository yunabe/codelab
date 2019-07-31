// Test watcher.ts API.
// TODO: Reduce "Check Type" of incremental compile.

import * as ts from "typescript";
import { writeFile } from "fs";

function resetPerformance() {
  (ts as any).performance.enable();
}

const sys = Object.create(ts.sys) as ts.System;
sys.writeFile = function(path, data) {
  console.log("writeFile:", path, data);
  if (lastRead > 0) {
    console.log("took:", Date.now() - lastRead, "[ms]", lastRead);

    reportTimeStatistic();
  }
};

const opts: ts.CompilerOptions = {};

opts["diagnostics"] = true;
opts["extendedDiagnostics"] = true;
opts.declaration = true;
opts.watch = true;

const host = ts.createWatchCompilerHost(
  ["mysrc.ts"],
  opts,
  sys,
  null,
  function(d: ts.Diagnostic) {
    console.log(d.messageText);
  },
  function(d: ts.Diagnostic) {
    console.log(d.messageText);
  }
);

host.setTimeout = function(cb) {
  setTimeout(cb, 0);
};

host.fileExists = path => {
  console.log("fileExists:", path);
  return ts.sys.fileExists(path);
};
let lastRead = 0;
host.readFile = function(path, encoding) {
  console.log("readFile:", path);
  if (path == "mysrc.ts") {
    // writeFile is called only when the content is updated.
    const rand = Math.floor(Math.random() * 1000 * 100);
    lastRead = Date.now();
    return `
const x = ${rand};
let y = x * x;
`;
  }
  return ts.sys.readFile(path, encoding);
};
let mySrcCb: ts.FileWatcherCallback;
host.watchFile = function(path, callback): ts.FileWatcher {
  console.log("watchFile:", path);
  if (path == "mysrc.ts") {
    mySrcCb = callback;
  }
  return {
    close: function() {}
  };
};
const builder = ts.createWatchProgram(host);
console.log("builder is ready!");

setTimeout(() => {
  console.log("notify...");
  resetPerformance();
  mySrcCb("mysrc.ts", ts.FileWatcherEventKind.Changed);
}, 0);

setTimeout(() => {
  console.log("notify...");
  resetPerformance();
  mySrcCb("mysrc.ts", ts.FileWatcherEventKind.Changed);
}, 2000);

function reportTimeStatistic() {
  const performance = (ts as any).performance;

  const programTime = performance.getDuration("Program");
  const bindTime = performance.getDuration("Bind");
  const checkTime = performance.getDuration("Check");
  const emitTime = performance.getDuration("Emit");
  // Individual component times.
  // Note: To match the behavior of previous versions of the compiler, the reported parse time includes
  // I/O read time and processing time for triple-slash references and module imports, and the reported
  // emit time includes I/O write time. We preserve this behavior so we can accurately compare times.
  console.log("I/O read", performance.getDuration("I/O Read"));
  console.log("I/O write", performance.getDuration("I/O Write"));
  console.log("Parse time", programTime);
  console.log("Bind time", bindTime);
  console.log("Check time", checkTime);
  console.log("Emit time", emitTime);
}
