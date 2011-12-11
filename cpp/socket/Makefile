all: server client

server: server.cc shared.o
	g++ -o server server.cc shared.o

client: client.cc shared.o
	g++ -o client client.cc shared.o

shared: shared.cc shared.h
	g++ -o shared.o shared.cc

clean:
	rm -rf server client *.o
