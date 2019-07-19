import * as ts from "typescript";
import * as fs from "fs";
import * as path from "path";
import * as glob from "glob";

function findNodeTypes(): string[] {
  function findNodeModules(): string | null {
    let dir = __dirname;
    while (true) {
      const nm = path.join(dir, "node_modules");
      if (fs.existsSync(nm)) {
        return nm;
      }
      const parent = path.dirname(dir);
      if (parent === dir) {
        break;
      }
      dir = parent;
    }
    return null;
  }

  const nodeModules = findNodeModules();
  if (!nodeModules) {
    return [];
  }
  return glob.sync(path.join(nodeModules, "@types/node/**/*.d.ts"));
}

const files = findNodeTypes();

function createLanguageServiceHost(): ts.LanguageServiceHost {
  return {
    getScriptFileNames,
    getScriptVersion,
    getScriptSnapshot,
    getCurrentDirectory,
    getCompilationSettings,
    getDefaultLibFileName,
    fileExists,
    readFile,
    readDirectory
  };

  function getScriptFileNames() {
    console.log("getScriptFileNames...");
    return files;
  }
  function getScriptVersion() {
    console.log("getScriptVersion...");
    return "1.2.3";
  }
  function getScriptSnapshot(fileName: string) {
    console.log("getScriptSnapshot", fileName);
    if (fileName.endsWith(".d.ts")) {
      return ts.ScriptSnapshot.fromString(fs.readFileSync(fileName).toString());
    }
    return ts.ScriptSnapshot.fromString(`
      import * as fs from "fs";
      fs.exists;
      const x: number = 10;
      `);
  }
  function getCurrentDirectory() {
    const cwd = process.cwd();
    console.log("getCurrentDirectory", cwd);
    return cwd;
  }
  function getCompilationSettings(): ts.CompilerOptions {
    console.log("getCompilationSettings...");
    return {};
  }
  function getDefaultLibFileName(options: ts.CompilerOptions): string {
    console.log("getDefaultLibFileName...");
    return ts.getDefaultLibFilePath(options);
  }
  function fileExists(path: string) {
    let exist = ts.sys.fileExists(path);
    console.log("fileExists: ", path, exist);
    return exist;
  }
  function readFile(path: string, encoding?: string): string {
    console.log("readFile:", path);
    return ts.sys.readFile(path, encoding);
  }
  function readDirectory(
    path: string,
    extensions?: ReadonlyArray<string>,
    exclude?: ReadonlyArray<string>,
    include?: ReadonlyArray<string>,
    depth?: number
  ): string[] {
    console.log("readDirectory:", path);
    return ts.sys.readDirectory(path, extensions, exclude, include, depth);
  }
}

const servicesHost = createLanguageServiceHost();

const services = ts.createLanguageService(
  servicesHost,
  ts.createDocumentRegistry()
);

files.push("foo.ts");
let output = services.getEmitOutput("foo.ts");
console.log("output.emitSkipped:", output.emitSkipped);
console.log(
  services
    .getCompilerOptionsDiagnostics()
    .concat(
      services
        .getSyntacticDiagnostics("foo.ts")
        .concat(services.getSemanticDiagnostics("foo.ts"))
    )
);
console.log("*************");

if (!output.emitSkipped) {
  for (let f of output.outputFiles) {
    console.log(`==== ${f.name} ===
${f.text}`);
  }
}

/*
files.push("bar.ts");
services.getEmitOutput("bar.ts");
console.log("--------------");
*/
