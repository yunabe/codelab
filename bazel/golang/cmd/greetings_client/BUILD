load("@io_bazel_rules_go//go:def.bzl", "go_binary", "go_library")

go_library(
    name = "greetings_client_lib",
    srcs = ["main.go"],
    importpath = "github.com/yunabe/codelab/bazel/golang/cmd/greetings_client",
    visibility = ["//visibility:private"],
    deps = [
        "//golang/greetings",
        "//proto",
        "@com_github_google_logger//:logger",
        "@org_golang_google_grpc//:go_default_library",
        "@org_golang_google_grpc//credentials/insecure:go_default_library",
    ],
)

go_binary(
    name = "greetings_client",
    embed = [":greetings_client_lib"],
    visibility = ["//visibility:public"],
)
