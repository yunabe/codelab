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

example.pb.cc example.pb.h: example.proto
	protoc example.proto --cpp_out=.

example.pb.o: example.pb.cc example.pb.h
	g++ example.pb.cc -c -o example.pb.o

protobuf_example.o: protobuf_example.cc example.pb.h
	g++ protobuf_example.cc -c -o protobuf_example.o

# -lpthread is required to link protobuf library.
protobuf_example: protobuf_example.o example.pb.o
	g++ protobuf_example.o example.pb.o -o protobuf_example -lprotobuf -lpthread

re2_example: re2_example.cc
	g++ re2_example.cc -o re2_example -lre2

clean:
	rm -f *.o *.pb.h *.pb.cc gflags_example glog_example protobuf_example \
	re2_example
