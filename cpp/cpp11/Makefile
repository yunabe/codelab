all: main lambda regex

main: main.cc
	g++ main.cc -std=c++0x -Wall -o main

lambda: lambda.cc
	g++ lambda.cc -std=c++0x -Wall -o lambda

regex: regex.cc
	g++ regex.cc -std=c++0x -Wall -o regex

clean:
	rm -rf main lambda regex
