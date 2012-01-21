run: libBasicModule.so libDirectorModule.so BasicModule.jar libTimeModule.so
	java -Djava.library.path=`pwd` -classpath BasicModule.jar com.yunabe.main.Main

basic_java_wrap.cc javafiles/com/yunabe/BasicModule.java  javafiles/com/yunabe/BasicModuleJNI.java  javafiles/com/yunabe/Lib.java: basic.i
	swig -c++ -java -package com.yunabe -outdir javafiles/com/yunabe -o basic_java_wrap.cc -module BasicModule basic.i

basic.o: basic.cc basic.h
	g++ -fPIC -c basic.cc -o basic.o

basic_java_wrap.o: basic_java_wrap.cc
	g++ -fPIC -c basic_java_wrap.cc -I/usr/lib/jvm/java-6-openjdk/include/

libBasicModule.so: basic.o basic_java_wrap.o include_and_import.o include_and_import_java_wrap.o
	g++ -shared basic.o basic_java_wrap.o include_and_import.o include_and_import_java_wrap.o -o libBasicModule.so

BasicModule.jar: javafiles/com/yunabe/BasicModule.java  javafiles/com/yunabe/BasicModuleJNI.java javafiles/com/yunabe/IncludeAndImportModule.java javafiles/com/yunabe/Lib.java javafiles/com/yunabe/DirectorModuleJNI.java javafiles/com/yunabe/TimeModule.java javafiles/com/yunabe/main/Main.java
	cd javafiles && javac `find com/yunabe/ | grep "\.java$""` && jar cvf ../BasicModule.jar com

include_and_import.o: include_and_import.cc include_and_import.h
	g++ -fPIC -c include_and_import.cc -o include_and_import.o

include_and_import_java_wrap.o: include_and_import_java_wrap.cc
	g++ -fPIC -c include_and_import_java_wrap.cc -I/usr/lib/jvm/java-6-openjdk/include/

libIncludeAndImportModule.so: include_and_import.o include_and_import_java_wrap.o
	g++ -shared include_and_import.o include_and_import_java_wrap.o -o libIncludeAndImportModule.so

include_and_import_java_wrap.cc javafiles/com/yunabe/IncludeAndImportModule.java: include_and_import.i
	swig -Wall -c++ -java -package com.yunabe -outdir javafiles/com/yunabe -o include_and_import_java_wrap.cc -module IncludeAndImportModule include_and_import.i

director_java_wrap.cc javafiles/com/yunabe/DirectorModuleJNI.java: director.i
	swig -c++ -java -package com.yunabe -outdir javafiles/com/yunabe -o director_java_wrap.cc -module DirectorModule director.i

director.o: director.cc director.h
	g++ -fPIC -c director.cc -o director.o

libTimeModule.so: time.o use_time.o use_time_java_wrap.o
	g++ -shared time.o use_time.o use_time_java_wrap.o -o libTimeModule.so

time.o: time.cc time.h
	g++ -fPIC -c time.cc -o time.o

use_time.o: use_time.cc use_time.h
	g++ -fPIC -c use_time.cc -o use_time.o

use_time_java_wrap.cc javafiles/com/yunabe/TimeModule.java: use_time.i
	swig -c++ -java -package com.yunabe -outdir javafiles/com/yunabe -o use_time_java_wrap.cc -module TimeModule use_time.i

use_time_java_wrap.o: use_time_java_wrap.cc
	g++ -fPIC -c use_time_java_wrap.cc -I/usr/lib/jvm/java-6-openjdk/include/

director_java_wrap.o: director_java_wrap.cc director_java_wrap.h
	g++ -fPIC -c director_java_wrap.cc -I/usr/lib/jvm/java-6-openjdk/include/

libDirectorModule.so: director.o director_java_wrap.o
	g++ -shared director.o director_java_wrap.o -o libDirectorModule.so

clean:
	rm -rf *.o *.jar *_wrap.cc *_wrap.h *.class *.so javafiles/com/yunabe/*.java javafiles/com/yunabe/*.class *.jar hs_err_*.log
