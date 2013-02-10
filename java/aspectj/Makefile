all: run_hello

# Compile-time weaving
run_hello: compile/HelloWorld.class compile/HelloWorldTracing.class
	java -classpath /home/yunabe/local/aspectj1.7/lib/aspectjrt.jar:compile HelloWorld

compile/HelloWorld.class compile/HelloWorldTracing.class: HelloWorld.java HelloWorldTracing.aj
	mkdir -p compile && ajc -d compile -classpath /home/yunabe/local/aspectj1.7/lib/aspectjrt.jar HelloWorld.java HelloWorldTracing.aj

# Load-time weaving
run_loadtime_hello: loadtime/HelloWorld.class loadtime/HelloWorldTracing.class loadtime/META-INF/aop.xml
	java -classpath /home/yunabe/local/aspectj1.7/lib/aspectjrt.jar:loadtime:weaver.jar -javaagent:/home/yunabe/local/aspectj1.7/lib/aspectjweaver.jar HelloWorld

loadtime/HelloWorld.class: HelloWorld.java
	mkdir -p loadtime && javac -d loadtime HelloWorld.java

loadtime/HelloWorldTracing.class: HelloWorldTracing.aj loadtime/HelloWorld.class
	mkdir -p loadtime && ajc -d loadtime -classpath /home/yunabe/local/aspectj1.7/lib/aspectjrt.jar:loadtime HelloWorldTracing.aj

loadtime/META-INF/aop.xml: aop.xml
	mkdir -p loadtime/META-INF && cp aop.xml loadtime/META-INF/aop.xml

clean:
	rm -rf *.class compile loadtime
