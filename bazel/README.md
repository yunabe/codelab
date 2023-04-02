# Bazel

## Tips & Pitfalls

- `sha256` of `http_archive` is a cache key: [Reference](https://github.com/bazelbuild/bazel/issues/10630#issuecomment-577041231)
  - When you update `urls`, don't forget to update `sha256`!
  - The change of `urls` is not reflected if `sha256` is not changed.
  - `bazel` does not notice the inconsistency between `sha256` and the file linked by the `urls`.

# Bazel and Go

Use https://github.com/bazelbuild/rules_go and https://github.com/bazelbuild/bazel-gazelle.

## Tips & Pitfalls

- Access `go` command used in `bazel`
  - Use `$(bazel info output_base)/external/go_sdk/bin/go`: [Reference](https://github.com/bazelbuild/rules_go/issues/2521)
- Don't forget to set `# gazelle:prefix` to `gazelle(name = "gazelle")` rule.
  - As of 2023-04, `gazelle` does not use `go.mod`.
  - Thus, you need to define the module prefix in both `go.mod` and `# gazelle:prefix`.
- Editor support: https://github.com/bazelbuild/rules_go/wiki/Editor-setup
