all: basic func oop concurrency websocket protobuf

basic: basic.go
	go build basic.go

func: func.go
	go build func.go

oop: oop.go
	go build oop.go

concurrency: concurrency.go
	go build concurrency.go

websocket: websocket.go
	go build websocket.go

protobuf: protobuf.go example.pb.go
	go build protobuf.go example.pb.go

example.pb.go: example.proto
	protoc --go_out=. example.proto

clean:
	rm -rf *.pb.go basic func oop concurrency websocket protobuf
