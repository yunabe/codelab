run: _basic.so _director.so _use_time.so
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

time.o: time.cc
	g++ -fPIC time.cc -c -o time.o

use_time.o: use_time.cc
	g++ -fPIC use_time.cc -c -o use_time.o

use_time_python_wrap.cc use_time.py: use_time.i
	swig -c++ -python -outdir ./ -o use_time_python_wrap.cc -module use_time use_time.i

use_time_python_wrap.o: use_time_python_wrap.cc
	g++ -fPIC use_time_python_wrap.cc -c -o use_time_python_wrap.o -I/usr/include/python2.6

_use_time.so: time.o use_time.o use_time_python_wrap.o
	g++ -shared time.o use_time.o use_time_python_wrap.o -o _use_time.so

clean:
	rm -rf *.o *.so *.pyc basic.py director.py use_time.py *_wrap.cc *_wrap.h
