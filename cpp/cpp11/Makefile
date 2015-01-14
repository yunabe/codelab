all: main lambda regex thread

main: main.cc
	g++ main.cc -std=c++0x -Wall -o main

lambda: lambda.cc
	g++ lambda.cc -std=c++0x -Wall -o lambda

regex: regex.cc
	g++ regex.cc -std=c++0x -Wall -o regex

thread: thread.cc
	g++ thread.cc -std=c++0x -Wall -pthread -o thread

clean:
	rm -rf main lambda regex thread
