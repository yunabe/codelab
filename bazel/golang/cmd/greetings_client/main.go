package main

import (
	"context"
	"io"

	"github.com/google/logger"
	_ "github.com/yunabe/codelab/bazel/golang/greetings"
	pb "github.com/yunabe/codelab/bazel/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	logger.Init("hello", true, false, io.Discard)
	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		logger.Fatalf("failed to dial: %v", err)
	}
	defer conn.Close()
	client := pb.NewGreetingsServiceClient(conn)
	ctx := context.Background()
	var in pb.GreetingRequest
	in.Name = "golang"
	res, err := client.Hello(ctx, &in)
	if err != nil {
		logger.Fatalf("failed to invoke Hello: %v", err)
	}
	logger.Infof("res.Message: %v", res.Message)
}
