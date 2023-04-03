load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "hello",
    srcs = ["hello.py"],
    deps = [
        "//proto:greetings_py_grpc",
        "//proto:greetings_py_pb2",
        "//python/utils:greetings",
    ],
)

py_binary(
    name = "greetings_client",
    srcs = ["greetings_client.py"],
    deps = [
        "//proto:greetings_py_grpc",
        "//proto:greetings_py_pb2",
        "//python/utils:greetings",
    ],
)


py_binary(
    name = "greetings_server",
    srcs = ["greetings_server.py"],
    deps = [
        "//proto:greetings_py_grpc",
        "//proto:greetings_py_pb2",
        "//python/utils:greetings",
    ],
)
