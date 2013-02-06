all: run_embed run_reload

run_embed: Embed.class
	java -classpath jython-2.5.3.jar:. Embed

Embed.class: Embed.java
	javac Embed.java -classpath jython-2.5.3.jar

run_reload: Reload.class
	java -classpath jython-2.5.3.jar:. -Dpython.path=python Reload

Reload.class: Reload.java
	javac Reload.java -classpath jython-2.5.3.jar

clean:
	rm -rf *.class
