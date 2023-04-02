load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
  name = "hello",
  srcs = ["hello.py"],
  deps = [
    "//proto:greetings_py_pb2",
    "//python/utils:greetings",
  ],
)
