load("@rules_proto//proto:defs.bzl", "proto_library")
load("@io_bazel_rules_go//go:def.bzl", "go_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
# load("@rules_python//python:proto.bzl", "py_proto_library")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_grpc_library", "py_proto_library")

proto_library(
    name = "greetings_proto",
    srcs = ["greetings.proto"],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "greetings_go_proto",
    compilers = ["@io_bazel_rules_go//proto:go_grpc"],
    importpath = "github.com/yunabe/codelab/bazel/proto",
    proto = ":greetings_proto",
    visibility = ["//visibility:public"],
)

go_library(
    name = "proto",
    embed = [":greetings_go_proto"],
    importpath = "github.com/yunabe/codelab/bazel/proto",
    visibility = ["//visibility:public"],
)

py_proto_library(
    name = "greetings_py_pb2",
    visibility = ["//visibility:public"],
    deps = [":greetings_proto"],
)

py_grpc_library(
    name = "greetings_py_grpc",
    srcs = [":greetings_proto"],
    deps = [":greetings_py_pb2"],
    visibility = ["//visibility:public"],
)
