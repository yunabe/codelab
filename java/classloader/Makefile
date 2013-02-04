all: run_main

run_main: Main.class Module.class ModuleManager.class foo/FooModule.class bar/BarModule.class
	java Main

foo/FooModule.class: FooModule.java Main.class
	mkdir -p foo; javac FooModule.java -d foo

bar/BarModule.class: BarModule.java Main.class
	mkdir -p bar; javac BarModule.java -d bar

ModuleManager.class Module.class Main.class: Main.java Module.java ModuleManager.java
	javac Module.java Main.java ModuleManager.java

clean:
	rm -rf *.class foo bar
