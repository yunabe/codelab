# Bazel

## Tips & Pitfalls

- `sha256` of `http_archive` is a cache key: [Reference](https://github.com/bazelbuild/bazel/issues/10630#issuecomment-577041231)
  - When you update `urls`, don't forget to update `sha256`!
  - The change of `urls` is not reflected if `sha256` is not changed.
  - `bazel` does not notice the inconsistency between `sha256` and the file linked by the `urls`.

# Bazel and Go

Use https://github.com/bazelbuild/rules_go and https://github.com/bazelbuild/bazel-gazelle.

## gazelle

- [Gazelle directives](https://github.com/bazelbuild/bazel-gazelle#directives)
  - Use `# gazelle:proto mode` to control the behavior of `gazelle` for `.proto` files.
  - Use [`go_package`](https://protobuf.dev/getting-started/gotutorial/#protocol-format) to change the package name.

## Tips & Pitfalls

- Access `go` command used in `bazel`
  - Use `$(bazel info output_base)/external/go_sdk/bin/go`: [Reference](https://github.com/bazelbuild/rules_go/issues/2521)
- Don't forget to set `# gazelle:prefix` to `gazelle(name = "gazelle")` rule.
  - As of 2023-04, `gazelle` does not use `go.mod`.
  - Thus, you need to define the module prefix in both `go.mod` and `# gazelle:prefix`.
- Editor support: https://github.com/bazelbuild/rules_go/wiki/Editor-setup
- It's not trivial to use `go.mod` with `bazel` if `bazel` autogenerates `.go` files, which is the main reason to use `bazel`.
- Generated `.pb.go` files are in `./bazel-bin/proto/...`. Run `find bazel-bin -follow -name '*.pb.go'` to find `.pb.go` files.
- go_rules_dependencies
  - [doc](https://github.com/bazelbuild/rules_go/blob/master/go/dependencies.rst#go_rules_dependencies)
  - [Overriding dependencies](https://github.com/bazelbuild/rules_go/blob/master/go/dependencies.rst#overriding-dependencies)
  - *Some of the dependencies declared by go_rules_dependencies require additional patches*

# Python and Bazel

## gazelle

- https://github.com/bazelbuild/rules_python/tree/main/gazelle

## Tips & Pitfalls

- We need to add `@py_rules` before `@proto_rules` in `WORKPLACE`.
- The python files used in `py_binary` is is a path like `bazel-out/k8-fastbuild/bin/python/cmd/hello.runfiles/__main__`.
  - We can check the path by printing `sys.path`.
  - `py_library` implicitly creates `__init__.py` to ancestor directories. Thus, we
    can import python modules with the absolute path from the workspace root.

# gRPC

- (option1) https://github.com/grpc/grpc
  - **Important**: It has a custom `.bazelrc`
  - We need to set `-std=c++14` with `--cxxopt` and `--host_cxxopt`.
  - See [this issue too](https://github.com/bazelbuild/bazel/issues/16371#issuecomment-1347826838).
  - Example usages
    - [Minimal example of a python grpc server built with bazel](https://gist.github.com/ivankra/04f11961f7953549a45a82fc13ef3866)
- (option2) https://rules-proto-grpc.com/en/latest/index.html
  - I did not try this.
