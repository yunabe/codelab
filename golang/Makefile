all: basic func oop concurrency websocket protobuf

basic: basic.8
	8l -o basic basic.8

basic.8: basic.go
	8g basic.go

func: func.8
	8l -o func func.8

func.8: func.go
	8g func.go

oop: oop.8
	8l -o oop oop.8

oop.8: oop.go
	8g oop.go

concurrency: concurrency.8
	8l -o concurrency concurrency.8

concurrency.8: concurrency.go
	8g concurrency.go

websocket: websocket.8
	8l -o websocket websocket.8

websocket.8: websocket.go
	8g websocket.go

protobuf: protobuf.8
	8l -o protobuf protobuf.8

protobuf.8: protobuf.go example_pb.8
	8g protobuf.go

example.pb.go: example.proto
	protoc --go_out=. example.proto

example_pb.8: example.pb.go
	8g -o example_pb.8 example.pb.go

clean:
	rm -rf *.8 *.pb.go basic func oop concurrency websocket protobuf
