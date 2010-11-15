main: main.o nativetype_wrap.o
	g++ main.o nativetype_wrap.o -o main -lpython2.6

main.o: main.cc
	g++ main.cc -I/usr/include/python2.6 -c -o main.o

nativetype.py nativetype_wrap.cxx: nativetype.i
	swig -c++ -python nativetype.i

nativetype_wrap.o: nativetype_wrap.cxx
	g++ nativetype_wrap.cxx -I/usr/include/python2.6 -c -o nativetype_wrap.o

clean:
	rm -rf *.pyc *.o *_wrap.cxx nativetype.py main
