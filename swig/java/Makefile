all: BasicModule.so BasicModule.jar

swig:
	swig -c++ -java -package com.yunabe -outdir javafiles/com/yunabe -o basic_java_wrap.cc -module BasicModule basic.i

basic.o: basic.cc basic.h
	g++ -fPIC -c basic.cc -o basic.o

basic_java_wrap.o: swig
	g++ -fPIC -c basic_java_wrap.cc -I/usr/lib/jvm/java-6-openjdk/include/ -I.

BasicModule.so: basic.o basic_java_wrap.o
	g++ -shared basic.o basic_java_wrap.o -o libBasicModule.so

BasicModule.jar: swig
	cd javafiles && javac `find com/yunabe/ | grep "\.java$""` && jar cvf ../BasicModule.jar com

clean:
	rm -rf *.o *.jar *_wrap.cc *.class *.so javafiles/com/yunabe/*.java javafiles/com/yunabe/*.class *.jar
