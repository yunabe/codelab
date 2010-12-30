# Please make sure that binutils-dev has been installed.

main: main.o sample.o new_sample.so dynamic_update.o
	g++ main.o sample.o dynamic_update.o -o main -ldl -lbfd -rdynamic

dynamic_update.o: dynamic_update.cc
	g++ dynamic_update.cc -c -o dynamic_update.o

sample.o: sample.cc sample.h
	g++ sample.cc -c -o sample.o

main.o: main.cc sample.h
	g++ main.cc -c -o main.o

new_sample.o: new_sample.cc sample.h
	g++ new_sample.cc -c -o new_sample.o -fPIC

new_sample.so: new_sample.o
	g++ new_sample.o -shared -o new_sample.so

clean:
	rm -f *.o *.so main
