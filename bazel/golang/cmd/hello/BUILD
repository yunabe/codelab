load("@io_bazel_rules_go//go:def.bzl", "go_binary", "go_library")

go_library(
    name = "hello_lib",
    srcs = ["hello.go"],
    importpath = "github.com/yunabe/codelab/bazel/golang/cmd/hello",
    visibility = ["//visibility:private"],
    deps = [
        "//golang/greetings",
        "@com_github_google_logger//:logger",
    ],
)

go_binary(
    name = "hello",
    embed = [":hello_lib"],
    visibility = ["//visibility:public"],
)
