all: run_embed run_reload run_java_wrapper_overhead

run_embed: Embed.class
	java -Dpython.path=python -classpath jython-2.5.3.jar:. Embed

Embed.class: Embed.java
	javac Embed.java -classpath jython-2.5.3.jar

run_reload: Reload.class
	java -classpath jython-2.5.3.jar:. -Dpython.path=python Reload

Reload.class: Reload.java
	javac Reload.java -classpath jython-2.5.3.jar

run_java_wrapper_overhead: JavaWrapperOverhead.class
	java -classpath jython-2.5.3.jar:. -Dpython.path=python JavaWrapperOverhead

JavaWrapperOverhead.class: JavaWrapperOverhead.java
	javac JavaWrapperOverhead.java -classpath jython-2.5.3.jar

clean:
	rm -rf *.class
