test: gflags_example_test

gflags_example: gflags_example.o gflags_example_lib.o
	g++ gflags_example.o gflags_example_lib.o -o gflags_example -lgflags

gflags_example.o: gflags_example.cc
	g++ gflags_example.cc -c -o gflags_example.o

gflags_example_lib.o: gflags_example_lib.cc
	g++ gflags_example_lib.cc -c -o gflags_example_lib.o

gflags_example_test: gflags_example_test.py gflags_example
	python gflags_example_test.py

clean:
	rm -f *.o gflags_example
