package greetings

import (
	"fmt"

	"github.com/google/logger"
	pb "github.com/yunabe/codelab/bazel/proto"
	prototext "google.golang.org/protobuf/encoding/prototext"
)

func Hello(name string) string {
	var req pb.GreetingRequest
	req.Name = "name"
	b, err := prototext.Marshal(&req)
	if err != nil {
		logger.Fatalf("failed to serialize to text: %v", err)
	}
	return fmt.Sprintf("Hi, %s. Welcome!", string(b))
}
