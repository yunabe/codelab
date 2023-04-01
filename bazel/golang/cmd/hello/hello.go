package main

import (
	"io"

	"github.com/google/logger"
	"github.com/yunabe/codelab/bazel/golang/greetings"
)

func main() {
	logger.Init("hello", true, false, io.Discard)
	logger.Infoln(greetings.Hello("world"))
}
