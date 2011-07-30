all: main func_add.so func_mul.so

# -rdynamic is needed to allow shared libraries to access symbols in main.
# In this example, show_result is called from shared libraries.
main: main.cc
	g++ -rdynamic -o main main.cc -ldl

func_add.o: func_add.cc
	g++ -fPIC -c -o func_add.o func_add.cc

func_add.so: func_add.o
	g++ -shared -o func_add.so func_add.o

func_mul.o: func_mul.cc
	g++ -fPIC -c -o func_mul.o func_mul.cc

func_mul.so: func_mul.o
	g++ -shared -o func_mul.so func_mul.o

clean:
	rm -f *.o *.so main
