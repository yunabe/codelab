all: producer_consumer ProducerConsumer.class

producer_consumer: producer_consumer.cc
	g++ producer_consumer.cc -std=c++11 -Wall -pthread -o producer_consumer

ProducerConsumer.class: ProducerConsumer.java
	javac ProducerConsumer.java -Xlint:all

clean:
	rm -rf producer_consumer *.class
