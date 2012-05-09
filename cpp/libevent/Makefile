all: buffer signalfd

buffer: buffer.cc
	g++ -o buffer buffer.cc -levent

signalfd: signalfd.cc
	g++ -o signalfd signalfd.cc -levent

clean:
	rm -rf buffer signalfd
