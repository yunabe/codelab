load("@io_bazel_rules_go//go:def.bzl", "go_library")

go_library(
    name = "greetings",
    srcs = ["greetings.go"],
    importpath = "github.com/yunabe/codelab/bazel/golang/greetings",
    visibility = ["//visibility:public"],
    deps = [
        "//proto",
        "@com_github_google_logger//:logger",
        "@org_golang_google_protobuf//encoding/prototext:go_default_library",
    ],
)
