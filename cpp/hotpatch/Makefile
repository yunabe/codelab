all: example example_lib.so

example: example.o hotpatch.o os.o example_lib.o
	g++ example.o example_lib.o hotpatch.o os.o -o example -lgflags -lglog -ldl -rdynamic

example.o: example.cc
	g++ example.cc -c -o example.o

example_lib.o: example_lib.cc
	g++ example_lib.cc -c -fPIC -o example_lib.o

example_lib.so: example_lib.o
	g++ -shared example_lib.o -o example_lib.so

hotpatch.o: hotpatch.cc
	g++ hotpatch.cc -c -o hotpatch.o

os.o: os.cc
	g++ os.cc -c -o os.o

clean:
	rm -f *.o *.so example
