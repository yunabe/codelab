all: fact

fact: fact.8
	8l -o fact fact.8

fact.8: fact.go
	8g fact.go

clean:
	rm -rf *.8 fact
