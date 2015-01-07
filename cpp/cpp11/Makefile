all: main lambda

main: main.cc
	g++ main.cc -std=c++0x -o main

lambda: lambda.cc
	g++ lambda.cc -std=c++0x -o lambda

clean:
	rm -rf main lambda
