all: example_pb2.py test

test: gflags_example_test googletest_example gflags_example
	./googletest_example

example_template.tpl.varnames.h: example_template.tpl
	make_tpl_varnames_h example_template.tpl

example_subtemplate.tpl.varnames.h: example_subtemplate.tpl
	make_tpl_varnames_h example_subtemplate.tpl

ctemplate_example: ctemplate_example.cc example_template.tpl.varnames.h example_subtemplate.tpl.varnames.h
	g++ ctemplate_example.cc -o ctemplate_example -lctemplate -lpthread

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

googletest_example: googletest_example.cc
	g++ googletest_example.cc -o googletest_example -lgtest -lpthread -lgtest_main

example.pb.cc example.pb.h: example.proto
	protoc example.proto --cpp_out=.

example_pb2.py: example.proto
	protoc example.proto --python_out=.

example.pb.o: example.pb.cc example.pb.h
	g++ example.pb.cc -c -o example.pb.o

protobuf_example.o: protobuf_example.cc example.pb.h
	g++ protobuf_example.cc -c -o protobuf_example.o

protobuf_py_test: example_pb2.py
	python protobuf_test.py

# -lpthread is required to link protobuf library.
protobuf_example: protobuf_example.o example.pb.o
	g++ protobuf_example.o example.pb.o -o protobuf_example -lprotobuf -lpthread

re2_example: re2_example.cc
	g++ re2_example.cc -o re2_example -lre2

gperftools_leak: gperftools_leak.cc
	g++ gperftools_leak.cc -o gperftools_leak -ltcmalloc

clean:
	rm -f *.o *.pb.h *.pb.cc *_pb2.py gflags_example glog_example \
  protobuf_example re2_example googletest_example *.varnames.h \
  ctemplate_example gperftools_leak
