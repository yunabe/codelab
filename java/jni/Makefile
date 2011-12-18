all: main bad_example Calc.class Data.class

Calc.class: Calc.java
	javac Calc.java

Data.class: Data.java
	javac Data.java

main: main.o
	g++ -o main main.o -L /usr/lib/jvm/java-6-openjdk/jre/lib/amd64/server -ljvm

main.o: main.cc
	g++ -o main.o -c main.cc -I/usr/lib/jvm/java-6-openjdk/include

bad_example: bad_example.o
	g++ -o bad_example bad_example.o -L /usr/lib/jvm/java-6-openjdk/jre/lib/amd64/server -ljvm

bad_example.o: bad_example.cc
	g++ -o bad_example.o -c bad_example.cc -I/usr/lib/jvm/java-6-openjdk/include

clean:
	rm -rf *.o *.class main bad_example