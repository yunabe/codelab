all: max_num_thread performance

max_num_thread: max_num_thread.cc
	g++ max_num_thread.cc -o max_num_thread -std=c++0x -lpthread
performance: performance.cc
	g++ performance.cc -o performance -std=c++0x -lpthread

clean:
	/bin/rm -f max_num_thread performance
