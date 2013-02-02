all: run_embed

run_embed: Embed.class
	java -classpath jython-2.5.3.jar:. Embed

Embed.class: Embed.java
	javac Embed.java -classpath jython-2.5.3.jar

clean:
	rm -rf *.class
