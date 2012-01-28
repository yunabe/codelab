run: _basic.so _director.so
	python main.py

basic_python_wrap.cc basic.py: basic.i
	swig -c++ -python -outdir ./ -o basic_python_wrap.cc -module basic basic.i

basic.o: basic.cc basic.h
	g++ -fPIC -c basic.cc -o basic.o

basic_python_wrap.o: basic_python_wrap.cc
	g++ -fPIC -c basic_python_wrap.cc -I/usr/include/python2.6

_basic.so: basic.o basic_python_wrap.o
	g++ -shared basic.o basic_python_wrap.o -o _basic.so

director_python_wrap.cc director.py: director.i
	swig -c++ -python -outdir ./ -o director_python_wrap.cc -module director director.i

director.o: director.cc director.h
	g++ -fPIC -c director.cc -o director.o

director_python_wrap.o: director_python_wrap.cc
	g++ -fPIC -c director_python_wrap.cc -I/usr/include/python2.6

_director.so: director.o director_python_wrap.o
	g++ -shared director.o director_python_wrap.o -o _director.so

clean:
	rm -rf *.o *.so *.pyc basic.py director.py *_wrap.cc *_wrap.h
