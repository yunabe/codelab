all: main Calc.class

Calc.class: Calc.java
	javac Calc.java

main: main.o
	g++ -o main main.o -L /usr/lib/jvm/java-6-openjdk/jre/lib/amd64/server -ljvm

main.o: main.cc
	g++ -o main.o -c main.cc -I/usr/lib/jvm/java-6-openjdk/include

clean:
	rm -rf *.o main *.class