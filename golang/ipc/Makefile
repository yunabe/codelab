include $(GOROOT)/src/Make.inc

all: server ipc_pb2.py

ipc.pb.go: ipc.proto
	protoc --go_out=. ipc.proto

ipc_pb2.py: ipc.proto
	protoc --python_out=. ipc.proto

server.$(O): server.go ipc.pb.go
	$(GC) server.go ipc.pb.go

server: server.$(O)
	$(LD) -o server server.$(O)

clean:
	rm -f *.$(O) *.pb.go *_pb2.py *.pyc server
