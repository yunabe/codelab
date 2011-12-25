run: libBasicModule.so BasicModule.jar
	java -Djava.library.path=`pwd` -classpath BasicModule.jar com.yunabe.main.Main

basic_java_wrap.cc javafiles/com/yunabe/BasicModule.java  javafiles/com/yunabe/BasicModuleJNI.java  javafiles/com/yunabe/Lib.java: basic.i
	swig -c++ -java -package com.yunabe -outdir javafiles/com/yunabe -o basic_java_wrap.cc -module BasicModule basic.i

basic.o: basic.cc basic.h
	g++ -fPIC -c basic.cc -o basic.o

basic_java_wrap.o: basic_java_wrap.cc
	g++ -fPIC -c basic_java_wrap.cc -I/usr/lib/jvm/java-6-openjdk/include/ -I.

libBasicModule.so: basic.o basic_java_wrap.o
	g++ -shared basic.o basic_java_wrap.o -o libBasicModule.so

BasicModule.jar: javafiles/com/yunabe/BasicModule.java  javafiles/com/yunabe/BasicModuleJNI.java  javafiles/com/yunabe/Lib.java javafiles/com/yunabe/main/Main.java
	cd javafiles && javac `find com/yunabe/ | grep "\.java$""` && jar cvf ../BasicModule.jar com

clean:
	rm -rf *.o *.jar *_wrap.cc *.class *.so javafiles/com/yunabe/*.java javafiles/com/yunabe/*.class *.jar
