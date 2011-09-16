include $(GOROOT)/src/Make.inc

all: server client ipc_pb2.py

ipc.pb.go: ipc.proto
	protoc --go_out=. ipc.proto

ipc_pb2.py: ipc.proto
	protoc --python_out=. ipc.proto

server.$(O): server.go ipc.go ipc.pb.go
	$(GC) server.go ipc.go ipc.pb.go

server: server.$(O)
	$(LD) -o server server.$(O)

client.$(O): client.go ipc.go ipc.pb.go
	$(GC) client.go ipc.go ipc.pb.go

client: client.$(O)
	$(LD) -o client client.$(O)

clean:
	rm -f *.$(O) *.pb.go *_pb2.py *.pyc server client
