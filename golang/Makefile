include $(GOROOT)/src/Make.inc

all: basic func oop concurrency websocket protobuf

basic: basic.$(O)
	$(LD) -o basic basic.$(O)

basic.$(O): basic.go
	$(GC) basic.go

func: func.$(O)
	$(LD) -o func func.$(O)

func.$(O): func.go
	$(GC) func.go

oop: oop.$(O)
	$(LD) -o oop oop.$(O)

oop.$(O): oop.go
	$(GC) oop.go

concurrency: concurrency.$(O)
	$(LD) -o concurrency concurrency.$(O)

concurrency.$(O): concurrency.go
	$(GC) concurrency.go

websocket: websocket.$(O)
	$(LD) -o websocket websocket.$(O)

websocket.$(O): websocket.go
	$(GC) websocket.go

protobuf: protobuf.$(O)
	$(LD) -o protobuf protobuf.$(O)

protobuf.$(O): protobuf.go example_pb.$(O)
	$(GC) protobuf.go

example.pb.go: example.proto
	protoc --go_out=. example.proto

example_pb.$(O): example.pb.go
	$(GC) -o example_pb.$(O) example.pb.go

clean:
	rm -rf *.$(O) *.pb.go basic func oop concurrency websocket protobuf
