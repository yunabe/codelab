test: gflags_example_test

gflags_example: gflags_example.o gflags_example_lib.o
	g++ gflags_example.o gflags_example_lib.o -o gflags_example -lgflags

gflags_example.o: gflags_example.cc
	g++ gflags_example.cc -c -o gflags_example.o

gflags_example_lib.o: gflags_example_lib.cc
	g++ gflags_example_lib.cc -c -o gflags_example_lib.o

gflags_example_test: gflags_example_test.py gflags_example
	python gflags_example_test.py

glog_example_lib.o: glog_example_lib.cc
	g++ glog_example_lib.cc -c -o glog_example_lib.o

glog_example.o: glog_example.cc
	g++ glog_example.cc -c -o glog_example.o

glog_example: glog_example.o glog_example_lib.o
	g++ glog_example.o glog_example_lib.o -o glog_example -lglog -lgflags

clean:
	rm -f *.o gflags_example glog_example
