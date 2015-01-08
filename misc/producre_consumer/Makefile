all: producer_consumer_c producer_consumer ProducerConsumer.class ProducerConsumerRaw.class

producer_consumer_c: producer_consumer.c
	gcc producer_consumer.c -o producer_consumer_c -pthread -Wall -std=c99 -O3

producer_consumer: producer_consumer.cc
	g++ producer_consumer.cc -std=c++11 -Wall -pthread -o producer_consumer -O3

ProducerConsumer.class: ProducerConsumer.java
	javac ProducerConsumer.java -Xlint:all

ProducerConsumerRaw.class: ProducerConsumerRaw.java
	javac ProducerConsumerRaw.java -Xlint:all

clean:
	rm -rf producer_consumer_c producer_consumer *.class
