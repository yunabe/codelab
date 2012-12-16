all: server client max_num_connection

server: server.cc shared.o
	g++ -o server server.cc shared.o

client: client.cc shared.o
	g++ -o client client.cc shared.o

shared: shared.cc shared.h
	g++ -o shared.o shared.cc

max_num_connection: max_num_connection.cc
	g++ max_num_connection.cc -o max_num_connection

clean:
	rm -rf server client *.o
