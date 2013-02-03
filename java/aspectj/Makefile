all: run_hello

run_hello: HelloWorld.class HelloWorldTracing.class
	java -classpath /home/yunabe/local/aspectj1.7/lib/aspectjrt.jar:. HelloWorld

HelloWorld.class HelloWorldTracing.class: HelloWorld.java HelloWorldTracing.aj
	ajc -d . -classpath /home/yunabe/local/aspectj1.7/lib/aspectjrt.jar HelloWorld.java HelloWorldTracing.aj

clean:
	rm -rf *.class
