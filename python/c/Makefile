pycfunc.so: pycfunc.o
	g++ -shared pycfunc.o -o pycfunc.so

pycfunc.o: pycfunc.cc auto_pyobj.h
	g++ -fPIC -c -o pycfunc.o -I/usr/include/python2.6/ pycfunc.cc

test: pycfunc.so pycfunc_test.py
	python pycfunc_test.py

clean:
	rm -f pycfunc.so pycfunc.o
