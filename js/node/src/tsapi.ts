// Played with https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API#customizing-module-resolution

import * as ts from "typescript";
import * as path from "path";

function createCompilerHost(): ts.CompilerHost {
  return {
    getSourceFile,
    getDefaultLibFileName: () => "lib.d.ts",
    writeFile: (fileName, content) => {
      console.log(`Write to ${fileName}:
${content}`);
    },
    getCurrentDirectory: () => ts.sys.getCurrentDirectory(),
    getDirectories: path => ts.sys.getDirectories(path),
    getCanonicalFileName: fileName =>
      ts.sys.useCaseSensitiveFileNames ? fileName : fileName.toLowerCase(),
    getNewLine: () => ts.sys.newLine,
    useCaseSensitiveFileNames: () => ts.sys.useCaseSensitiveFileNames,
    fileExists,
    readFile,
    resolveModuleNames
  };

  function fileExists(fileName: string): boolean {
    return ts.sys.fileExists(fileName);
  }

  function readFile(fileName: string): string | undefined {
    throw new Error(`readFile is not implemented: ${fileName}`);
  }

  function getSourceFile(
    fileName: string,
    languageVersion: ts.ScriptTarget,
    onError?: (message: string) => void
  ) {
    console.log(`getSourceFile(${fileName})`);
    if (fileName.startsWith("lib.")) {
      return ts.createSourceFile(
        fileName,
        ts.sys.readFile(path.join("./node_modules/typescript/lib", fileName)),
        languageVersion
      );
    }
    return ts.createSourceFile(
      fileName,
      `const x: string= 10;`,
      languageVersion
    );
  }

  function resolveModuleNames(
    moduleNames: string[],
    containingFile: string
  ): ts.ResolvedModule[] {
    throw new Error(`resolveModuleNames is not implemented: ${moduleNames}`);
  }
}

function main() {
  const options: ts.CompilerOptions = {
    module: ts.ModuleKind.AMD,
    target: ts.ScriptTarget.ES5
  };
  const host = createCompilerHost();
  const program = ts.createProgram(["mylib.ts"], options, host);
  console.log(program.getGlobalDiagnostics());
  console.log(program.getSemanticDiagnostics());
  console.log(program.getSyntacticDiagnostics());
}

main();
