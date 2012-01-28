run: _basic.so
	python main.py

basic_python_wrap.cc basic.py: basic.i
	swig -c++ -python -outdir ./ -o basic_python_wrap.cc -module basic basic.i

basic.o: basic.cc basic.h
	g++ -fPIC -c basic.cc -o basic.o

basic_python_wrap.o: basic_python_wrap.cc
	g++ -fPIC -c basic_python_wrap.cc -I/usr/include/python2.6

_basic.so: basic.o basic_python_wrap.o
	g++ -shared basic.o basic_python_wrap.o -o _basic.so

clean:
	rm -rf *.o *.so *.pyc basic.py *_wrap.cc
